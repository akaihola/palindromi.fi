ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
REMOTE_REPO ?= origin
GITHUB_ACTOR ?= akaihola

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
	  -d ./html \
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
	WORKSPACE=$$(pwd) ;\
	RENDERED=$$(mktemp -d) ;\
	git worktree add $$RENDERED rendered ;\
	cd $$RENDERED ;\
	git config user.email "${GITHUB_ACTOR}@users.noreply.github.com" ;\
	git config user.name "Antti Kaihola" ;\
	git config --add safe.directory $$WORKSPACE ;\
	git fetch origin rendered ;\
	git merge -X theirs --no-commit origin/main ;\
	make build ;\
	git add -A ;\
	git commit -m "Rendered $$(git rev-parse --short origin/main)" ;\
	git push -v --force $(REMOTE_REPO) rendered ;\
	cd $$WORKSPACE ;\
	git worktree remove $$RENDERED

upload_rendered_branch:
	git config --global --add safe.directory $$(pwd) ;\
	RENDERED=$$(mktemp -d) ;\
	git worktree add $$RENDERED rendered ;\
	WORKSPACE=$$(pwd) ;\
	cd $$RENDERED ;\
	make upload ;\
	cd $$WORKSPACE ;\
	git worktree remove $$RENDERED
