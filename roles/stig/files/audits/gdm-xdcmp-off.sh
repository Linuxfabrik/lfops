source /tmp/lib.sh

if is_not_installed 'gdm'; then exit $SKIP; fi
if grep -Eis '^\s*Enable\s*=\s*true' /etc/gdm/custom.conf &>/dev/null; then exit $FAIL; fi
exit $PASS
