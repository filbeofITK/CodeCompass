#!/usr/bin/env bash

set -e

unzip "$1" -d "/tmp"
cp --recursive "/tmp/sources-root/"* "/"
CodeCompass_parser --workspace /mnt/output/workspace --name SourceProject --input compilation_database.json --database "sqlite:database=/mnt/output/SourceProject.sqlite"

