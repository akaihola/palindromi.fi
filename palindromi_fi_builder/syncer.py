"""Update contents of a target directory with minimal changes

Preserves timestamps for unchanged files, originally to support rsync-based
publishing. Current deployment uploads a GitHub Pages artifact.

Process each destination once per Syncer instance. Repeated writes are not
idempotent, and repeating a directory-tree copy can raise KeyError. Destinations
must be under the root. Deletion occurs only when remove_deleted() is called.

Supports three operations:
- writing contents to a file
- copying a file from another location
- copying a directory tree from another location

Makes sure that:
- existing identical files are not touched
- existing different files are overwritten
- existing extra files are deleted

Usage::

    from pathlib import Path
    from palindromi_fi_builder.syncer import Syncer

    syncer = Syncer(Path('/my/target'))
    syncer.write_text('foo', Path('/my/target/subdir/foo.txt'))
    syncer.copy(Path('bar.txt'), Path('/my/target/bar.txt'))
    syncer.copytree(Path('mytree'), Path('/my/target/mytree'))
    syncer.remove_deleted()

"""

from pathlib import Path
from typing import Set


def mkdirp(path: Path) -> None:
    """Create a directory and all its parents if they don't exist

    :param path: Path to the directory to create

    """
    path.mkdir(parents=True, exist_ok=True)


class Syncer:
    """Update contents of a target directory with minimal changes"""

    def __init__(self, root: Path) -> None:
        self.root = root.absolute()
        self.old_files: Set[Path] = set(self.root.rglob("*"))
        self.new_files: Set[Path] = set()

    def _forget(self, path: Path) -> None:
        self.new_files.add(path)
        for directory in path.relative_to(self.root).parents:
            self.new_files.add(self.root / directory)

    def write_bytes(self, new_content: bytes, dest: Path) -> bool:
        """Write content to a file and update tracking of old/new files

        :param new_content: Content to write
        :param dest: Path to the file to write
        :return: True if written; False if the first write matches an existing file

        """
        dest = dest.absolute()
        self._forget(dest)
        if dest in self.old_files:
            self.old_files.remove(dest)
            old_content = dest.read_bytes()
            if new_content == old_content:
                return False
        mkdirp(dest.parent)
        dest.write_bytes(new_content)
        return True

    def write_text(self, new_content: str, dest: Path) -> bool:
        """Write UTF-8 text to a file and update tracking of old/new files

        :param new_content: Content to write
        :param dest: Path to the file to write
        :return: True if written; False if the first write matches an existing file

        """
        return self.write_bytes(new_content.encode("UTF-8"), dest)

    def copy(self, src: Path, dest: Path) -> bool:
        """Copy a file and update tracking of old/new files

        :param src: Path to the source file
        :param dest: Path to the destination file
        :return: True if written; False if the first write matches an existing file

        """
        new_content = src.read_bytes()
        return self.write_bytes(new_content, dest)

    def copytree(self, src_root: Path, dest_root: Path) -> Set[Path]:
        """Copy a directory tree and update tracking of old/new files

        :param src_root: Path to the source directory
        :param dest_root: Path to the destination directory
        :return: Absolute destination paths for files and subdirectories, including
                 unchanged entries, but excluding dest_root itself

        """
        copied = set()
        for src in src_root.rglob("*"):
            relative_path = src.relative_to(src_root)
            dest = (dest_root / relative_path).absolute()
            copied.add(dest)
            if src.is_dir():
                self._forget(dest)
                if dest.is_dir():
                    self.old_files.remove(dest)
                else:
                    mkdirp(dest)
            else:
                self.copy(src, dest)
        return copied

    def remove_deleted(self) -> None:
        """Remove initial files and directories not registered by write/copy calls"""
        for path in sorted(self.old_files - self.new_files, reverse=True):
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()
