source /tmp/lib.sh

if ipv6_is_enabled; then
    if [ "$(sysctl net.ipv6.conf.all.accept_redirects 2> /dev/null)" != 'net.ipv6.conf.all.accept_redirects = 0' ]; then exit $FAIL; fi
    if [ "$(sysctl net.ipv6.conf.default.accept_redirects 2> /dev/null)" != 'net.ipv6.conf.default.accept_redirects = 0' ]; then exit $FAIL; fi
    exit $PASS
else
    exit $SKIP
fi
