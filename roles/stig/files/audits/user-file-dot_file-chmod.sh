source /tmp/lib.sh

audit_lines=$(for dir in $(grep -E --invert-match '(halt|sync|shutdown|nfsnobody)' /etc/passwd | awk -F: '($7 != "/usr/sbin/nologin" && $7 != "/sbin/nologin" && $7 != "/bin/false") {print $6}' | sort | uniq); do
        for file in $dir/.[A-Za-z0-9]*; do
            if [ ! -h "$file" -a -f "$file" ]; then
                perms=$(stat $file | awk 'NR==4 {print $2}')
                # "(0644/-rw-r--r--)"
                if [ $(echo $perms | cut -c13) != "-" ]; then echo "$file"; continue; fi
                if [ $(echo $perms | cut -c16) != "-" ]; then echo "$file"; continue; fi
            fi
        done
    done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo users\' dot files that are group or world writable
    echo --------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
