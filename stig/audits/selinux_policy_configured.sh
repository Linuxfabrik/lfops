source /tmp/lib.sh      

if grep -Eq '^\s*SELINUXTYPE=(targeted|mls)\b' /etc/selinux/config && \
   [ "$(sestatus | grep 'Loaded policy name' | awk -F': ' '{print $2}')" = "$(grep -E '^\s*SELINUXTYPE=' /etc/selinux/config | awk -F'=' '{print $2}')" ]; then
   exit $PASS
fi
exit $FAIL
