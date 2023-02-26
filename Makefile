ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
REMOTE_REPO ?= $(REMOTE_REPO):origin

all: clean build upload

clean:
	rm $(ROOT_DIR)palindromi_fi_builder/static/__target__ -rf
	rm $(ROOT_DIR)html/* -rf

build: palindromi_fi_builder/static/__target__/palindrome.js html/index.html

palindromi_fi_builder/static/__target__/palindrome.js: palindromi_fi_builder/static/palindrome.py
	transcrypt -b -m -n $(ROOT_DIR)palindromi_fi_builder/static/palindrome.py

html/index.html: palindromi_fi_builder/static/__target__/palindrome.js palindromi_fi_builder/templates palindromi_fi_builder/*.py
	python -m palindromi_fi_builder render \
	  $(ROOT_DIR)database \
	  -o $(ROOT_DIR)html

upload: upload-files fix-content-types

upload-files:
	gsutil -m rsync \
	  -R \
	  -d $(ROOT_DIR)html \
	  gs://www.palindromi.fi

fix-content-types:
	gsutil -m setmeta \
	  -h "Content-Type:text/html" \
	  gs://www.palindromi.fi/*
	gsutil -m setmeta \
	  -h "Content-Type:text/css" \
	  gs://www.palindromi.fi/static/*.css

lint:
	darker -L "darglint2 -v 2" -L pylint -L flake8 -L mypy

render_to_branch:
	RENDERED=$$(mktemp -d) ;\
	git worktree add $$RENDERED rendered ;\
	WORKSPACE=$$(pwd) ;\
	git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com" ;\
	git config --global user.name "${GITHUB_ACTOR}" ;\
	git config --global --add safe.directory $$WORKSPACE ;\
	git merge -X theirs --no-commit origin/main ;\
	make build ;\
	git add -A ;\
	git commit -m "Rendered $$(git rev-parse --short origin/main)" ;\
	git push -v --force-with-lease $(REMOTE_REPO) rendered ;\
	cd $$WORKSPACE ;\
	git worktree remove $$RENDERED

upload_rendered_branch:
	git config --global --add safe.directory $$(pwd) ;\
	RENDERED=$$(mktemp -d) ;\
	git worktree add $$RENDERED rendered ;\
	WORKSPACE=$$(pwd) ;\
	make upload ;\
	cd $$WORKSPACE ;\
	git worktree remove $$RENDERED
