#!/bin/sh -l

echo "Parameter: filetype, Value: $1"

echo "Run Hello Python Script"
python /hello.py $1 2&>1 | tee logfile.log

echo logfile.log

time=$(date)
echo "::set-output name=time::$time"