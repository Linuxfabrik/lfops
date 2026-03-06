source /tmp/lib.sh

if find /etc/audit/ -type f \( -name '*.conf' -o -name '*.rules' \) ! -user root | grep -q '.'; then
  exit $FAIL
fi

exit $PASS
