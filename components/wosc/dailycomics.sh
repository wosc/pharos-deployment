#!/bin/bash

DIR=/home/wosc/public_html/dailystrips
YESTERDAY=`date --date yesterday +%Y.%m.%d`

dailystrips --useragent "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0" --date $YESTERDAY --local --save --clean 7 --basedir $DIR @wosc &> /dev/null
ln -sf $DIR/dailystrips-$YESTERDAY.html $DIR/index.html
if ! grep -q DOCTYPE $DIR/index.html; then
    sed -i -e 's+<html>+<!DOCTYPE html><html lang="en">+' \
        -e's+</title>+</title>\n<link rel="shortcut icon" href="favicon.png">+' $DIR/index.html
fi
