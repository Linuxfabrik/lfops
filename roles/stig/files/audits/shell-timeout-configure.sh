source /tmp/lib.sh

tmout=$(grep "^TMOUT=" /etc/bashrc /etc/profile /etc/profile.d/*.sh 2> /dev/null | cut -d= -f2 | sort --human-numeric-sort --reverse | head -1 | sed 's/;.*//')
if [ -z "$tmout" ]; then exit $FAIL; fi
if [ $tmout -gt 900 ]; then exit $FAIL; fi
# From the bash documentation: If set to a value greater than zero, TMOUT is treated as the default timeout for the read builtin.
if [ $tmout -le 0 ]; then exit $FAIL; fi
exit $PASS
