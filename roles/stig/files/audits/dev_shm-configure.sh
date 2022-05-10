source /tmp/lib.sh

if [ -z "$(mount | grep -E '\s/dev/shm\s')" ]; then exit $SKIP; fi
exit $PASS
