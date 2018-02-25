#!/bin/bash
#
# pipes mail to sa-learn and removes them afterwards

for dir in /var/mail/*/; do
    user=$(basename "$dir")
    if [ -d ${dir}Maildir/.learn_spam ]; then
        find ${dir}Maildir/.learn_spam/new -maxdepth 1 -type f | xargs sa-learn -u $user --spam > /dev/null
        find ${dir}Maildir/.learn_spam/cur -maxdepth 1 -type f | xargs sa-learn -u $user --spam > /dev/null
        find ${dir}Maildir/.learn_spam/new -maxdepth 1 -type f | xargs rm -f
        find ${dir}Maildir/.learn_spam/cur -maxdepth 1 -type f | xargs rm -f
    fi
    if [ -d ${dir}Maildir/.learn_mail ]; then
        find ${dir}Maildir/.learn_mail/new -maxdepth 1 -type f | xargs sa-learn -u $user --ham > /dev/null
        find ${dir}Maildir/.learn_mail/cur -maxdepth 1 -type f | xargs sa-learn -u $user --ham > /dev/null
        find ${dir}Maildir/.learn_mail/new -maxdepth 1 -type f | xargs rm -f
        find ${dir}Maildir/.learn_mail/cur -maxdepth 1 -type f | xargs rm -f
    fi
done
