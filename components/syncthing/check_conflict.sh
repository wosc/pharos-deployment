#!/bin/bash

DEST=/srv/prometheus/node/syncthing.prom

count=$(find $HOME/sync/plan/ -name "*sync-conflict*" | wc -l)

echo "
# HELP syncthing_conflicts_total The number of conflicted files.
# TYPE syncthing_conflicts_total gauge
syncthing_conflicts_total ${count:-0}
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}
