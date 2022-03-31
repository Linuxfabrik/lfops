# {{ ansible_managed }}
# 2020022001

alias whatismyip="curl ipecho.net/plain"
alias dmesg='dmesg --level=emerg,alert,crit,err --reltime'

function lf-confirm() {
    echo -n "Are you sure? [y/N] "
    read reply

    if [ "$reply" = y -o "$reply" = Y ]
    then
        return 0
    else
        echo "Command cancelled."
        return 1
    fi
}

{% if icinga2_master is defined and icinga2_master|length %}
function schedule-icinga-downtime() {
    if [ -z "$1" ]; then
        echo 'arg 1 required! (downtime duration in s).'
        exit 1
    fi

    if [ -z "$2" ]; then
        comment="Downtime set per schedule-icinga-downtime."
    else
        comment="$2"
    fi

    START_TIME=$(date +%s)
    END_TIME=$(( $START_TIME + $1 ))
    DATA="{ \"type\": \"Host\", \"filter\": \"match(\\\"{{ ansible_facts['fqdn'] }}\\\", host.name)\", \"start_time\": \"$START_TIME\", \"end_time\": \"$END_TIME\", \"author\": \"{{ ansible_facts['fqdn'] }}\", \"comment\": \"$comment\" , \"all_services\": true }"
    curl --connect-timeout 5 --insecure --silent --user {{ icinga2_api_user }}:{{ icinga2_api_password }} --header 'Accept: application/json' --request POST 'https://{{ icinga2_master }}:5665/v1/actions/schedule-downtime' --data "$DATA" 1> /dev/null
{% if (external_monitor_api is defined and external_monitor_api|length)
    and (external_monitor_api_user is defined and external_monitor_api_user|length )
    and (external_monitor_api_password is defined and external_monitor_api_password|length)
    and (external_monitor_services is defined and external_monitor_services|length) %}
    DATA="{ \"type\": \"Service\", \"filter\": \"{% for service in external_monitor_services %}match(\\\"{{ service }}\\\", service.name){% if not loop.last %} || {% endif %}{% endfor %}\", \"start_time\": \"$START_TIME\", \"end_time\": \"$END_TIME\", \"author\": \"{{ ansible_facts['fqdn'] }}\", \"comment\": \"$comment\" }"
    curl --connect-timeout 5 --insecure --silent --user {{ external_monitor_api_user }}:{{ external_monitor_api_password }} --header 'Accept: application/json' --request POST 'https://{{ external_monitor_api }}/v1/actions/schedule-downtime' --data "$DATA" 1> /dev/null
{% endif %}
}

alias reboot="lf-confirm && schedule-icinga-downtime 300 'Manual reboot' && /usr/sbin/reboot"
{% else %}
alias reboot="lf-confirm && /usr/sbin/reboot"
{% endif %}
alias poweroff="lf-confirm && /usr/sbin/poweroff"
