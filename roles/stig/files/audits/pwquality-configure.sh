source /tmp/lib.sh

## Notes: Per the standard - Additional module options may be set, recommendation
##   requirements only cover including try_first_pass and minlen set to 14 or more.
if [ $(grep -E --count "^password\s+requisite\s+pam_pwquality.so.*try_first_pass.*retry=3" /etc/pam.d/password-auth) -eq 0 ]; then exit $FAIL; fi
if [ $(grep -E --count "^password\s+requisite\s+pam_pwquality.so.*try_first_pass.*retry=3" /etc/pam.d/system-auth) -eq 0 ]; then exit $FAIL; fi
minlen="$(awk '/^\s*minlen = / {print $3}' /etc/security/pwquality.conf)"
minlen=${minlen:=0}
if [ $minlen -lt 14 ]; then exit $FAIL; fi
exit $PASS
