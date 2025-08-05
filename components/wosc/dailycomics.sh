#!/bin/bash

DIR=/home/wosc/public_html/dailystrips
TODAY=`date --date today +%Y-%m-%d`

/usr/local/bin/dailycomics --config ~/.dot/x11/dailystrips.yaml --folder $DIR
ln -sf $DIR/dailystrips-$TODAY.html $DIR/index.html
find $DIR -mtime 7 -not -name favicon.png | xargs rm -f
