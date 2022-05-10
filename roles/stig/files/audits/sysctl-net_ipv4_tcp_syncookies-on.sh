source /tmp/lib.sh

if [ "$(sysctl net.ipv4.tcp_syncookies 2> /dev/null)" != 'net.ipv4.tcp_syncookies = 1' ]; then exit $FAIL; fi
# if [ -n "$(grep -E -r "^\s*net\.ipv4\.tcp_syncookies\s*=\s*[02]" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" ]; then exit $FAIL; fi
exit $PASS
