# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2010
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = httpd
VERSION = 2.4.39
APR_VER = 1.6.2
UTIL_VER = 1.6.1

LICENCE_FILE = $(DIR)/COPYING

BASE_URL = http://archive.apache.org/dist/httpd/
APR_URL = http://archive.apache.org/dist/apr/

CONFIG_OPTS += --enable-ssl --with-ssl=/usr \
	--with-included-apr --enable-mods-shared=all --enable-layout=RedHat

CONFIGURE = yes
INSTALL = yes

configure: patch
	wget $(APR_URL)apr-$(APR_VER).tar.gz -O ./$(DIR)/srclib/apr-$(APR_VER).tar.gz
	tar -xzf $(DIR)/srclib/apr-$(APR_VER).tar.gz -C $(DIR)/srclib/
	wget $(APR_URL)apr-util-$(UTIL_VER).tar.bz2 -O ./$(DIR)/srclib/apr-util-$(UTIL_VER).tar.bz2
	tar -xjf $(DIR)/srclib/apr-util-$(UTIL_VER).tar.bz2 -C $(DIR)/srclib
	mv $(DIR)/srclib/apr-$(APR_VER)	$(DIR)/srclib/apr
	mv $(DIR)/srclib/apr-util-$(UTIL_VER) $(DIR)/srclib/apr-util
	@(cd $(DIR); ./configure $(CONFIG_OPTS) --prefix=$(PKG_DIR))

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(DIR) DESTDIR=$(PKG_ROOT) install
	@rm -rf $(PKG_ROOT)/{etc,var}

include ../Makefile.rules
