# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = ookla-speedtest
VERSION = 1.0.0-$(mARCH)-linux
EXTENSION = .tgz

BASE_URL = https://bintray.com/ookla/download/download_file?file_path=
#export NO_CHECK_CERT = 1

#CONFIG_OPTS += --without-pam
DOWNLOAD=yes
COMPILE = yes
INSTALL = yes

download:
	wget $(BASE_URL)$(PACKAGE)-$(VERSION)$(EXTENSION) -O $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION)
	touch $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION).done

compile:
	
	#mv $(DOWNLOADS_DIR)/download_file?file_path=%2Fookla-speedtest-1.0.0-x86_64-linux ($(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION).tgz
	@true
	
install:
	tar -xzvf $(DOWNLOADS_DIR)/$(PACKAGE)-$(VERSION)$(EXTENSION) -C $(PKG_ROOT)
	echo $(PKG_ROOT)
	echo $(PWD)
	mkdir -p $(PKG_ROOT)/usr/bin
	mv $(PKG_ROOT)/speedtest $(PKG_ROOT)/usr/bin
	mkdir -p $(PKG_ROOT)/usr/share/man/man5
	mv $(PKG_ROOT)/speedtest.5 $(PKG_ROOT)/usr/share/man/man5
	mkdir -p $(PKG_ROOT)/usr/share/doc
	mv $(PKG_ROOT)/speedtest.md $(PKG_ROOT)/usr/share/doc
	
include ../Makefile.rules
