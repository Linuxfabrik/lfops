source /tmp/lib.sh

# TODO: this could be checked against auditctl -l
partitions=$(df | grep '^/dev' | awk '{ print $NF }')
echo Ensure use of privileged commands is collected
echo ----------------------------------------------
echo ''
for i in $partitions; do
    audit_lines=$(find $i -xdev \( -perm -4000 -o -perm -2000 \) -type f | awk '{print "-a always,exit -F path=" $1 " -F perm=x -F auid>='"$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)"' -F auid!=4294967295 -k privileged" }')
    echo "$audit_lines"
done
echo ''
exit $REV
