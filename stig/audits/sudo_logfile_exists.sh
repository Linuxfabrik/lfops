source /tmp/lib.sh

grep -rPsiq -- '^\h*Defaults\h+([^#]+,\h*)?logfile\h*=\h*(\"|\')?\H+(\"|\')?(,\h*\H+\h*)*\h*(#.*)?$' /etc/sudoers* 2>/dev/null || exit $FAIL

exit $PASS