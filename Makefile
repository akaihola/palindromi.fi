ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

all: clean build

clean:
	rm $(ROOT_DIR)palindromi_fi_builder/static/__target__ -rf
	rm $(ROOT_DIR)html/* -rf

build: palindromi_fi_builder/static/__target__/palindrome.js html/index.html

palindromi_fi_builder/static/__target__/palindrome.js: palindromi_fi_builder/static/palindrome.py
	transcrypt -b -m -n $(ROOT_DIR)palindromi_fi_builder/static/palindrome.py
	# remove trailing timestamp from first line of JS files to minimize changes between builds
	sed -i '1s/, .*//' $(ROOT_DIR)palindromi_fi_builder/static/__target__/*.js
	# remove absolute paths from project file to minimize changes between builds
	sed -i 's:"/[^"]*\(palindromi_fi\|transcrypt/modules\):"\1:g' $(ROOT_DIR)palindromi_fi_builder/static/__target__/palindrome.project

html/index.html: palindromi_fi_builder/static/__target__/palindrome.js palindromi_fi_builder/templates palindromi_fi_builder/*.py
	python -m palindromi_fi_builder render \
	  $(ROOT_DIR)database \
	  -o $(ROOT_DIR)html

lint:
	darker -L "darglint2 -v 2" -L pylint -L flake8 -L mypy
