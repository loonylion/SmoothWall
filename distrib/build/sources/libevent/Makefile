# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = libevent
VERSION = 2.1.10

#BASE_URL = http://downloads.sourceforge.net/levent/
BASE_URL = https://github.com/libevent/libevent/releases/download/release-$(VERSION)/
TARBALL = $(PACKAGE)-$(VERSION)-stable
DIR = $(TARBALL)

CONFIG_OPTS = --prefix=/usr \
	      --disable-static

include ../Makefile.rules
