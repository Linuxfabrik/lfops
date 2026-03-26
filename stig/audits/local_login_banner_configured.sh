source /tmp/lib.sh

check_login_banner /etc/issue && exit $PASS || exit $FAIL
