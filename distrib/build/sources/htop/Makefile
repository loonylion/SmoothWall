# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = htop
VERSION = 2.2.0

PATCH_FILE1=htop-Makefile.patch

BASE_URL = http://hisham.hm/htop/releases/$(VERSION)/

PRE_CONFIGURE = LDFLAGS=-ltinfo
CONFIG_OPTS += --prefix=/usr --disable-unicode

include ../Makefile.rules
