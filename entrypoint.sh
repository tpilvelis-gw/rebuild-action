#!/bin/sh -l

echo "Parameter: filetype, Value: $1"

echo "Run Hello Python Script"
python /hello.py $1

time=$(date)
echo "::set-output name=time::$time"