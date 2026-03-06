source /tmp/lib.sh

# only one logging system in use (rsyslog xor journald)
rs=0 jl=0
systemctl is-active --quiet rsyslog && rs=1
systemctl is-active --quiet systemd-journald && jl=1

if [ "$rs" -eq 1 ] && [ "$jl" -eq 1 ]; then
  exit $FAIL
fi

if [ "$rs" -eq 1 ] || [ "$jl" -eq 1 ]; then
  exit $PASS
fi

exit $FAIL
