#!/bin/bash

DEST=/srv/prometheus/node/numprocs.prom

echo "
# TYPE node_procs_total gauge
node_procs_total $(ps -A --no-headers | wc -l)
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
