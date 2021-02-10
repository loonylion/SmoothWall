# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = haveged
VERSION = 1.9.14

BASE_URL = https://github.com/jirka-h/haveged/archive/

DOWNLOAD = yes

download:
	wget $(BASE_URL)/v$(VERSION).tar.gz -O $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz
	touch $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tar.gz.done
include ../Makefile.rules
