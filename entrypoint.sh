#!/bin/sh -l

echo "Entrypoint Shell"

echo "Parameter: filetype, Value: $1"

python /hello.py -v $GITHUB_WORKSPACE -f $1

time=$(date)
echo "::set-output name=time::$time"

