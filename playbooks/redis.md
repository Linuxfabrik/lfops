# Playbook redis

Runs

* [linuxfabrik.lfops.kernel_settings](https://github.com/Linuxfabrik/lfops/tree/main/roles/kernel_settings) - sets kernel parameters specific for Redis
* [linuxfabrik.lfops.redis](https://github.com/Linuxfabrik/lfops/tree/main/roles/redis)

Have a look at the roles README for their available variables.


## Playbook-specific Variables

These variables skip the execution of the corresponding role:

* `redis__skip_kernel_settings`
