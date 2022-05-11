source /tmp/lib.sh

if [ "$(sysctl net.ipv4.icmp_ignore_bogus_error_responses 2> /dev/null)" != 'net.ipv4.icmp_ignore_bogus_error_responses = 1' ]; then exit $FAIL; fi
# if [ -n "$(grep -E -s "^\s*net\.ipv4\.icmp_ignore_bogus_error_responses\s*=\s*0" /etc/sysctl.conf /etc/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /run/sysctl.d/*.conf 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" ]; then exit $FAIL; fi
exit $PASS
