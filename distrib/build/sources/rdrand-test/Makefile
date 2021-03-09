# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = rdrand-test
VERSION = 
EXTENSION = .zip

BASE_URL = https://cdn.arstechnica.net/wp-content/uploads/2019/10/
DOWNLOAD = yes
COMPILE = yes
INSTALL = yes

download:
	wget $(BASE_URL)$(PACKAGE)$(EXTENSION) -O $(DOWNLOADS_DIR)/$(PACKAGE)$(EXTENSION)
	

compile:
	unzip -b $(DOWNLOADS_DIR)/$(PACKAGE)$(EXTENSION) -d sources/coretree/tree/var/smoothwall/rdrand-test -x *.c
	
install:
	@true
	
include ../Makefile.rules
