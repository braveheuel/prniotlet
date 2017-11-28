#! /bin/sh
#
# get_and_parse.sh
# Copyright (C) 2017 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.
#

mkdir -p out/
wget --http-user=ch --ask-password https://www.heuel-web.de/owncloud/remote.php/dav/calendars/ch/adventskalender?export -O calendar.ics
./parseICS.py --start $1 calendar.ics out/
