source /tmp/lib.sh

l_output=""
! grep -Pqs -- '^\h*0\b' /sys/module/ipv6/parameters/disable && l_output="- IPv6 is not enabled"
if sysctl net.ipv6.conf.all.disable_ipv6 2>/dev/null | grep -Pqs -- "^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\b" && \
   sysctl net.ipv6.conf.default.disable_ipv6 2>/dev/null | grep -Pqs -- "^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\b"; then
  l_output="- IPv6 is not enabled"
fi

if [ -z "$l_output" ]; then
  l_output="- IPv6 is enabled"
  echo -e "\n$l_output\n"
  exit $PASS
else
  echo -e "\n$l_output\n"
  exit $FAIL
fi
