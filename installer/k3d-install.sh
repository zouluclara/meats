#!/bin/bash

cd `dirname $0`

function die() {
  echo "ERROR $*"
  exit
}

pip install -e . || die pip

jupyter nbextension enable --py widgetsnbextension --sys-prefix || die widgets
jupyter nbextension install --py --sys-prefix k3d || die install
jupyter nbextension enable --py --sys-prefix k3d || die enable
