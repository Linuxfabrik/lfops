source /tmp/lib.sh      

if [ -z "$(sshd -T | awk '$1 ~ /^\s*maxstartups/{split($2, a, ":");{if(a[1] > 10 || a[2] > 30 || a[3] > 60) print $0}}')" ]; then
  exit $PASS
fi
exit $FAIL
