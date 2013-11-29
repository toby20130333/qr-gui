ABOUT
=====
qr-gui QR Image encoder/decoer with GUI.

qr-gui is a GUI tool to generate QR images or decode QR from image files or webcam, using qrencode and zbar as backend.

Tested on Debian testing.


Features
========
* Easy to use.
* Instant QR image generation.
* Decoding QR by selecting an area on screen.


INSTALL
=======
For Debian based systems(like Deibna, Linux Mint), please download and install the deb package.

For other linux distributions, please install it with `pip3` - python3
version of pip:

    # pip3 install qr-gui


DEPENDENCIES
============
In linux desktops other than debian based systems, you may need to solve pakcage deepencies manually, by installing these packages:
* qrencode - commandline interface of `qrencode`.
* python3-gi - Python3 bindings for gobject-introspection libraries.
* zbar-tools - decode QR from images or webcam.


TODO
====
* Add rpm package builder.


SCREENSHOT
==========
![qrencoegui screenshot](screenshots/screenshot-0.png?raw=true)
