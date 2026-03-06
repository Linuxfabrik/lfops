source /tmp/lib.sh      

if dnf check-update >/dev/null 2>&1; then
  if ! dnf needs-restarting -r >/dev/null 2>&1; then
    exit $PASS
  fi
fi

exit $FAIL
