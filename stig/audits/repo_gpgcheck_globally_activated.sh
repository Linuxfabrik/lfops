source /tmp/lib.sh

if ! grep -Piq -- '^\h*repo_gpgcheck\h*=\h*1\b' /etc/dnf/dnf.conf; then
  exit $FAIL
fi

# no repo_gpgcheck=0 overrides in repos
for repo in $(grep -l "repo_gpgcheck=0" /etc/yum.repos.d/* 2>/dev/null); do
  exit $FAIL
done

exit $PASS
