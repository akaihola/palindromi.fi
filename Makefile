ROOT_DIR:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

all: clean build upload

clean:
	rm $(ROOT_DIR)palindromi_fi_builder/static/__target__ -rf
	rm $(ROOT_DIR)html/* -rf

build: palindromi_fi_builder/static/__target__/palindrome.js html/index.html

palindromi_fi_builder/static/__target__/palindrome.js: palindromi_fi_builder/static/palindrome.py
	transcrypt -b -m -n $(ROOT_DIR)palindromi_fi_builder/static/palindrome.py

html/index.html: palindromi_fi_builder/static/__target__/palindrome.js
	python -m palindromi_fi_builder render \
	  $(ROOT_DIR)database \
	  -o $(ROOT_DIR)html

upload:
	BOTO_FILE=$(ROOT_DIR).boto ; \
	gsutil \
	  -o "GSUtil:use_magicfile=True" \
	  rsync \
		-R \
		-d $(ROOT_DIR)html \
		gs://www.palindromi.fi
