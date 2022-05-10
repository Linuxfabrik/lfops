source /tmp/lib.sh

if is_not_installed 'gdm'; then exit $SKIP; fi
if [ ! -f /etc/dconf/profile/gdm ]; then exit $FAIL; fi
if [ -z "$(grep -E '^user-db:user' /etc/dconf/profile/gdm 2> /dev/null)" ]; then exit $FAIL; fi
if [ -z "$(grep -E '^system-db:gdm' /etc/dconf/profile/gdm 2> /dev/null)" ]; then exit $FAIL; fi
if [ -z "$(grep -E '^file-db:/usr/share/gdm/greeter-dconf-defaults' /etc/dconf/profile/gdm 2> /dev/null)" ]; then exit $FAIL; fi
if [ ! -d /etc/dconf/db/gdm.d ]; then exit $FAIL; fi
gdm_file='/etc/dconf/db/gdm.d/00-login-screen'
if [ ! -f $gdm_file ]; then exit $FAIL; fi
if [ -z "$(grep -E '^\[org/gnome/login-screen\]' $gdm_file 2> /dev/null)" ]; then exit $FAIL; fi
if [ -z "$(grep -E '^disable-user-list\s*=\s*true' $gdm_file 2> /dev/null)" ]; then exit $FAIL; fi
exit $PASS
