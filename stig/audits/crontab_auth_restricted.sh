source /tmp/lib.sh      

check_file_root_perms /etc/cron.allow 640 && exit $PASS || exit $FAIL
