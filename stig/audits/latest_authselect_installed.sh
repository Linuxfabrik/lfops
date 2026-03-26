source /tmp/lib.sh

rpm_version_gte "authselect" "0" "1.2.6" "2" && exit $PASS || exit $FAIL
