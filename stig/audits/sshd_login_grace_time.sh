source /tmp/lib.sh      

if [ -z "$(sshd -T | awk '$1 ~ /^\s*logingracetime/{if($2 > 60) print $0}')" ]; then
  exit $PASS
fi
exit $FAIL
