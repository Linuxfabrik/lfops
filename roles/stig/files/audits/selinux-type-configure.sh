source /tmp/lib.sh

if [ "$(grep -E --count '^SELINUXTYPE=(targeted|mls)\b' /etc/selinux/config)" -ne 1 ]; then exit $FAIL; fi
if [ "$(sestatus | awk '/Loaded policy name/ {print $4}')" != "targeted" ]; then exit $FAIL; fi
exit $PASS
