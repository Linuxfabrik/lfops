source /tmp/lib.sh

if [ $(grep /systemd-sulogin-shell /usr/lib/systemd/system/rescue.service | wc -l) -eq 0 ]; then exit $FAIL; fi
if [ $(grep /systemd-sulogin-shell /usr/lib/systemd/system/emergency.service | wc -l) -eq 0 ]; then exit $FAIL; fi
exit $PASS
