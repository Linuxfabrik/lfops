source /tmp/lib.sh

if grep -Psq '^\h*([^#\n\r]+)?\/nologin\b' /etc/shells; then exit $FAIL; fi
exit $PASS