source /tmp/lib.sh

cfg="$(systemd-analyze cat-config systemd/journal-upload.conf /etc/systemd/journal-upload.conf.d/*.conf 2>/dev/null)"

for k in URL ServerKeyFile ServerCertificateFile TrustedCertificateFile; do
  if ! grep -Eq "^[[:space:]]*${k}=[^[:space:]]+" <<< "$cfg"; then
    exit $FAIL
  fi
done

exit $PASS
 
 #NOTE: the verification of the output is based on example values this here MUST be manually reviewed