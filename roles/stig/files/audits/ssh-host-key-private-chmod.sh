source /tmp/lib.sh

files=$(find /etc/ssh -xdev -type f -name 'ssh_host_*_key')
for file in $files; do
    if ! test_perms 600 $file; then exit $FAIL; fi
done
exit $PASS
