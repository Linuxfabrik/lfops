source /tmp/lib.sh

if [ "$(sysctl net.ipv4.conf.all.accept_redirects 2> /dev/null)" != 'net.ipv4.conf.all.accept_redirects = 0' ]; then exit $FAIL; fi
if [ "$(sysctl net.ipv4.conf.default.accept_redirects 2> /dev/null)" != 'net.ipv4.conf.default.accept_redirects = 0' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.all\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.all.accept_redirects=0' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.default\.accept_redirects" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.default.accept_redirects=0' ]; then exit $FAIL; fi
exit $PASS
