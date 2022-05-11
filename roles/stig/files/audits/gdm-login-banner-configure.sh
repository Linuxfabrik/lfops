source /tmp/lib.sh

if is_not_installed 'gdm'; then exit $SKIP; fi
if [ ! -f /etc/dconf/profile/gdm ]; then exit $FAIL; fi
if [ ! -d /etc/dconf/db/gdm.d ]; then exit $FAIL; fi
gdm_file='/etc/dconf/db/gdm.d/01-banner-message'
if [ ! -f $gdm_file ]; then exit $FAIL; fi
if [ -z "$(grep -E '^banner-message-enable\s*=\s*true' $gdm_file 2> /dev/null)" ]; then exit $FAIL; fi
if [ -z "$(grep -E '^banner-message-text\s*=.*' $gdm_file 2> /dev/null)" ]; then exit $FAIL; fi
exit $PASS
