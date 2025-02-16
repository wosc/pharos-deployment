#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

for filename in $(find ./components -name requirements.txt); do
    directory=$(dirname $filename)
    cd $DIR/$directory
    echo $directory
    cmd=$(sed -ne 's/^# *\(pip-compile.*\)$/\1/p' requirements.txt)
    $cmd --quiet --upgrade
done
