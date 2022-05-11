source /tmp/lib.sh

if [ -z "$(grep -E 'kernelopts=(\S+\s+)*audit_backlog_limit=\S+\b' /boot/grub2/grubenv)" ]; then exit $FAIL; fi
if [ $(auditctl -s | grep backlog_limit | cut -d' ' -f2) -lt 8192 ]; then exit $FAIL; fi
exit $PASS
