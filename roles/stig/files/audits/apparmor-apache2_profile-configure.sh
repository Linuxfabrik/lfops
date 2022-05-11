source /tmp/lib.sh

if is_not_installed 'apparmor'; then exit $SKIP; fi
exit $REV
