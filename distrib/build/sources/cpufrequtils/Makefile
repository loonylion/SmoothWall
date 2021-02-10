# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = cpufrequtils
VERSION = 008

BASE_URL = http://ftp.be.debian.org/pub/linux/utils/kernel/cpufreq

#PRE_CONFIGURE = CFLAGS="-Wno-error $(CFLAGS)"

CONFIGURE = yes
INSTALL = yes

configure: 
	tar -xzf ../../downloads/cpufrequtils-$(VERSION).tar.gz
install: compile
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/lib
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/bin
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/man
	@mkdir -p $(PKG_ROOT)$(PKG_DIR)/include
	@install -D $(COMPILE_DIR)/libcpufreq.so* $(PKG_ROOT)$(PKG_DIR)/lib/
	#@install -m 644 -D $(COMPILE_DIR)/lib/libcpufreq.h $(PKG_ROOT)$(PKG_DIR)/include/
	@install -m 644 -D $(COMPILE_DIR)/man/cpufreq-set.1 $(PKG_ROOT)$(PKG_DIR)/man/
	@install -m 644 -D $(COMPILE_DIR)/man/cpufreq-info.1 $(PKG_ROOT)$(PKG_DIR)/man/
	@install -D $(COMPILE_DIR)/cpufreq-set $(PKG_ROOT)$(PKG_DIR)/bin/
	@install -D $(COMPILE_DIR)/cpufreq-info $(PKG_ROOT)$(PKG_DIR)/bin/
	@install -D $(COMPILE_DIR)/cpufreq-aperf $(PKG_ROOT)$(PKG_DIR)/bin/
	#chmod 644 $(PKG_ROOT)$(PKG_DIR)/lib/libcpufreq.h
	chmod 644 $(PKG_ROOT)$(PKG_DIR)/man/cpufreq-set.1
	chmod 644 $(PKG_ROOT)$(PKG_DIR)/man/cpufreq-info.1
	
include ../Makefile.rules
