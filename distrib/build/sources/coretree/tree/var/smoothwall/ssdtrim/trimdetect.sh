#!/bin/bash
#trimdetect.sh
#attempts to detect SSDs with Trim support
dscgran=`lsblk -lD | awk 'BEGIN{min=2;max=2} {if (NR>=min){if (NR<=max){ {print $3} }}}' | cut -c1`
dscmax=`lsblk -lD | awk 'BEGIN{min=2;max=2} {if (NR>=min){if (NR<=max){ {print $4} }}}' | cut -c1`

if [$(dscmax) > 0]
	then
		if [-f /var/smoothwall/ssdtrim/supported]
			exit 0;
		else
			touch /var/smoothwall/ssdtrim/supported
		fi
	elseif [ -f /var/smoothwall/ssdtrim/supported]
		rm /var/smoothwall/ssdtrim/supported
	fi
fi
