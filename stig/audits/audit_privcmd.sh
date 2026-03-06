source /tmp/lib.sh

fail=0

RUNNING=$(auditctl -l)
[ -n "${RUNNING}" ] || exit $FAIL

for PARTITION in $(findmnt -n -l -k -it $(awk '/nodev/ { print $2 }' /proc/filesystems | paste -sd,) | grep -Pv "noexec|nosuid" | awk '{print $1}'); do
  for PRIVILEGED in $(find "${PARTITION}" -xdev -perm /6000 -type f); do
    grep -qr "${PRIVILEGED}" /etc/audit/rules.d && printf '' || fail=1
    printf -- "${RUNNING}" | grep -q "${PRIVILEGED}" || fail=1
  done
done

if [ "$fail" -eq 0 ]; then
  exit $PASS
else
  exit $FAIL
fi