#! /bin/sh
#
# get_and_parse.sh
# Copyright (C) 2017 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.
#

DOKPATH="$HOME/Dokumente/advent/2017"

if [ -z "$1" ]
then
        START=1
else
        START=$1
fi

mkdir -p out/
wget --http-user=ch --ask-password https://www.heuel-web.de/owncloud/remote.php/dav/calendars/ch/adventskalender?export -O calendar.ics
if [ -f calendar.ics ]
then
        ./parseICS.py --start $START calendar.ics "$DOKPATH"
        rsync -avze ssh $DOKPATH/ raspberrypi:$DOKPATH/
else
        echo "Error Retrieving Calendar!"
        exit 1
fi
