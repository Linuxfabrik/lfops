source /tmp/lib.sh

# journald rotation set per site policy (requires non-empty values)
cfg="$(systemd-analyze cat-config systemd/journald.conf /etc/systemd/journald.conf.d/*.conf 2>/dev/null)"

for k in SystemMaxUse SystemKeepFree RuntimeMaxUse RuntimeKeepFree MaxFileSec; do
  if ! grep -Eq "^[[:space:]]*${k}=[^[:space:]]+" <<< "$cfg"; then
    exit $FAIL
  fi
done

exit $PASS
