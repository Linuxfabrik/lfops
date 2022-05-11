source /tmp/lib.sh

if [ "$(sysctl net.ipv4.conf.all.rp_filter 2> /dev/null)" != 'net.ipv4.conf.all.rp_filter = 1' ]; then exit $FAIL; fi
if [ "$(sysctl net.ipv4.conf.default.rp_filter 2> /dev/null)" != 'net.ipv4.conf.default.rp_filter = 1' ]; then exit $FAIL; fi
# if [ -n "$(grep -E -s "^\s*net\.ipv4\.conf\.all\.rp_filter\s*=\s*0" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" ]; then exit $FAIL; fi
# if [ "$(grep -E -s "^\s*net\.ipv4\.conf\.default\.rp_filter\s*=\s*1" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.default.rp_filter=1' ]; then exit $FAIL; fi
exit $PASS
