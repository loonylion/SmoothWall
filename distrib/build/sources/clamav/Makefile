include ../Makefile.conf

PACKAGE = clamav
VERSION = 0.103.0

BASE_URL = https://www.clamav.net/downloads/production

# The --disable-clamav switch disables the check for existence of the clamav user and group 
#    but clamscan would still require an unprivileged account to work in a superuser mode.

PRE_CONFIGURE = LIBS=-ltinfo
CONFIG_OPTS += --sysconfdir=/usr/lib/smoothwall --with-dbdir=/var/clamav --disable-clamav --disable-ltdl-install --without-included-ltdl

#PATCH_FILE1 = clamav-pidperms.patch

INSTALL = yes

install: compile
	@mkdir -p $(PKG_ROOT)
	@mkdir -p $(PKG_ROOT)/var/clamav
	@make -C $(COMPILE_DIR) DESTDIR=$(PKG_ROOT) install
	@chown -R 105:105 $(PKG_ROOT)/var/clamav
	@rm -f $(PKG_ROOT)/usr/lib/smoothwall/clamd.conf
	@rm -f $(PKG_ROOT)/usr/lib/smoothwall/freshclam.conf

include ../Makefile.rules
