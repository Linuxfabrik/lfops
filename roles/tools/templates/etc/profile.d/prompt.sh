# {{ ansible_managed }}
# 2022033101

if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
    VER=$(cat /etc/debian_version)
elif [ -f /etc/SuSe-release ]; then
    # Older SuSE/etc.
    OS=$(cat /etc/SuSe-release)
    VER=''
elif [ -f /etc/redhat-release ]; then
    # Older Red Hat, CentOS, etc.
    OS=$(cat /etc/redhat-release)
    VER=''
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    VER=$(uname -r)
fi

RED="\[\033[1;31m\]"
GREEN="\[\033[1;32m\]"
YELLOW="\[\033[1;33m\]"
WHITEONRED="\[\033[41;37m\]"
NO_COLOR="\[\033[0m\]"

PSRED="[$RED\$(date +%H:%M:%S) \u@\h $OS$VER \w$NO_COLOR]\$ "
PSYELLOW="[$YELLOW\$(date +%H:%M:%S) \u@\h $OS$VER \w$NO_COLOR]\$ "
PSGREEN="[$GREEN\$(date +%H:%M:%S) \u@\h $OS$VER \w$NO_COLOR]\$ "

{% if tools__prompt_ps1 is defined and tools__prompt_ps1 | length %}
export PS1="{{ tools__prompt_ps1 }}"
{% else %}
{% if 'test' in group_names %}
export PS1=$PSGREEN
{% elif 'stage' in group_names %}
export PS1=$PSYELLOW
{% else %}
export PS1=$PSRED
{% endif %}
{% endif %}
