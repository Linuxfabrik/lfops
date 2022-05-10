source /tmp/lib.sh

if [ $(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep -i maxsessions | cut -d' ' -f2) -le 10 ]; then exit $PASS; fi
exit $FAIL
