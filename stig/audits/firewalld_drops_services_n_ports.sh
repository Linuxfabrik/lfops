source /tmp/lib.sh

if systemctl is-enabled --quiet firewalld.service; then
    active_zone=$(firewall-cmd --get-active-zones | awk 'NR==1{print $1}')
    
    echo "Active zone: $active_zone"
    echo "--------------------------------------------------"
    firewall-cmd --list-all --zone="$active_zone" | grep -E '^(services:|ports:)'
else
    echo "firewalld.service is not enabled."
fi

#NOTE: needs to run under sudo/root to be authorized to access firewalld
