#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    print "\nUsage: %s {template} \n\n" $0
fi

python radix-subst.py --props .properties --src_path  --dst_path ./dist

# can be used for one file
#python subst.py --props ./secure.properties --src_path ./templates/test.txt --dst_path ./dist/test.txt
