#! /bin/bash

# Script to generate and publish techdopcs from current directory to gcs
export GOOGLE_APPLICATION_CREDENTIALS=~/gcr.json
techdocs-cli generate --source-dir . 
techdocs-cli publish --publisher-type googleGcs --storage-name techdocs-tap --entity alpha/Component/surfersweb

