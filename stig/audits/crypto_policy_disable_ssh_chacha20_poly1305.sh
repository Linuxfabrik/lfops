source /tmp/lib.sh

l_output="" l_output2=""

if grep -Piq -- '^\h*cipher\h*=\h*([^#\n\r]+)?-CBC\b' /etc/crypto-policies/state/CURRENT.pol; then
  if grep -Piq -- '^\h*cipher@(lib|open)ssh(-server|-client)?\h*=\h*' /etc/crypto-policies/state/CURRENT.pol; then
    if ! grep -Piq -- '^\h*cipher@(lib|open)ssh(-server|-client)?\h*=\h*([^#\n\r]+)?\bchacha20-poly1305\b' /etc/crypto-policies/state/CURRENT.pol; then
      l_output="$l_output\n - chacha20-poly1305 is disabled for SSH"
    else
      l_output2="$l_output2\n - chacha20-poly1305 is enabled for SSH"
    fi
  else
    l_output2="$l_output2\n - chacha20-poly1305 is enabled for SSH"
  fi
else
  l_output=" - chacha20-poly1305 is disabled"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi