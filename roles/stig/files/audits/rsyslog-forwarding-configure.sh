source /tmp/lib.sh

if [ -e /etc/rsyslog.conf ]; then
    # old rsyslog syntax:
    if [ $(grep --only-matching '^\*\.\*[^I]*@' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2> /dev/null | wc -l) -gt 0 ]; then exit $PASS; fi
    # new rsyslog syntax:
    if [ $(grep --only-matching --ignore-case '^\*\.\*action\.\*omfwd\.\*target' /etc/rsyslog.conf /etc/rsyslog.d/*.conf 2> /dev/null | wc -l) -gt 0 ]; then exit $PASS; fi
fi
exit $FAIL
