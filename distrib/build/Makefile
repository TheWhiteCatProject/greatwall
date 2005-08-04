# Top level Makefile for SmoothWall Build system.

# Please set to working nameservers.  DNS_SERVER2 is optional
#DNS_SERVER1 = 192.168.0.254
DNS_SERVER1 = 192.168.72.253

default:
	@echo "Please use one of:"
	@echo
	@echo "build:            Primary build target.  You must know what you are doing!"
	@echo
	@echo "predownload:      Downloads sourcecode packages in advance."
	@echo
	@echo "packageinfos.html:Outputs HTML describing package names and URLs.  Please"
	@echo "                  call with -s switch to make."
	@echo
	@echo "clean-buildroot:  Empties the buildroot temp dir.  Generally harmless."
	@echo
	@echo "clean-target:     Removes all built package tarfiles."
	@echo
	@echo "clean-sources:    Does a 'make clean' in each source package dir."
	@echo
	@echo "clean-tools:      Removes everything in /tools.  Do not do this as the build"
	@echo "                  scripts use this for the shell."
	@echo
	@echo "clean-distrib:    Removes everything in the above dir, except the build"
	@echo "                  and tools directories."

build:
	@DNS_SERVER1=$(DNS_SERVER1) DNS_SERVER2=$(DNS_SERVER2) ./makebuild1

predownload:
	@(cd sources; for I in `find  -type d -maxdepth 3 -mindepth 1`; do \
		if [ "$$I" != "./CVS" ]; then \
			make -C $$I BUILDENV=1 -n download >/dev/null 2>/dev/null; \
			if [ $$? -eq 0 ]; then \
				make -C $$I BUILDENV=1 download; \
				if [ $$? -ne 0 ]; then \
					echo "Oops"; \
					exit; \
				fi \
			fi \
		fi \
	done);

packageinfos.html:
	@echo "<ul>" >/tmp/packageinfo.html
	-(cd sources; for I in `find -type d -maxdepth 1 -mindepth 1`; do \
		if [ "$$I" != "CVS" ]; then \
			make -C $$I packageinfo.html; \
		fi \
	done);
	-make -C sources/modules packageinfos.html
	@echo "</ul>" >>/tmp/packageinfo.html
	
clean-buildroot:
	@rm -rf buildroot/*

clean-target:
	@rm -rf target/*
	
clean-sources:
	@(cd sources; for I in `find -type d -maxdepth 1 -mindepth 1`; do \
		if [ "$$I" != "CVS" ]; then \
			make -C $$I clean; \
		fi \
	done);

clean-tools:
	@rm -rf ../tools/*

clean-distrib:
	@(cd ..; \
	umount proc; \
	rm -rf bin etc lib proc sbin var boot dev home opt root tmp usr);

clean:
	@echo "No general 'clean' target. Type 'make' with no target for info."
	