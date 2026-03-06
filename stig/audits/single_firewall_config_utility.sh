source /tmp/lib.sh

l_fwd_status=""
l_nft_status=""
l_fwutil_status=""

is_installed 'firewalld' && l_fwd_status="$(systemctl is-enabled firewalld.service):$(systemctl is-active firewalld.service)"
is_installed 'nftables' && l_nft_status="$(systemctl is-enabled nftables.service):$(systemctl is-active nftables.service)"

l_fwutil_status="$l_fwd_status:$l_nft_status"

case $l_fwutil_status in
  enabled:active:masked:inactive|enabled:active:disabled:inactive)
    exit $PASS ;;
  masked:inactive:enabled:active|disabled:inactive:enabled:active)
    exit $PASS ;;
  enabled:active:enabled:active)
    exit $FAIL ;;
  enabled:*:enabled:*)
    exit $FAIL ;;
  *:active:*:active)
    exit $FAIL ;;
  :enabled:active)
    exit $PASS ;;
  *)
    exit $FAIL ;;
esac
