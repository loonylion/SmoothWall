# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../../Makefile
include ../../Makefile.conf
include ../../Makefile.versions

RUNTIME_ROOT = runtimeroot

SWE_PKGS = busybox eudev kmod pciutils bash util-linux \
	   sysfsutils parted readline inotify-tools mtools device-ids kbd kernel-drivers \
	   e2fsprogs zlib xz module-init-tools sysvinit libelf linux-firmware $(GRUB)


# Stuff that shouldn't be needed in the initramfs, drivers/gpio net/bluetooth
# some net drivers removed: >10gbit, wlan,bluetooth,wimax, some chelsio 10gbit removed because theres no firmware so they wont work
NOT_DRIVERS = drivers/gpu drivers/parport drivers/scsi/fcoe \
	      drivers/scsi/fnic drivers/scsi/osd drivers/scsi/libfc \
	      drivers/scsi/cxgbi drivers/scsi/be2iscsi drivers/scsi/bfa \
	      drivers/scsi/lpfc drivers/hwmon drivers/media \
	      drivers/watchdog drivers/edac drivers/regulator \
	      drivers/video net/netfilter net/ipsec \
	      net/sched net/sctp net/bluetooth \
	      net/ax25 net/wimax net/cfrm drivers/accessibility drivers/android drivers/auxdisplay drivers/fpga drivers/gnss drivers/nfc drivers/pcmcia drivers/atm drivers/infiniband drivers/scsi/pcmcia drivers/macintosh drivers/staging/android drivers/staging/media drivers/staging/xgifb drivers/input/joystick drivers/input/tablet drivers/input/touchscreen drivers/input/mouse drivers/input/gameport net/appletalk net/batman-adv net/bpfilter net/6lowpan net/decnet net/nfc net/x25 net/9p net/dccp net/rose net/rds net/dsa drivers/isdn drivers/net/hamradio drivers/net/wimax drivers/w1 sound drivers/net/ethernet/mellanox/mlx5 drivers/net/ethernet/mellanox/mlxsw drivers/net/ethernet/intel/i40e drivers/net/ethernet/chelsio/cxgb4 drivers/net/ethernet/chelsio/cxgb4vf net drivers/firewire fs/ntfs fs/xfs drivers/leds drivers/cpufreq

#these are mostly wifi, but theres a few completely unrelated/unnecessary stuff as well: korg, yamaha, ess, emi* are soundcards, cis are pcmcia cards, ql2*_fw.bin files are for a qlogic fibre channel controller. Wired nic firmware are also removed. most of what's left is either storage controller, usb or serial device firmware or cpu microcode
NOT_FIRMWARE = yamaha korg libertas rtlwifi iwlwifi*.ucode ess emi26 emi62 mrvl rtw88 cis rt*.bin brcm ti-connectivity ar3k ath6k ath10k ath11k ar5523.bin carl9170.fw wsm_22.bin wil6210.* agere_*_fw.bin cbfw-3.2.5.1.bin ctfw-3.2.5.1.bin ct2fw-3.2.5.1.bin mt7601u.bin mt7662* mediatek ositech mwl8k ql2*_fw.bin liquidio qed rtl-nic 3com bnx2 bnx2x cadence cavium e100 mellanox tigon myricom netronome kaweth acenic mts_*.fw bnx2x*.fw myri10ge_*.dat phantfw.bin slicoss

NOT_SHARE = locales/[a-d]* locales/e[o-z]* locales/[e-z]* doc info man readline
NOT_USR = include info man


ROOTDIRS = cdrom dev etc harddisk proc sys tmp usr run

root:
	@echo "        Make root directories" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nMake root directories"
	for i in $(ROOTDIRS); do mkdir -vp tmp/$$i; done

