source /tmp/lib.sh

audit_lines=$(rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n')
echo rpm gpg keys
echo ------------
echo ''
echo "$audit_lines"
echo ''
exit $REV
