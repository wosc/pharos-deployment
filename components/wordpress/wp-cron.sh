#!/bin/bash

cd "$HOME/lib"
/usr/local/bin/wp cron event run --due-now
