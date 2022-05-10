source /tmp/lib.sh

if [ -n "$(grep -E "^\s*kernelopts=(\S+\s+)*ipv6\.disable=1\b\s*(\S+\s*)*$" /boot/grub2/grubenv)" ]; then exit $PASS; fi
exit $FAIL
