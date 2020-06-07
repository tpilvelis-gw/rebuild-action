#!/bin/sh -l

echo "Entry Point Shell Shell"

echo "Parameter: filetype, Value: $1"

echo "Run Hello Python Script"

python /hello.py -v $GITHUB_WORKSPACE -f $1

time=$(date)
echo "::set-output name=time::$time"

