source /tmp/lib.sh

grubby --info=ALL 2>/dev/null | grep -Poq '\baudit=1\b' || exit $FAIL
grep -Psoi -- '^\h*GRUB_CMDLINE_LINUX="([^#\n\r]+\h+)?audit=1\b' /etc/default/grub >/dev/null 2>&1 || exit $FAIL

exit $PASS
