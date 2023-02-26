import abc
import time
from pathlib import Path
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar, Union

import pytest
from _pytest._py.path import LocalPath

from palindromi_fi_builder.syncer import Syncer

T = TypeVar("T")


class SyncerAction(abc.ABC, Generic[T]):
    def __init__(self, new_content: T) -> None:
        self.new_content = new_content

    def create_src(self, path: Path) -> None:
        pass

    @abc.abstractmethod
    def run_syncer(
        self, syncer_obj: Syncer, src: Path, dest: Path
    ) -> Union[bool, Set[Path]]:
        pass


class Write(SyncerAction[str]):
    """For written files, create no source file and just write the target"""

    def run_syncer(self, syncer_obj: Syncer, src: Path, dest: Path) -> bool:
        return syncer_obj.write_text(self.new_content, dest)


class Copy(SyncerAction[str]):
    """For copied files, create the source file and copy it to the target"""

    def create_src(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.new_content)

    def run_syncer(self, syncer_obj: Syncer, src: Path, dest: Path) -> bool:
        return syncer_obj.copy(src, dest)


class CopyTree(SyncerAction[Dict[str, str]]):
    """For copied trees, create the source files and copy them to the target"""

    def create_src(self, path: Path) -> None:
        for fp, new_content in self.new_content.items():
            (path / fp).parent.mkdir(parents=True, exist_ok=True)
            (path / fp).write_text(new_content)

    def run_syncer(self, syncer_obj: Syncer, src: Path, dest: Path) -> Set[Path]:
        return syncer_obj.copytree(src, dest)


class Verifier(str):
    """Base class for test result verifiers"""

    def verify(self, path: Path, original_mtime: Optional[float] = None) -> None:
        pass


class Directory(Verifier):
    """Verify that the destination directory exists"""

    def verify(self, path, original_mtime: Optional[float] = None) -> None:
        """Verify that the destination directory exists

        :param path: Path to the directory to verify
        :param original_mtime: Original modification time of the directory
        :raises AssertionError: If the directory doesn't exist

        """
        assert path.is_dir()


class FileVerifier(Verifier):
    """Verify that the destination file has correct contect"""

    def verify(self, path, original_mtime: Optional[float] = None):
        assert path.read_text("utf-8") == self


class New(FileVerifier):
    """Verify correct content and no previous file for newly written files"""

    def verify(self, path, original_mtime: Optional[float] = None):
        """Verify correct content and no previous file for newly written files

        :param path: Path to the file to verify
        :param original_mtime: Original modification time of the file
        :raises AssertionError: If the contents are not correct, or if an original
                                mtime is given while the file didn't exist before

        """
        super().verify(path)
        assert not original_mtime


class Updated(FileVerifier):
    """Verify correct content and newer mtime for updated files"""

    def verify(self, path: Path, original_mtime: Optional[float] = None) -> None:
        """Verify correct content and newer modification time for updated files

        :param path: Path to the file to verify
        :param original_mtime: Original modification time of the file
        :raises AssertionError: If the contents has changed, or if the new modification
                                time isn't later than the original

        """
        super().verify(path)
        assert path.stat().st_mtime > original_mtime


class Kept(FileVerifier):
    """Verify same content and intact modification time for identical existing files"""

    def verify(self, path: Path, original_mtime: Optional[float] = None) -> None:
        """Verify correct content and original modification time for identical files

        :param path: Path to the file to verify
        :param original_mtime: Original modification time of the file
        :raises AssertionError: If the contents has changed, or if the new modification
                                time isn't the same as the original

        """
        super().verify(path)
        assert path.stat().st_mtime == original_mtime


@pytest.mark.parametrize(
    "dest, src, expect",
    [
        ({}, [("a", Write("new"))], {"a": New("new")}),
        ({}, [("a/b", Write("new"))], {"a": Directory(), "a/b": New("new")}),
        ({}, [("a/b", Copy("new"))], {"a": Directory(), "a/b": New("new")}),
        (
            {},
            [("a/b", CopyTree({"c": "new", "d/e": "new"}))],
            {
                "a": Directory(),
                "a/b": Directory(),
                "a/b/c": New("new"),
                "a/b/d": Directory(),
                "a/b/d/e": New("new"),
            },
        ),
        ({"a": "same"}, [("a", Write("same"))], {"a": Kept("same")}),
        ({"a": "same"}, [("a", Copy("same"))], {"a": Kept("same")}),
        ({"a": "old"}, [("a", Write("update"))], {"a": Updated("update")}),
        ({"a": "old"}, [("a", Copy("update"))], {"a": Updated("update")}),
        ({"a": "delete"}, [("b", Write("new"))], {"b": New("new")}),
        ({"a": "delete"}, [("b", Copy("new"))], {"b": New("new")}),
        (
            {"a/b": "old", "c/d": "same", "e/f": "delete"},
            [("a/b", Write("update")), ("c/d", Write("same")), ("g/h", Write("new"))],
            {
                "a": Directory(),
                "a/b": Updated("update"),
                "c": Directory(),
                "c/d": Kept("same"),
                "g": Directory(),
                "g/h": New("new"),
            },
        ),
    ],
)
def test_syncer(
    dest: Dict[str, str],
    src: List[Tuple[str, SyncerAction]],
    expect: Dict[str, FileVerifier],
    tmpdir: LocalPath,
) -> None:
    """Test the `Syncer` class

    :param dest: Dictionary of files to create in the destination directory
    :param src: List of files to create in the source directory and the action to
                perform on them
    :param expect: Dictionary of files to verify in the destination directory and the
                   verifier to use
    :param tmpdir: Temporary directory to use for the test

    """
    src_root = Path(tmpdir / "src")
    src_root.mkdir()
    dest_root = Path(tmpdir / "dest")
    dest_root.mkdir()

    # Write existing content into the destination directory
    original_mtimes = {}
    for p, old_content in dest.items():
        dest_abs = dest_root / p
        dest_abs.parent.mkdir(parents=True, exist_ok=True)
        dest_abs.write_text(old_content)
        original_mtimes[dest_abs] = dest_abs.stat().st_mtime

    # Write content to be copied in the source directory
    for path, action in src:
        source_path = Path(src_root / path)
        action.create_src(source_path)

    # ensure new mtimes will be different
    time.sleep(0.001)

    # Write files, copy files and/or copy trees, and finally delete all
    # non-touched files.
    syncer = Syncer(dest_root)
    for path, action in src:
        dest_abs = Path(dest_root / path)
        action.run_syncer(syncer, src_root / path, dest_abs)
    syncer.remove_deleted()

    # Verify that
    # - resulting files have correct content
    # - unmodified files have their old timestamp
    # - untouched files are deleted
    result_paths = set(dest_root.rglob("*"))
    for p, expect_content in expect.items():
        expect_abs = Path(dest_root / p)
        expect_content.verify(expect_abs, original_mtimes.get(expect_abs))
        result_paths.discard(expect_abs)
        for parent in expect_abs.parents:
            result_paths.discard(parent)
    assert not result_paths
