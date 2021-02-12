# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../../Makefile.conf

PACKAGE = Geo-Ip-PurePerl
VERSION = 1.25

BASE_URL = http://search.cpan.org/CPAN/authors/id/B/BO/BORISZ/

CONFIGURE = yes
CLEAN = yes

configure: $(DIR)/
	@echo; echo "configure"
	cd $(DIR); perl Makefile.PL

clean:
	@echo -n " $(PACKAGE)"
	@rm -rf $(DIR)
	@rm -rf $(COMPILE_DIR)

include ../../../Makefile.rules
