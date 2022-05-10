source /tmp/lib.sh

if [ "$(sysctl net.ipv4.ip_forward 2> /dev/null)" != 'net.ipv4.ip_forward = 0' ]; then exit $FAIL; fi
# if [ -n "$(grep -E -s "^\s*net\.ipv4\.ip_forward\s*=\s*1" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" ]; then exit $FAIL; fi
exit $PASS
