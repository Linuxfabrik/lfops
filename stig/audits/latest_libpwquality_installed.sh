source /tmp/lib.sh

rpm_version_gte "libpwquality" "0" "1.4.4" "8" && exit $PASS || exit $FAIL
