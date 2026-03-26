source /tmp/lib.sh      

if is_installed 'chrony'; then
    # grep -Psi -- '^\h*OPTIONS=\"?\h*([^#\n\r]+\h+)?-u\h+root\b' /etc/sysconfig/chronyd
    if ! grep -Psi -- '^\h*OPTIONS=\"?\h*([^#\n\r]+\h+)?-u\h+root\b' /etc/sysconfig/chronyd &>/dev/null; then
        exit $PASS
    fi
fi
exit $FAIL