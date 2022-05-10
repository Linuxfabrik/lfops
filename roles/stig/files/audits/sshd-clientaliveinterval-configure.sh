source /tmp/lib.sh

clientaliveinterval=$(sshd -T -C user=root -C host="$(hostname)" -C addr="$(grep $(hostname) /etc/hosts | awk '{print $1}')" | grep clientaliveinterval | cut -d' ' -f2)
if [ $clientaliveinterval -lt 1 -o $clientaliveinterval -gt 900 ]; then exit $FAIL; fi
