# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = automake
VERSION = 1.16.1

BASE_URL = https://ftp.gnu.org/gnu/automake

# Tool Chain Build Stage_3
#
ifeq ($(BUILD_PHASE), Stage_3)
CONFIG_OPTS += --enable-install-program=hostname
endif # Stage 3

# # Final Build
#

include ../Makefile.rules
