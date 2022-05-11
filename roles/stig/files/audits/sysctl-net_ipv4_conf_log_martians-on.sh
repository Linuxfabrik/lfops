source /tmp/lib.sh

if [ "$(sysctl net.ipv4.conf.all.log_martians 2> /dev/null)" != 'net.ipv4.conf.all.log_martians = 1' ]; then exit $FAIL; fi
if [ "$(sysctl net.ipv4.conf.default.log_martians 2> /dev/null)" != 'net.ipv4.conf.default.log_martians = 1' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.all\.log_martians" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.all.log_martians=1' ]; then exit $FAIL; fi
# if [ "$(grep "^net\.ipv4\.conf\.default\.log_martians" /etc/sysctl.conf /etc/sysctl.d/* 2> /dev/null | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'net.ipv4.conf.default.log_martians=1' ]; then exit $FAIL; fi
exit $PASS
