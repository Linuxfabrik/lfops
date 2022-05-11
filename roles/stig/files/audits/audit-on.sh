source /tmp/lib.sh

# /boot/grub2/grubenv is available in BIOS and UEFI boot mode
if [ -z "$(grep -E 'kernelopts=(\S+\s+)*audit=1\b' /boot/grub2/grubenv)" ]; then exit $FAIL; fi
exit $PASS
