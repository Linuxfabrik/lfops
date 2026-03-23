source /tmp/lib.sh      

# global config must set repo_gpgcheck=1
if ! grep -Piq -- '^\h*repo_gpgcheck\h*=\h*1\b' /etc/dnf/dnf.conf; then
  exit $FAIL
fi

# ensure no repo_gpgcheck=0 in repos
if grep -Prs -- '^\h*repo_gpgcheck\h*=\h*0\b' /etc/yum.repos.d/ >/dev/null 2>&1; then
  exit $FAIL
fi

exit $PASS
