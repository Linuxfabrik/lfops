source /tmp/lib.sh

# verify correct permissions, ownership, and group for grub.cfg
# and if it exists, user.cfg
# taken from CIS_CentOS_Linux_8_Benchmark_v1.0.1

tst1="" tst2="" tst3="" tst4="" test1="" test2="" efidir="" gbdir=""
grubdir="" grubfile="" userfile=""

efidir=$(find /boot/efi/EFI/* -maxdepth 0 -type d -not -name 'BOOT')
gbdir=$(find /boot -maxdepth 1 -type d -name 'grub*')

for file in "$efidir"/grub.cfg "$efidir"/grub.conf; do
    [ -f "$file" ] && grubdir="$efidir" && grubfile=$file
done

if [ -z "$grubdir" ]; then
    for file in "$gbdir"/grub.cfg "$gbdir"/grub.conf; do
        [ -f "$file" ] && grubdir="$gbdir" && grubfile=$file
    done
fi

userfile="$grubdir/user.cfg"
stat -c "%a" "$grubfile" | grep -Pq '^\h*[0-7]00$' && tst1=pass
stat -c "%u:%g" "$grubfile" | grep -Pq '^\h*0:0$' && tst2=pass
[ "$tst1" = pass ] && [ "$tst2" = pass ] && test1=pass
if [ -f "$userfile" ]; then
    stat -c "%a" "$userfile" | grep -Pq '^\h*[0-7]00$' && tst3=pass
    stat -c "%u:%g" "$userfile" | grep -Pq '^\h*0:0$' && tst4=pass
    [ "$tst3" = pass ] && [ "$tst4" = pass ] && test2=pass
else
    test2=pass
fi
[ "$test1" = pass ] && [ "$test2" = pass ] && passing=true

# If passing is true we pass
if [ "$passing" = true ] ; then
    exit $PASS
else
    exit $FAIL
fi
