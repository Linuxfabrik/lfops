# list of result codes
PASS=0
FAIL=1
SKIP=2                      # not applicable
TODO=4                      # needs to be implemented
REV=8                       # review manually

# Remove locale settings to eliminate localized outputs where possible
export LC_ALL=C
unset LANG


extract() {
    local result=$(echo "$1" | awk -F "$2|$3" '{print tolower($2)}')
    echo "$result"
}


has_fsopt_on_usb() {
    local fsopt=$1
    ## Note: Only usb media is supported at the moment. Need to investigate what
    ##  difference a CDROM, etc. can make, but I've set it up ready to add
    ##  another search term. You're welcome :)
    local filesystems=$(for device in "$devices"; do lsblk --paths --noheadings --list $device | grep -E --invert-match '^$device|[SWAP]' | awk '{print $1}'; done)
    for filesystem in $filesystems; do
        fs_without_opt=$(mount | grep -E "$filesystem\s" | grep --invert-match "$fsopt" &>/dev/null | wc -l)
        if [ $fs_without_opt -ne 0 ]; then return 1; fi
    done
    return 0
}


has_usb_devices() {
    if [ -z "$(lsblk --paths --noheadings --list --scsi | awk '/usb/ {print $1}')" ]; then return 1; fi
    return 0
}


is_active() {
    if systemctl is-active $1 >/dev/null 2>&1; then return 0; fi
    return 1
}


is_active_kernelmod() {
    if [ $(diff -qsZ <(modprobe --dry-run --verbose $1 2>/dev/null | tail -n1) <(echo "install /bin/true") &>/dev/null; echo $?) -ne 0 ]; then return 0; fi
    if [ -n "$(lsmod | grep $1)" ]; then return 0; fi
    return 1
}


is_disabled() {
    if ! systemctl is-enabled $1 >/dev/null 2>&1; then return 0; fi
    return 1
}


is_enabled() {
    if systemctl is-enabled $1 &>/dev/null; then return 0; fi
    return 1
}


is_installed() {
    if rpm -q $1 &> /dev/null; then return 0; fi
    return 1
}


is_not_installed() {
    if ! rpm -q $1 &> /dev/null; then return 0; fi
    return 1
}


ipv6_is_enabled() {
    if [ "$(cat /sys/module/ipv6/parameters/disable)" == "1" ]; then return 1; fi
    return 0
}


test_perms() {
    local perms=$1
    local file=$2

    # if the file does not exist, we are tolerant: then the file permissions are not wrong
    if [ ! -e $file ]; then return $PASS; fi

    local u=$(echo $perms | cut -c1)
    local g=$(echo $perms | cut -c2)
    local o=$(echo $perms | cut -c3)
    local file_perms="$(stat -L $file | awk '/Access: \(/ {print $2}')"
    local file_u=$(echo $file_perms | cut -c3)
    local file_g=$(echo $file_perms | cut -c4)
    local file_o=$(echo $file_perms | cut -c5)

    if [ "$(ls -ld $file | awk '{ print $3" "$4 }')" != "root root" ]; then return $FAIL; fi
    if [ $file_u -gt $u ]; then return $FAIL; fi
    if [ $file_g -gt $g ]; then return $FAIL; fi
    if [ $file_o -gt $o ]; then return $FAIL; fi

    return $PASS
}
