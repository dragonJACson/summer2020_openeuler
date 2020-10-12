#!/bin/bash

if [ "x$1" == "x--delete" -o "x$1" == "x-d" ]; then
    delete_path=$(echo $2)
    delete=1
    shift
    shift
else
    find_path=$(echo $1)
    delete=0
    shift
    shift
fi

if [ $delete == 1 ]; then
    find $delete_path -type f -name "*.token" -print0 | xargs -I {} -0 rm -v "{}"
else
    find $find_path -type f -name "*.token" -print
fi
