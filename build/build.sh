#!/bin/sh

# v1.0 - 2013.5.12
# inited.

if [ -d 'fakeroot' ]; then
	rm -rvf fakeroot
fi

PYLIB='fakeroot/usr/lib/python3/dist-packages/'

mkdir -vp fakeroot/usr/bin fakeroot/DEBIAN $PYLIB

cp -v ../qrencode-gui fakeroot/usr/bin/
cp -rvf ../qrencodegui $PYLIB
rm -rvf $PYLIB/qrencodegui/__pycache__
mv -vf $PYLIB/qrencodegui/Config.py.build $PYLIB/qrencodegui/Config.py
cp -rvf ../share fakeroot/usr/share
cp -vf control fakeroot/DEBIAN/
