# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = infnoise-trng
VERSION = 0.3.1

#BASE_URL = https://github.com/13-37-org/infnoise/releases/tag/$(VERSION)
BASE_URL = http://www.miscstuff.org/swe/buildmirror/3.2
#export NO_CHECK_CERT = 1

#CONFIG_OPTS += --without-pam

ifeq ($(mARCH),x86_64)
ARCH=amd64
endif

DOWNLOAD=yes
COMPILE=yes
INSTALL=yes

download:
	wget $(BASE_URL)/SWE_infnoise_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/SWE_infnoise_$(VERSION)_$(ARCH).tar.xz
	touch $(DOWNLOADS_DIR)/infnoise_$(VERSION)_$(ARCH).tar.xz.done
	wget $(BASE_URL)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz
	#wget $(BASE_URL)/infnoise-tools_$(VERSION)_$(ARCH).deb -O $(DOWNLOADS_DIR)/infnoise-tools_$(VERSION)_$(ARCH).deb
	
	touch $(DOWNLOADS_DIR)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz.done
	
	wget $(BASE_URL)/SWE_libinfnoise_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/SWE_libinfnoise_$(VERSION)_$(ARCH).tar.xz
	touch $(DOWNLOADS_DIR)/libinfnoise_$(VERSION)_$(ARCH).tar.xz.done

compile:
	@true

install:
	#cp $(DOWNLOADS_DIR)/infnoise_$(VERSION)_$(ARCH).deb $(PKG_ROOT)/infnoise_$(VERSION)_$(ARCH).deb
	#cp $(DOWNLOADS_DIR)/infnoise-tools_$(VERSION)_$(ARCH).deb $(PKG_ROOT)/infnoise-tools_$(VERSION)_$(ARCH).deb
	#cp $(DOWNLOADS_DIR)/libinfnoise_$(VERSION)_$(ARCH).deb $(PKG_ROOT)/libinfnoise_$(VERSION)_$(ARCH).deb
	#OLDDIR=$(PWD)
	#cd $(PKG_ROOT)
	#ar -xvf $(PKG_ROOT)/infnoise_$(VERSION)_$(ARCH).deb 
	#mv $(PKG_ROOT)/data.tar.xz $(PKG_ROOT)/infnoise_$(VERSION)_$(ARCH).tar.xz
	#rm -f $(PKG_ROOT)/control.tar.gz
	#rm -f $(PKG_ROOT)/debian-binary
	#rm -f $(PKG_ROOT)/_gpgbuilder
	#ar -xvf $(PKG_ROOT)/infnoise-tools_$(VERSION)_$(ARCH).deb 
	#mv $(PKG_ROOT)/data.tar.xz $(PKG_ROOT)/infnoise-tools_$(VERSION)_$(ARCH).tar.xz
	#rm -f $(PKG_ROOT)/control.tar.gz
	#rm -f $(PKG_ROOT)/debian-binary
	#rm -f $(PKG_ROOT)/_gpgbuilder
	#ar -xvf $(PKG_ROOT)/libinfnoise_$(VERSION)_$(ARCH).deb 
	#mv $(PKG_ROOT)/data.tar.xz $(PKG_ROOT)/libinfnoise_$(VERSION)_$(ARCH).tar.xz
	#rm -f $(PKG_ROOT)/control.tar.gz
	#rm -f $(PKG_ROOT)/debian-binary
	#rm -f $(PKG_ROOT)/_gpgbuilder
	#cd $(OLDDIR)
	
	#cp $(DOWNLOADS_DIR)/SWE_infnoise_$(VERSION)_$(ARCH).tar.xz $(PKG_ROOT)/SWE_infnoise_$(VERSION)_$(ARCH).tar.xz
	#cp $(DOWNLOADS_DIR)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz $(PKG_ROOT)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz
	#cp $(DOWNLOADS_DIR)/SWE_libinfnoise_$(VERSION)_$(ARCH).tar.xz $(PKG_ROOT)/SWE_libinfnoise_$(VERSION)_$(ARCH).tar.xz
	tar -xJf $(DOWNLOADS_DIR)/SWE_infnoise_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	rm -rf $(PKG_ROOT)/lib/systemd/system/infnoise.service
	tar -xJf $(DOWNLOADS_DIR)/SWE_libinfnoise_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	tar -xJf $(DOWNLOADS_DIR)/SWE_infnoise-tools_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	rmdir $(PKG_ROOT)/lib/systemd/system $(PKG_ROOT)/lib/systemd
#@true

include ../Makefile.rules
