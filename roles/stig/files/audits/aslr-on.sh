source /tmp/lib.sh

if [ "$(sysctl kernel.randomize_va_space 2> /dev/null)" != 'kernel.randomize_va_space = 2' ]; then exit $FAIL; fi
# if [ "$(grep "^kernel\.randomize_va_space" /etc/sysctl.conf /etc/sysctl.d/*  | sed -e 's/^.*://' -e 's/\s//g' | sort | uniq)" != 'kernel.randomize_va_space=2' ]; then exit $FAIL; fi

# TODO: if systemctl is-enabled coredump.service, then check
# /etc/systemd/coredump.conf:
# Storage=none
# ProcessSizeMax=0
exit $PASS
