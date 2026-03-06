source /tmp/lib.sh

grep -Psi -- '^\h*etm\b' /etc/crypto-policies/state/CURRENT.pol \
  | grep -qiE '(etm@(libssh|openssh(-server|-client)?|SSH)|^etm)\s*=\s*DISABLE_ETM' && exit $PASS
exit $FAIL