source /tmp/lib.sh

if [ "$(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep ignorerhosts | cut -d' ' -f2)" == 'yes' ]; then exit $PASS; fi
exit $FAIL
