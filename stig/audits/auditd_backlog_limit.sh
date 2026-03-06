source /tmp/lib.sh

if grubby --info=ALL | grep -Po '\baudit_backlog_limit=\d+\b' | awk -F= '$2 >= 8192 {found=1} END {exit !found}' \
   && grep -Pso -- '^\h*GRUB_CMDLINE_LINUX="([^#\n\r]+\h+)?\baudit_backlog_limit=\d+\b' /etc/default/grub | awk -F= '$2 >= 8192 {found=1} END {exit !found}'; then
    exit $PASS
else
    exit $FAIL
fi
