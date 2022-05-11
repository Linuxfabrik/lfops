source /tmp/lib.sh

if is_installed 'lsof'; then
    audit_lines=$(lsof -i -P -n | grep -v "(ESTABLISHED)")
    echo list of services listening on the system
    echo ----------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
fi
exit $REV
