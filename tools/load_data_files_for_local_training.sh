#!/bin/bash

mkdir ../src/data

aws s3 sync s3://<bucket-name>/data/ ../src/data --include "*.csv" --exact-timestamps
