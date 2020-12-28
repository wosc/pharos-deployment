#!/bin/bash

DEST=/srv/prometheus/node/mailcheck.prom

/srv/prometheus/bin/mail-check-roundtrip /srv/prometheus/mailcheck.conf
if [ "$?" = "0" ]; then
    MAILCHECK=1
else
    MAILCHECK=0
fi

/srv/prometheus/bin/caldav-check-roundtrip /srv/prometheus/caldavcheck.conf
if [ "$?" = "0" ]; then
    CALDAVCHECK=1
else
    CALDAVCHECK=0
fi

echo "
# TYPE mail_roundtrip_up gauge
mail_roundtrip_up $MAILCHECK
# TYPE mail_caldav_roundtrip_up gauge
mail_caldav_roundtrip_up $CALDAVCHECK
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
