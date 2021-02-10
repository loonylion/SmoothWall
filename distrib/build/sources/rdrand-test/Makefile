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
	wget $(BASE_URL)$(PACKAGE)$(EXTENSION) -O $(PACKAGE)$(EXTENSION)

compile:
	#mv $(DOWNLOADS_DIR)/download_file?file_path=%2Fookla-speedtest-1.0.0-x86_64-linux ($(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tgz
	@true
	
install:
	#mkdir -p $(PKG_ROOT)/usr/bin
	#mv speedtest $(PKG_ROOT)/usr/bin
	@true
	
include ../Makefile.rules
