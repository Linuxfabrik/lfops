source /tmp/lib.sh      

check_file_root_perms /etc/cron.hourly 700 && exit $PASS || exit $FAIL
