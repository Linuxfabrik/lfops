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
    if [ "$(cat /sys/module/ipv6/parameters/disable)" = "1" ]; then return 1; fi
    return 0
}


# returns 0 if any pkg from a space-separated list is installed; auto-detects dpkg/rpm
any_pkg_installed() {
    local pkg_list="$1"
    local pq=""
    if command -v dpkg-query > /dev/null 2>&1; then
        pq="dpkg-query -W"
    elif command -v rpm > /dev/null 2>&1; then
        pq="rpm -q"
    fi
    for pkg in $pkg_list; do
        $pq "$pkg" > /dev/null 2>&1 && return 0
    done
    return 1
}


# returns 0 if installed rpm pkg version >= given minimum epoch:version-release
rpm_version_gte() {
    local pkg="$1" min_epoch="$2" min_ver="$3" min_rel="$4"
    local evr
    evr="$(rpm -q --qf '%{EPOCHNUM}:%{VERSION}-%{RELEASE}\n' "$pkg" 2>/dev/null)"
    [ -z "$evr" ] && return 1
    python3 - <<PY
import sys, rpm
evr = """$evr""".strip()
epoch, vr = evr.split(":", 1)
ver, rel  = vr.split("-", 1)
sys.exit(0 if rpm.labelCompare((epoch, ver, rel), ("$min_epoch", "$min_ver", "$min_rel")) >= 0 else 1)
PY
}


# pass if pkg not installed or all services neither enabled nor active
service_unused() {
    local pkg="$1"; shift
    is_not_installed "$pkg" && return 0
    systemctl is-enabled "$@" 2>/dev/null | grep -q 'enabled' && return 1
    systemctl is-active "$@" 2>/dev/null | grep -q '^active' && return 1
    return 0
}


# pass if mountpoint exists and has given option
has_mount_option() {
    local mnt="$1" opt="$2"
    findmnt -kn "$mnt" >/dev/null 2>&1 || return 1
    findmnt -kn "$mnt" | grep -v "$opt" | grep -q '.' && return 1
    return 0
}


# pass if mountpoint exists as separate partition
has_separate_partition() {
    findmnt -kn "$1" >/dev/null 2>&1 && return 0
    return 1
}


# pass if file owned by root:root and mode <= max_mode
check_file_root_perms() {
    local file="$1" max_mode="$2"
    [ -e "$file" ] || return 1
    local mode uid gid
    mode="$(stat -Lc '%a' "$file" 2>/dev/null)" || return 1
    uid="$(stat -Lc '%u' "$file" 2>/dev/null)" || return 1
    gid="$(stat -Lc '%g' "$file" 2>/dev/null)" || return 1
    [ "$mode" -le "$max_mode" ] && [ "$uid" -eq 0 ] && [ "$gid" -eq 0 ] && return 0
    return 1
}


# pass if login banner file has no OS/version info leaks
check_login_banner() {
    local file="$1"
    [ -f "$file" ] || return 1
    local os_id re
    os_id="$(grep -E '^ID=' /etc/os-release 2>/dev/null | head -n1 | cut -d= -f2 | sed -e 's/"//g')"
    re='(\\v|\\r|\\m|\\s)'
    [ -n "$os_id" ] && re="(\\v|\\r|\\m|\\s|${os_id})"
    grep -Eiq -- "$re" "$file" && return 1
    return 0
}


# pass if kernel module is not loaded, not loadable, and deny listed
check_kernel_module_disabled() {
    local l_mod_name="$1" l_mod_type="$2"
    local l_output3="" l_dl=""
    local a_output=() a_output2=()
    local l_mod_path
    l_mod_path="$(readlink -f /lib/modules/**/kernel/$l_mod_type 2>/dev/null | sort -u)"

    _f_module_chk() {
        l_dl="y"
        local a_showconfig=()
        while IFS= read -r l_showconfig; do
            a_showconfig+=("$l_showconfig")
        done < <(modprobe --showconfig 2>/dev/null | grep -P -- '\b(install|blacklist)\h+'"${l_mod_name//-/_}"'\b')

        if ! lsmod | grep "$l_mod_name" &>/dev/null; then
            a_output+=(" - kernel module: \"$l_mod_name\" is not loaded")
        else
            a_output2+=(" - kernel module: \"$l_mod_name\" is loaded")
        fi

        if grep -Pq -- '\binstall\h+'"${l_mod_name//-/_}"'\h+\/bin\/(true|false)\b' <<< "${a_showconfig[*]}"; then
            a_output+=(" - kernel module: \"$l_mod_name\" is not loadable")
        else
            a_output2+=(" - kernel module: \"$l_mod_name\" is loadable")
        fi

        if grep -Pq -- '\bblacklist\h+'"${l_mod_name//-/_}"'\b' <<< "${a_showconfig[*]}"; then
            a_output+=(" - kernel module: \"$l_mod_name\" is deny listed")
        else
            a_output2+=(" - kernel module: \"$l_mod_name\" is not deny listed")
        fi
    }

    for l_mod_base_directory in $l_mod_path; do
        if [ -d "$l_mod_base_directory/${l_mod_name/-/\/}" ] && [ -n "$(ls -A "$l_mod_base_directory/${l_mod_name/-/\/}" 2>/dev/null)" ]; then
            l_output3="$l_output3\n - \"$l_mod_base_directory\""
            [[ "$l_mod_name" =~ overlay ]] && l_mod_name="${l_mod_name::-2}"
            [ "$l_dl" != "y" ] && _f_module_chk
        else
            a_output+=(" - kernel module: \"$l_mod_name\" doesn't exist in \"$l_mod_base_directory\"")
        fi
    done

    [ -n "$l_output3" ] && echo -e "\n\n -- INFO --\n - module: \"$l_mod_name\" exists in:$l_output3"

    if [ "${#a_output2[@]}" -le 0 ]; then
        printf '%s\n' "" "- Audit Result:" " ** PASS **" "${a_output[@]}"
        return 0
    else
        printf '%s\n' "" "- Audit Result:" " ** FAIL **" " - Reason(s) for audit failure:" "${a_output2[@]}"
        [ "${#a_output[@]}" -gt 0 ] && printf '%s\n' "- Correctly set:" "${a_output[@]}"
        return 1
    fi
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
