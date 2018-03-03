#!/bin/bash
now=$(date +%s)
lastmodified=$(stat -c %Y /var/log/supervisor/thyrida.log)
if (( now - lastmodified > 5 * 60)); then
    supervisorctl stop thyrida > /dev/null
fi
