source /tmp/lib.sh

if [ $(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep maxauthtries | cut -d' ' -f2) -le 4 ]; then exit $PASS; fi
exit $FAIL
