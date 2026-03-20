source /tmp/lib.sh

l_output="" l_output2=""

if grep -Piq -- '^\h*cipher\h*=\h*([^#\n\r]+)?-CBC\b' /etc/crypto-policies/state/CURRENT.pol; then
  if grep -Piq -- '^\h*cipher@(lib|open)ssh(-server|-client)?\h*=\h*' /etc/crypto-policies/state/CURRENT.pol; then
    if ! grep -Piq -- '^\h*cipher@(lib|open)ssh(-server|-client)?\h*=\h*([^#\n\r]+)?-CBC\b' /etc/crypto-policies/state/CURRENT.pol; then
      l_output="$l_output\n - Cipher Block Chaining (CBC) is disabled for SSH"
    else
      l_output2="$l_output2\n - Cipher Block Chaining (CBC) is enabled for SSH"
    fi
  else
    l_output2="$l_output2\n - Cipher Block Chaining (CBC) is enabled for SSH"
  fi
else
  l_output=" - Cipher Block Chaining (CBC) is disabled"
fi

if [ -z "$l_output2" ]; then
  exit $PASS
else
  exit $FAIL
fi