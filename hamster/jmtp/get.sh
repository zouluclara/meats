#!/bin/bash

target=`pwd`
pushd `dirname $0`/..
./jmtp/mount.sh
cp -iv mnt/Phone/com.hipipal.qpyplus/scripts/$1 $target
./jmtp/umount.sh
popd
