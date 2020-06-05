#!/bin/sh -l

echo "Parameter: filetype, Value: $1"

echo "Run Hello Python Script"
python /hello.py $1

log=$(<log.txt)
echo "::set-output name=log::$log"

time=$(date)
echo "::set-output name=time::$time"

