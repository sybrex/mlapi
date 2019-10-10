#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

source ./venv/bin/activate
uvicorn --root-path=$DIR --port=8000 api:app --reload