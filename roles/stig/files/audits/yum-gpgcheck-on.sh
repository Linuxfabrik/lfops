source /tmp/lib.sh

if [ $(grep -Er ^gpgcheck.*=.*0 /etc/yum.conf /etc/dnf/dnf.conf /etc/yum.repos.d/ | wc -l) -ne 0 ]; then exit $FAIL; fi
exit $PASS
