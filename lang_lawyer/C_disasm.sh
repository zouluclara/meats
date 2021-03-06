#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 [options, like -O3] file.c"
    exit
fi

gcc -g -c -o /tmp/C_disasm.o "$@"
objdump -S -M intel  /tmp/C_disasm.o
rm /tmp/C_disasm.o
