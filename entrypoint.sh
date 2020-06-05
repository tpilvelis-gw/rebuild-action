#!/bin/sh -l

echo "Hello $1 $2"
time=$(date)

echo "Run Hello Python Script"
python /hello.py

echo "::set-output name=time::$time"