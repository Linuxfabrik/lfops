source /tmp/lib.sh

if [ $(dnf --quiet check-update &> /dev/null; echo $?) -eq 0 ]; then exit $PASS; fi
exit $FAIL
