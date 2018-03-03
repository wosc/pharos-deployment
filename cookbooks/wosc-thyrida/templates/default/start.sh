#!/bin/bash
if ! supervisorctl status thyrida | grep -q RUNNING; then
    supervisorctl start thyrida > /dev/null
    sleep 2
    target="/user/login"
else
    target="/domain/list"
fi
echo "Location: http://${SERVER_NAME}:${SERVER_PORT}${target}"
echo
echo
