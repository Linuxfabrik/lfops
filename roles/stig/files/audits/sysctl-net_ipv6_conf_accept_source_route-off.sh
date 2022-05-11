source /tmp/lib.sh

if ipv6_is_enabled; then
    if [ "$(sysctl net.ipv6.conf.all.accept_source_route 2> /dev/null)" != 'net.ipv6.conf.all.accept_source_route = 0' ]; then exit $FAIL; fi
    if [ "$(sysctl net.ipv6.conf.default.accept_source_route 2> /dev/null)" != 'net.ipv6.conf.default.accept_source_route = 0' ]; then exit $FAIL; fi
    exit $PASS
else
    exit $SKIP
fi
