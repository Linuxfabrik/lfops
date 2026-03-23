source /tmp/lib.sh

check_login_banner /etc/issue.net && exit $PASS || exit $FAIL
