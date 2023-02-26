#!/bin/sh

echo "${INPUT_SECRETS}" >/secrets.json
gcloud auth activate-service-account --key-file=/secrets.json
rm /secrets.json
make upload_rendered_branch
