source /tmp/lib.sh

# check for UEFI first - if so, skip.
if [ -d /sys/firmware/efi ]; then
    exit $REV
fi
if is_active_kernelmod 'vfat'; then exit $FAIL; fi
exit $PASS
