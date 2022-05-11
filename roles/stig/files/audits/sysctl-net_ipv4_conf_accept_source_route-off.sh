source /tmp/lib.sh

if [ "$(sysctl net.ipv4.conf.all.accept_source_route 2> /dev/null)" != 'net.ipv4.conf.all.accept_source_route = 0' ]; then exit $FAIL; fi
if [ "$(sysctl net.ipv4.conf.default.accept_source_route 2> /dev/null)" != 'net.ipv4.conf.default.accept_source_route = 0' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.all\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.all.accept_source_route=0' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.default\.accept_source_route" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.default.accept_source_route=0' ]; then exit $FAIL; fi
exit $PASS
