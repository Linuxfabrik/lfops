source /tmp/lib.sh

if [ $(grep -Ei '^\s*Defaults\s+([^#]+,\s*)?logfile=' /etc/sudoers /etc/sudoers.d/* 2>/dev/null | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
