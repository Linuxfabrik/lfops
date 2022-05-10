source /tmp/lib.sh

loglevel=$(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep loglevel | cut -d' ' -f2)
if [ "$loglevel" == 'INFO' -o "$loglevel" == 'VERBOSE' ]; then exit $PASS; fi
exit $FAIL
