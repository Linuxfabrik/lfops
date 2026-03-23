source /tmp/lib.sh

rpm_version_gte "pam" "0" "1.5.1" "19" && exit $PASS || exit $FAIL
