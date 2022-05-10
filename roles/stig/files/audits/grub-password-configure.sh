source /tmp/lib.sh

if [ $(grep "^\s*GRUB2_PASSWORD=" /boot/grub2/user.cfg /etc/grub.d/* 2> /dev/null | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
