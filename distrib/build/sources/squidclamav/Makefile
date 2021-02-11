include ../Makefile.conf

PACKAGE = squidclamav
VERSION = 7.1

BASE_URL = https://sourceforge.net/projects/squidclamav/files/squidclamav/$(VERSION)

PRE_CONFIGURE = LIBS=-ltinfo

CONFIG_OPTS = --with-c-icap

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install

include ../Makefile.rules
