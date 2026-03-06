source /tmp/lib.sh

l_output="" l_output2="" l_hbfw=""

# Determine which firewall utility is in use (same convention as prior CIS scripts)
if systemctl is-enabled firewalld.service 2>/dev/null | grep -q 'enabled'; then
  l_hbfw="fwd"
elif systemctl is-enabled nftables.service 2>/dev/null | grep -q 'enabled'; then
  l_hbfw="nft"
fi

# Firewalld note: base chains are installed by default
if [ "$l_hbfw" = "fwd" ]; then
  echo -e "\n- Audit Result:\n *** PASS ***\n - FirewallD is in use (base chains installed by default)\n"
  exit "$PASS"
fi

# If nftables isn't in use, this audit can't be satisfied as written
if [ "$l_hbfw" != "nft" ]; then
  echo -e "\n- Audit Result:\n *** FAIL ***\n - Neither FirewallD nor NFTables appears to be enabled\n - Ensure a single firewall configuration utility is in use\n"
  exit "$FAIL"
fi

# NFTables audit: verify base chains exist for INPUT/FORWARD/OUTPUT hooks
l_ruleset="$(nft list ruleset 2>/dev/null)"

if grep -q 'hook input' <<< "$l_ruleset" && grep -q 'type filter hook input' <<< "$l_ruleset"; then
  l_output="$l_output\n - INPUT base chain exists (type filter hook input)"
else
  l_output2="$l_output2\n - Missing INPUT base chain for filter hook input"
fi

if grep -q 'hook forward' <<< "$l_ruleset" && grep -q 'type filter hook forward' <<< "$l_ruleset"; then
  l_output="$l_output\n - FORWARD base chain exists (type filter hook forward)"
else
  l_output2="$l_output2\n - Missing FORWARD base chain for filter hook forward"
fi

if grep -q 'hook output' <<< "$l_ruleset" && grep -q 'type filter hook output' <<< "$l_ruleset"; then
  l_output="$l_output\n - OUTPUT base chain exists (type filter hook output)"
else
  l_output2="$l_output2\n - Missing OUTPUT base chain for filter hook output"
fi

if [ -z "$l_output2" ]; then
  echo -e "\n- Audit Result:\n *** PASS ***\n$l_output\n"
  exit "$PASS"
else
  echo -e "\n- Audit Result:\n *** FAIL ***\n$l_output2\n\n - Correctly set:\n$l_output\n"
  exit "$FAIL"
fi
