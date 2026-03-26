source /tmp/lib.sh      

if { is_enabled 'crond' || is_enabled 'cron'; } && \
   { is_active 'crond' || is_active 'cron'; }; then
  exit $PASS
fi
exit $FAIL
