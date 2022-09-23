# {{ ansible_managed }}
# 2022051101

RED="\[\033[1;31m\]"
GREEN="\[\033[1;32m\]"
YELLOW="\[\033[1;33m\]"
WHITEONRED="\[\033[41;37m\]"
NO_COLOR="\[\033[0m\]"

PSRED="[$RED\$(date +%H:%M:%S) \u@\h {{ ansible_facts['distribution'] }}{{ ansible_facts['distribution_major_version'] }} \w$NO_COLOR]\$ "
PSYELLOW="[$YELLOW\$(date +%H:%M:%S) \u@\h {{ ansible_facts['distribution'] }}{{ ansible_facts['distribution_major_version'] }} \w$NO_COLOR]\$ "
PSGREEN="[$GREEN\$(date +%H:%M:%S) \u@\h {{ ansible_facts['distribution'] }}{{ ansible_facts['distribution_major_version'] }} \w$NO_COLOR]\$ "

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
