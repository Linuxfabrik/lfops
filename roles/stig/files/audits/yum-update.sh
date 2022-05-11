source /tmp/lib.sh

if [ $(yum check-update &>/dev/null; echo $?) -eq 0 ]; then exit $PASS; fi
exit $REV
