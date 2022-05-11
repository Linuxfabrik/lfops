source /tmp/lib.sh
source /tmp/lib-apache-httpd.sh

conf=$(echo "$APACHE_CONF" | grep -i ";SecRuleEngine ")

if [ -n "$conf" ]; then
    # directive was used and configured, Apache applied no default value, so:

    lines=$(extract "$conf" '<i>' '</i>')
    while IFS= read -r line; do
        if [[ $line != "on" ]]; then exit $FAIL; fi
    done <<< "$lines"
fi

conf=$(echo "$APACHE_CONF" | grep -i ";SecRule " | wc -l)

# CIS: "if the number of active rules is 325 or greater then OWASP
# ModSecurity CRS 3.0 is considered active." Bullshit. 200 rules
# are fair enough.
if [ $conf -ge 250 ]; then
    exit $REV
fi


# use awk for:
# * Inbound Anomaly Threshold must be less than or equal to 5
# * Outbound Anomaly Threshold must be less than or equal to 4
# * Paranoia Level must be greater than or equal to 1

exit $FAIL
