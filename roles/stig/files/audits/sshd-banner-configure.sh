source /tmp/lib.sh

if [ "$(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep banner | cut -d' ' -f2)" == '/etc/issue.net' ]; then exit $PASS; fi
exit $FAIL
