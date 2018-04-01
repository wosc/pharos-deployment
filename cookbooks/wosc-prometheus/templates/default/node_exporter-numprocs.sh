#!/bin/bash

DEST=/srv/prometheus/node/numprocs.prom
TS=$(date +%s%N |cut -b1-13)

echo "
# TYPE node_procs_total gauge
node_procs_total $(ps -A --no-headers | wc -l) $TS
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
