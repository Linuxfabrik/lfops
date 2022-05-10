source /tmp/lib.sh

# checking for xorg-x11-server-common instead of xorg-x11-*, as any gui will need this but there are other harmless xorg-x11-* packages
if is_installed 'xorg-x11-server-common'; then exit $FAIL; fi
exit $PASS
