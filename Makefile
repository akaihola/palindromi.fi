ROOT_DIR:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

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
	gsutil \
	  rsync \
		-R \
		-d $(ROOT_DIR)html \
		gs://www.palindromi.fi

fix-content-types:
	gsutil setmeta \
	  -h "Content-Type:text/html" \
	  gs://www.palindromi.fi/*
	gsutil setmeta \
	  -h "Content-Type:text/css" \
	  gs://www.palindromi.fi/static/*.css
