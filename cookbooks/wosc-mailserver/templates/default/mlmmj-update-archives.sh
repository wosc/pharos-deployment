#!/bin/bash
# Adapted from update-archive.sh
# <http://www.leopold.dk/~martin/mlmmj-scripts.html>
#
# Supports an additional control file
#   /etc/mlmmj/list/MYLIST/control/archivedir
# to point to the web root directory

hypermail="/usr/local/bin/hypermail"

for list in /etc/mlmmj/lists/*/; do
    if [ ! -f $list/control/archivedir ]; then
        continue;
    fi

    listname=$(basename $list)
    listdir=/var/spool/mlmmj/$listname
    wwwdir=$(cat $list/control/archivedir)

    lastindexfile=$wwwdir/last
    newindex=$(cat $listdir/index)
    lastindex=$(cat $lastindexfile)
    if [ -z "$lastindex" ]; then
        lastindex=1
    fi

    for i in `seq $lastindex $newindex`; do
        $hypermail -l $listname -i -u -d $wwwdir < $listdir/archive/$i 2>&1 | grep -v 'WARNING: locale "en_US", not supported.'
    done

    echo $newindex > $lastindexfile
    chown www-data: -R $wwwdir
done
