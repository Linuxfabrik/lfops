source /tmp/lib.sh

if is_enabled 'httpd'; then exit $FAIL; fi
if is_enabled 'nginx'; then exit $FAIL; fi
if is_enabled 'lighttpd'; then exit $FAIL; fi
exit $PASS
