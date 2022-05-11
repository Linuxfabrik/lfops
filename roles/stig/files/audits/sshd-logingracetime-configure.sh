source /tmp/lib.sh

logingracetime=$(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep logingracetime | cut -d' ' -f2)
if [ $logingracetime -ge 1 -a $logingracetime -le 60 ]; then exit $PASS; fi
exit $FAIL
