#!/bin/bash

DEST=/srv/prometheus/node/sslexpires.prom

EXPIRES=$(/srv/prometheus/bin/sslexpires mail.wosc.de)

echo "
# TYPE ssl_certificate_expires gauge
ssl_certificate_expires{hostname=\"mail.wosc.de\"} $EXPIRES
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
