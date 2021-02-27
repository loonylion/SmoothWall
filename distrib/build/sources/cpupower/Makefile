# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = SWE_cpupower
VERSION = 4.19.170

#BASE_URL = https://github.com/13-37-org/infnoise/releases/tag/$(VERSION)
BASE_URL = http://www.miscstuff.org/swe/buildmirror/3.2
#export NO_CHECK_CERT = 1

#CONFIG_OPTS += --without-pam
ARCH=i386
ifeq ($(mARCH),x86_64)
ARCH=amd64
endif


DOWNLOAD=yes
COMPILE=yes
INSTALL=yes

download:
	wget $(BASE_URL)/$(PACKAGE)_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/$(PACKAGE)_$(VERSION)_$(ARCH).tar.xz
	touch $(DOWNLOADS_DIR)/$(PACKAGE)_$(VERSION)_$(ARCH).tar.xz.done
	#wget $(BASE_URL)/$(PACKAGE)-tools_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/$(PACKAGE)-tools_$(VERSION)_$(ARCH).tar.xz
	#wget $(BASE_URL)/infnoise-tools_$(VERSION)_$(ARCH).deb -O $(DOWNLOADS_DIR)/infnoise-tools_$(VERSION)_$(ARCH).deb
	
	#touch $(DOWNLOADS_DIR)/$(PACKAGE)-tools_$(VERSION)_$(ARCH).tar.xz.done
	
	wget $(BASE_URL)/SWE_libcpupower1_$(VERSION)_$(ARCH).tar.xz -O $(DOWNLOADS_DIR)/SWE_libcpupower_$(VERSION)_$(ARCH).tar.xz
	touch $(DOWNLOADS_DIR)/libcpupower1_$(VERSION)_$(ARCH).tar.xz.done

compile:
	@true

install:
	tar -xJf $(DOWNLOADS_DIR)/$(PACKAGE)_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	#rm -rf $(PKG_ROOT)/lib/systemd/system/infnoise.service
	tar -xJf $(DOWNLOADS_DIR)/SWE_libcpupower_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	#tar -xJf $(DOWNLOADS_DIR)/$(PACKAGE)-tools_$(VERSION)_$(ARCH).tar.xz -C $(PKG_ROOT)
	#rmdir $(PKG_ROOT)/lib/systemd/system $(PKG_ROOT)/lib/systemd
	#sed "s|,TAG+=\"systemd\", ENV{SYSTEMD_WANTS}=\"infnoise.service\"||" -i $(PKG_ROOT)/etc/udev/rules.d/75-infnoise.rules
#@true

include ../Makefile.rules
