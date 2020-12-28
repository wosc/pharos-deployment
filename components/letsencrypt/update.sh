#!/bin/bash

email="wosc@wosc.de"

cd ~/data
for domain in */; do
    domain=$(basename $domain)
    cd ~/data/$domain

    aliases=$domain
    if [ -f ./aliases ]; then
        aliases="$aliases $(tr "\n" " " < ./aliases)"
    fi

    vhosts=""
    for name in $aliases; do
        vhosts="$vhosts --vhost $name:$HOME/public/$domain"
    done

    ~/deployment/bin/simp_le --email $email $vhosts \
                             --reuse_key -f key.pem -f cert.pem -f fullchain.pem \
                             -f account_key.json -f account_reg.json
    updated=$?
    rm -rf ~/public/$domain/acme-challenge

    if [ "$updated" = "0" ]; then
        if [ -x ./update ]; then
            ./update
        else
            sudo /etc/init.d/nginx reload &> /dev/null
        fi
    fi
done
