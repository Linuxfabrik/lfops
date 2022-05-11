source /tmp/lib.sh

# ignore those files and directories due to changing chmods on
# every reboot (CIS includes everything)
if [ $(find /var/log \
    -type f \
    ! -iname btmp \
    ! -iname dmesg \
    ! -iname lastlog \
    ! -iname wtmp \
    -perm /g+wx,o+rwx \
    -ls 2>/dev/null | wc -l) -eq 0 ]; then exit $PASS; fi
exit $FAIL
