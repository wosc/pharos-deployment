#!/bin/bash

set -e

cd /home/neckharmonics

if [[ "last.push" -nt "last.pull" ]]; then
    cd public_html
    git fetch &> /dev/null
    git reset --hard origin/main &> /dev/null
    touch "../last.pull"
fi
