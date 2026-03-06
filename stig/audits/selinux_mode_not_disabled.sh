source /tmp/lib.sh      

if getenforce | grep -Eq '^(Enforcing|Permissive)$' && \
   grep -Eqi '^\s*SELINUX=(enforcing|permissive)\b' /etc/selinux/config; then
  exit $PASS
fi
exit $FAIL
