# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

OPENSSL_VER = 1.1.1b

PACKAGE = openssl
VERSION = $(OPENSSL_VER)

#BASE_URL = http://www.openssl.org/source/
BASE_URL = https://www.openssl.org/source/old/1.1.1

# If building for 486, generate only 386 code. Otherwise, building
#   'modern' code should be OK.
ifeq ($(mARCH),i486)
ONLY386 = 386
endif

PLATFORM = generic32
ifeq ($(mARCH),x86_64)
PLATFORM = x86_64
endif

PREFIX = /build/buildroot/ssl

OPENSSLDIR = $(PKG_DIR)/lib/ssl


CONFIGURE = yes
COMPILE = yes
INSTALL = yes
CLEAN = yes

configure: $(DIR)/
	@echo; echo; echo "configure"; echo
	sed -i -e '/^  \*86-\*-linux2/i \
  FUBAR\
\toptions="$$options $(CFLAGS)";;' $(DIR)/config
	sed -i -e '/^  \*86-\*-linux2/,+11d' $(DIR)/config
	sed -i -e 's/  FUBAR$$/  *86-*-linux2) OUT="linux-elf"/' $(DIR)/config
	#echo $(PWD)
	#echo $(mTUPLE)
	@(cd $(DIR); \
	  ./Configure linux-$(PLATFORM) -no-ssl3 -no-idea shared --prefix=$(PKG_DIR) --libdir=lib --openssldir=$(OPENSSLDIR));

compile: configure
	@echo; echo; echo "compile"; echo
	+@$(MAKE) $(JOBS) -C $(PACKAGE)-$(VERSION)

install: compile
	@echo; echo; echo "install"; echo
	@mkdir -p $(PKG_ROOT)
	sed "s|DESTDIR=|DESTDIR=$(PKG_ROOT)|" -i $(DIR)/Makefile
	make -C $(PACKAGE)-$(OPENSSL_VER) INSTALL_PREFIX=$(PKG_ROOT) install

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)
ifeq ($(BUILD_PHASE), Final)
	@rm -rf $(PKG_ROOT); mkdir -p $(PKG_ROOT)
ifeq ($(BITS_64), yes)
	mkdir -p $(PKG_ROOT)/{lib,usr/lib}
	@cd $(PKG_ROOT); ln -s lib lib64
	@cd $(PKG_ROOT)/usr; ln -s lib lib64
endif
	@rm -f $(TARGET_DIR)/smoothwall-$(PACKAGE).tar.gz
endif

include ../Makefile.rules
