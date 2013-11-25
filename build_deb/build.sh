#!/bin/sh

# v1.1 - 2013.11.25
# updated for v3.0.1
# v1.0 - 2013.5.12
# inited.

if [ -d 'fakeroot' ]; then
	rm -rvf fakeroot
fi

PYLIB='fakeroot/usr/lib/python3/dist-packages/'

mkdir -vp fakeroot/usr/bin fakeroot/DEBIAN $PYLIB

cp -v ../qr-gui fakeroot/usr/bin/
cp -rvf ../qr_gui $PYLIB
rm -rvf $PYLIB/qr_gui/__pycache__
cp -rvf ../share fakeroot/usr/share
cp -vf control fakeroot/DEBIAN/
