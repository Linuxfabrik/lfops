source /tmp/lib.sh      

if grep -Piq -- '^\h*gpgcheck\h*=\h*(1|true|yes)\b' /etc/dnf/dnf.conf && \
   ! grep -Pris -- '^\h*gpgcheck\h*=\h*(0|[^01]|[^Tt][^Rr][^Uu][^Ee]|[^Yy][^Ee][^Ss])' /etc/yum.repos.d/ >/dev/null 2>&1; then
  exit $PASS
fi
exit $FAIL
