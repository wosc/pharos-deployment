#!/bin/bash
# https://gitlab.com/MathieuMD/node_exporter-exim

DEST=/srv/prometheus/node/mail_eximstats.prom

unit2val() {
    v=$(echo $1|tr -d '[A-Z]')
    u=$(echo $1|tr -d '[0-9]')
    case $u in
        KB) v=$((v*1024));;
        MB) v=$((v*1024**2));;
        GB) v=$((v*1024**3));;
        TB) v=$((v*1024**4));;
        PB) v=$((v*1024**5));;
    esac
    echo $v
}

# Timestamp is an int64 (milliseconds since epoch)
TS="$(date +%s%N |cut -b1-13)"

ES="$(/usr/sbin/eximstats -h0 -nr -ne -t0 /var/log/exim4/mainlog 2>/dev/null)"
#Grand total summary
#-------------------
#                                                                  At least one address
#  TOTAL               Volume   Messages Addresses     Hosts      Delayed       Failed
#  Received             738MB       5129                  28     966 18.8%      8  0.2%
#  Delivered            823MB       5703     10960        60
#  Rejects                           512                  10

Match="Received"
Received_VOL="$(  echo "$ES" |awk "/^  $Match /{print \$2}")"
Received_MSG="$(  echo "$ES" |awk "/^  $Match /{print \$3}")"
Received_HOSTS="$(echo "$ES" |awk "/^  $Match /{print \$4}")"

Match="Delivered"
Delivered_VOL="$(  echo "$ES" |awk "/^  $Match /{print \$2}")"
Delivered_MSG="$(  echo "$ES" |awk "/^  $Match /{print \$3}")"
Delivered_ADDR="$( echo "$ES" |awk "/^  $Match /{print \$4}")"
Delivered_HOSTS="$(echo "$ES" |awk "/^  $Match /{print \$5}")"

Match="Rejects"
Rejects_MSG="$(  echo "$ES" |awk "/^  $Match /{print \$2}")"
Rejects_HOSTS="$(echo "$ES" |awk "/^  $Match /{print \$3}")"

Match="Temp Rejects"
TmpRejects_MSG="$(  echo "$ES" |awk "/^  $Match /{print \$3}")"
TmpRejects_HOSTS="$(echo "$ES" |awk "/^  $Match /{print \$4}")"

echo "
# HELP mail_received_total The total number of messages received.
# TYPE mail_received_total counter
mail_received_total ${Received_MSG:-0} $TS
# TYPE mail_received_bytes_total counter
mail_received_bytes_total $(unit2val ${Received_VOL:-0}) $TS
# TYPE mail_received_hosts_total counter
mail_received_hosts_total ${Received_HOSTS:-0} $TS

# HELP mail_delivered_total The total number of messages delivered.
# TYPE mail_delivered_total counter
mail_delivered_total ${Delivered_MSG:-0} $TS
# TYPE mail_delivered_bytes_total counter
mail_delivered_bytes_total $(unit2val ${Delivered_VOL:-0}) $TS
# TYPE mail_delivered_addresses_total counter
mail_delivered_addresses_total ${Delivered_ADDR:-0} $TS
# TYPE mail_delivered_hosts_total counter
mail_delivered_hosts_total ${Delivered_HOSTS:-0} $TS

# HELP mail_rejects_total The total number of messages rejected.
# TYPE mail_rejects_total counter
mail_rejects_total ${Rejects_MSG:-0} $TS
# TYPE mail_rejects_hosts_total counter
mail_rejects_hosts_total ${Rejects_HOSTS:-0} $TS

# HELP mail_rejects_tmp_total The total number of messages rejected temporarily.
# TYPE mail_rejects_tmp_total counter
mail_rejects_tmp_total ${TmpRejects_MSG:-0} $TS
# TYPE mail_rejects_tmp_hosts_total counter
mail_rejects_tmp_hosts_total ${TmpRejects_HOSTS:-0} $TS

# HELP mail_fatal_errors_total Number of lines in the paniclog file
# TYPE mail_fatal_errors_total counter
mail_fatal_errors_total $(wc -l < /var/log/exim4/paniclog) $TS
" > ${DEST}.tmp
mv -f ${DEST}{.tmp,}

# vim: ft=sh
