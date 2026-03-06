source /tmp/lib.sh

encrypt_method="$(grep -Pi -- '^\h*ENCRYPT_METHOD\h+(SHA512|yescrypt)\b' /etc/login.defs | awk '{print $2}')"

if [ -z "$encrypt_method" ]; then
    exit $FAIL
fi

exit $PASS