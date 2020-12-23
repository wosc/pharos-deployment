#!/bin/bash
#
# removes Spam-emails older than 1 month

for dir in /var/mail/*/; do
    if [ -d ${dir}Maildir/.Spam ]; then
        find $dir/Maildir/.Spam/new -daystart -type f -ctime +30 | xargs rm -f
        find $dir/Maildir/.Spam/cur -daystart -type f -ctime +30 | xargs rm -f
    fi
done
