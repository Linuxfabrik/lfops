source /tmp/lib.sh

if [ $(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep clientalivecountmax | cut -d' ' -f2) -ne 0 ]; then exit $FAIL; fi
exit $PASS
