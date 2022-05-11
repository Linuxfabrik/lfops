source /tmp/lib.sh

audit_lines=$(for dir in $(grep -E --invert-match '(halt|sync|shutdown)' /etc/passwd | awk -F: '($7 != "/usr/sbin/nologin" && $7 != "/sbin/nologin" && $7 != "/bin/false") {print $6}' | sort | uniq); do
        if [ -e "$dir/.netrc" ]; then
            perms=$(stat $dir/.netrc | awk 'NR==4 {print $2}')
            # "(0644/-rw-r--r--)"
            if [ $(echo $perms | cut -c11) != "-" ]; then echo "$dir/.netrc"; continue; fi
            if [ $(echo $perms | cut -c12) != "-" ]; then echo "$dir/.netrc"; continue; fi
            if [ $(echo $perms | cut -c13) != "-" ]; then echo "$dir/.netrc"; continue; fi
            if [ $(echo $perms | cut -c14) != "-" ]; then echo "$dir/.netrc"; continue; fi
            if [ $(echo $perms | cut -c15) != "-" ]; then echo "$dir/.netrc"; continue; fi
            if [ $(echo $perms | cut -c16) != "-" ]; then echo "$dir/.netrc"; continue; fi
        fi
    done)
if [ -n "$(echo "$audit_lines" | sed 's/\s*$//')" ]; then
    echo users\' .netrc files that are group or world accessible
    echo -------------------------------------------------------
    echo ''
    echo "$audit_lines"
    echo ''
    exit $FAIL
fi
exit $PASS
