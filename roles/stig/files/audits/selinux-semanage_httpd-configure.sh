source /tmp/lib.sh

if [ "$(getenforce)" == 'Disabled' ]; then exit $SKIP; fi
# needs semanage from the policycoreutils-python-utils (RHEL 8+) or policycoreutils-python (up to RHEL 7)
if [ ! command -v semanage &> /dev/null ]; then exit $SKIP; fi
if [ "$(semodule --list-modules | grep permissive_httpd_t)" == "" ]; then exit $PASS; fi
exit $FAIL
