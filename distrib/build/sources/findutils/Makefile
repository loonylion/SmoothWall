# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = findutils
VERSION = 4.7.0
EXTENSION=.tar.xz

BASE_URL = https://ftp.gnu.org/gnu/findutils

ifneq ($(BUILD_PHASE),Final)
CONFIG_OPTS += --prefix=/tools
else
CONFIG_OPTS += --prefix=$(PKG_DIR) \
	      --libexecdir=/usr/lib/findutils \
	      --localstatedir=/var/lib/locate
endif


include ../Makefile.rules
