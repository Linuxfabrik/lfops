source /tmp/lib.sh

state=1

pwauth_history=$(grep -E '^password\s+required\s+pam_pwhistory.so.*remember' /etc/pam.d/password-auth)
sysauth_history=$(grep -E '^password\s+required\s+pam_pwhistory.so.*remember' /etc/pam.d/system-auth)
pwauth_unix=$(grep -E '^password\s+sufficient\s+pam_unix.so.*remember' /etc/pam.d/password-auth)
sysauth_unix=$(grep -E '^password\s+sufficient\s+pam_unix.so.*remember' /etc/pam.d/system-auth)

pwauth_history_count=$(echo "$pwauth_history" | sed -e 's/.*remember=\([0-9]*\)/\1/')
sysauth_history_count=$(echo "$sysauth_history" | sed -e 's/.*remember=\([0-9]*\)/\1/')
pwauth_unix_count=$(echo "$pwauth_unix" | sed -e 's/.*remember=\([0-9]*\)/\1/')
sysauth_unix_count=$(echo "$sysauth_unix" | sed -e 's/.*remember=\([0-9]*\)/\1/')

## Use parameter expansion so that null values become 0 and don't break the tests
## https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
pwauth_history_count=${pwauth_history_count:-0}
sysauth_history_count=${sysauth_history_count:-0}
pwauth_unix_count=${sysauth_unix_count:-0}
sysauth_unix_count=${sysauth_unix_count:-0}

## I couldn't be bothered handling null values, so used param expansion above
## so that null values became zeroes
if [ $pwauth_history_count -ge 5 -a $sysauth_history_count -ge 5 ]; then exit $FAIL; fi
if [ $pwauth_unix_count -ge 5 -a $sysauth_unix_count -ge 5 ]; then exit $FAIL; fi

exit $PASS