bin:
	@echo; echo; echo "bin"
	mkdir -vp tmp/bin tmp/lib tmp/usr/lib/klibc/bin
	mkdir -vp tmp/sbin
	cp -aR /sbin/* tmp/bin
ifeq ($(mTUPLE),$(filter $(mTUPLE),pi0w rpi2 rpi3))
# strip:tmp/bin/fake-hwclock: File format not recognized
	rm -v tmp/bin/fake-hwclock
endif
	strip tmp/bin/*

lib:
	@echo -e "\n\nlib"
	@echo "        Unpack Linux" >>$(MEDIA_BUILD_OUT)
	@echo -e "\nUnpack Linux"
	tar xfz /build/target/smoothwall-linux$(KERNEL_TYPE).tar.gz -C tmp ./lib/modules
	@echo "        Copy glibc libraries" >>$(MEDIA_BUILD_OUT)
	@echo -e "\nCopy glibc files"
	#cp -avR /lib/lib* tmp/lib
	cp -avR /build/buildroot/glibc/lib/lib* tmp/lib
	cp -aR /usr/lib/libncurses.so* tmp/lib/
	cp -aR /usr/lib/libtinfo.so* tmp/lib/

klibc:
	@echo "        Copy klibc" >>$(MEDIA_BUILD_OUT)
	@echo; echo; echo "klibc"
	mkdir -vp tmp/usr/lib/klibc/bin
	cp -aR /build/buildroot/klibc/usr/lib/klibc/lib/klibc-*.so tmp/lib
	cp -aR /build/buildroot/klibc/usr/lib/klibc/bin tmp/usr/lib/klibc/
	cp -aR /build/buildroot/klibc/usr/lib/klibc/lib tmp/usr/lib/klibc/

# klibc bin

all: clean root lib klibc
	@echo "        Setup SmoothWall" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nSetup SmoothWall"
	(cd tmp; \
	  cp -aR ../../../coretree/tree/etc/passwd etc; \
	  cp -aR ../../../coretree/tree/etc/group etc; \
	  install -D /usr/share/terminfo/l/linux usr/share/terminfo/l/linux; \
	  cp -aR /lib/ld-*.so /lib/ld-*.so.* /lib/libc-*.so /lib/libc.so.* lib; \
	  cp -aR ../etc/fstab etc; \
	  cp -aR ../etc/mtab etc; \
	  cp -aR ../etc/shells etc; \
	  cp -aR ../etc/termcap etc; \
	  cp -aR ../etc/udev-trigger.rc etc; chmod 755 etc/udev-trigger.rc; \
	  cp -aR ../etc/halt etc; chmod 755 etc/halt; \
	)

	@echo "        Install our programs" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nInstall our programs"
	for i in $(SWE_PKGS); do \
	  echo $$i; \
	  tar xfz /build/target/smoothwall-$$i.tar.gz -C tmp/; \
	done

	@echo -e "\n\nSome other"
	@echo "        Create /etc/ld.so.conf and link init" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nCreate /etc/ld.so.conf"; echo
	touch tmp/etc/ld.so.conf
	cd tmp; /sbin/ldconfig -r .


	@echo "        Copy runtime init" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nCopy runtime init"
	cd tmp; cp -v ../etc/runt-init init; chmod 555 init

	  #mknod -m0666 lib/udev/devices/null c 1 3; \
	  #ln -sf proc/kcore /lib/udev/devices/core; \
	  #ln -sf proc/self/fd /lib/udev/devices/fd; \
	  #ln -sf proc/self/fd/0 /lib/udev/devices/stdin; \
	  #ln -sf proc/self/fd/1 /lib/udev/devices/stdout; \
	  #ln -sf proc/self/fd/2 /lib/udev/devices/stderr; \
	#

#	cd tmp; [ -L sbin ] || (mv sbin/* bin; rmdir sbin; ln -s bin sbin)
#	cd tmp/usr; [ -L sbin ] || (mv sbin/* bin; rmdir sbin; ln -s bin sbin)

ifeq ($(BITS_64), yes)
	cd tmp; [ -e lib64 ] || ln -s lib lib64
	cd tmp/usr; [ -e lib64 ] || ln -s lib lib64
endif

	@touch tmp/cdrominstall

	@echo "        Striptree" >>$(MEDIA_BUILD_OUT)
	@echo -e "\n\nStriptree"; echo
	@/build/toolcrib/striptree tmp

# Clean extra stuff to shrink the initramfs
	@echo "        Clean to shrink the initramfs" >>$(MEDIA_BUILD_OUT)
	@echo; echo; echo "Clean extra stuff to shrink the initramfs"
	@for i in tmp/lib/modules/*; do (cd "$$i/kernel"; rm -rvf $(NOT_DRIVERS)); done
	@cd tmp/lib/firmware; rm -rvf $(NOT_FIRMWARE)
	@cd tmp/usr/share; rm -rf $(NOT_SHARE)
	@cd tmp/usr; rm -rf $(NOT_USR)
	@cd tmp; find . -name lib\*a -exec rm {} \;

# Build the runtime initramfs CPIO archive
	@echo "        Build the runtimeroot initramfs CPIO archive" >>$(MEDIA_BUILD_OUT)
	@echo; echo; echo "Build the runtimeroot initramfs CPIO archive"
	@cd tmp; find . | cpio -o -H newc | gzip > ../../$(RUNTIME_ROOT)image.gz

	@echo -e "runtimeroot build for $(KERNEL_TYPE) complete\n\n"

clean:
ifndef BUILD_PHASE
	@rm -rf $(RUNTIME_ROOT) tmp/
	@rm -f ../$(RUNTIME_ROOT)image.gz
	@rm -f $(RUNTIME_ROOT)image.gz
	@rm -rf runtimeroot/
else
	@echo "$(PACKAGE)"
	@echo; echo "runtimeroot clean"
	rm -rf $(RUNTIME_ROOT) tmp/
	rm -vf ../$(RUNTIME_ROOT)imag*
	rm -vf $(RUNTIME_ROOT)image.gz
	rm -vrf runtimeroot/
endif
