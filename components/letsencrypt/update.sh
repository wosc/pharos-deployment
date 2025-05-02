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

    # Using the main $domain for all vhosts works in conjunction with nginx.conf
    # which specifies (the first) $server_name, because our port 80 servers
    # redirect to https://$server_name -- i.e. once an initial certificate exists
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
            sudo systemctl reload nginx &> /dev/null
        fi
    fi
done
