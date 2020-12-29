#!/bin/bash
# https://gitlab.com/MathieuMD/node_exporter-exim

DEST=/srv/prometheus/node/mail_queue.prom

unit2val() {
    v=$(echo $1|tr -d '[A-Za-z]')
    u=$(echo $1|tr -d '[., 0-9]')
    case $u in
        K|KB|KiB|Ko|Kio) v=$(python -c "print(int(round($v*1024)))");;
        M|MB|MiB|Mo|Mio) v=$(python -c "print(int(round($v*1024**2)))");;
        G|GB|GiB|Go|Gio) v=$(python -c "print(int(round($v*1024**3)))");;
        T|TB|TiB|To|Tio) v=$(python -c "print(int(round($v*1024**4)))");;
        P|PB|PiB|Po|Pio) v=$(python -c "print(int(round($v*1024**5)))");;
    esac
    echo $v
}

MQ="$(mailq)"

MQS="$(echo "$MQ" |/usr/sbin/exiqsumm 2>/dev/null |grep 'TOTAL$')"
#Count  Volume  Oldest  Newest  Domain
#-----  ------  ------  ------  ------
#
#    3    74KB     23h      0m  example.com
#...
#    2    10KB      4d      4d  example.net
#---------------------------------------------------------------
#    9   148KB      4d      0m  TOTAL

nb="$(echo "$MQS" |awk '{print $1}')"
vol="$(echo "$MQS" |awk '{print $2}')"

MQF="$(echo "$MQ" |grep '\*\*\* frozen \*\*\*$')"
#15h   15K 1eJSFg-0003ls-MJ <iztotfq@informinge.biz.ua> *** frozen ***
fz="$(echo -n "$MQF" |wc -l)"
fzvol="$(( $(echo $(echo "$MQF" |awk '{print $2}' |while read i; do unit2val $i; done) |tr ' ' '+') ))"

echo "
# HELP mail_queue_total The total number of messages in queue.
# TYPE mail_queue_total gauge
mail_queue_total ${nb:-0}

# HELP mail_queue_bytes_total The total size of all messages in queue.
# TYPE mail_queue_bytes_total gauge
mail_queue_bytes_total $(unit2val ${vol:-0})

# HELP mail_queue_frozen_total The total number of frozen messages in queue.
# TYPE mail_queue_frozen_total gauge
mail_queue_frozen_total ${fz:-0}

# HELP mail_queue_frozen_bytes_total The total size of all frozen messages.
# TYPE mail_queue_frozen_bytes_total gauge
mail_queue_frozen_bytes_total ${fzvol:-0}
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}

# vim: ft=sh
