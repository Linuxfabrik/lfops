source /tmp/lib.sh

if [ -n "$(grep -E 'kernelopts=(\S+\s+)*(selinux=0|enforcing=0)+\b' /boot/grub2/grubenv)" ]; then exit $FAIL; fi
exit $PASS
