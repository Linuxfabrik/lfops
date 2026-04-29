# vulture whitelist
#
# vulture's pre-commit hook complains about a handful of names in the
# existing plugins. They are tracked centrally in
# https://github.com/Linuxfabrik/lfops/issues/221 and removed from this
# whitelist as they get cleaned up.
#
# Without this file every commit that touches a Python file fails
# pre-commit with the same four findings, even though they have nothing
# to do with the change at hand.

# plugins/lookup/bitwarden_item.py:293
# False positive: `variables` is part of the Ansible lookup-plugin
# `run()` signature, the framework passes it in, vulture cannot see that.
variables

# plugins/module_utils/gnupg.py:45
# Real dead code — to be removed in a follow-up.
locale

# plugins/module_utils/gnupg.py:66
# Unused loop / unpack variable; intentional placeholder, can stay.
record

# plugins/modules/ipauser.py:891
# Real dead code — to be removed in a follow-up.
ipa_user_id
