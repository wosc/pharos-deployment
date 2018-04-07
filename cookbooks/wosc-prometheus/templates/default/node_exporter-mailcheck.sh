#!/bin/bash

DEST=/srv/prometheus/node/mailcheck.prom
TS=$(date +%s%N |cut -b1-13)

/usr/local/bin/mail-check-roundtrip /srv/prometheus/mailcheck.conf
if [ "$?" = "0" ]; then
    VALUE=1
else
    VALUE=0
fi

echo "
# TYPE mail_roundtrip_up gauge
mail_roundtrip_up $VALUE $TS
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
