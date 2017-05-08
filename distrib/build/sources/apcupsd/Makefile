# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = apcupsd
VERSION = 3.14.14

BASE_URL = http://downloads.sourceforge.net/project/$(PACKAGE)/$(PACKAGE)%20-%20Stable/$(VERSION)

CONFIG_OPTS = --enable-usb

COMPILE = yes
compile: configure
	+$(PRE_COMPILE) $(MAKE) ${JOBS} -C $(COMPILE_DIR) VERBOSE=1

include ../Makefile.rules
