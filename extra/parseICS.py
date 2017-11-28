#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 cheuel <christoph.heuel@lairdtech.com>

"""
Adventskalendar Parser
"""
import icalendar
import click
from os import path

def write_file(day, directory, text):
    if text:
        with open(path.join(directory, "{0}.txt".format(day)), 'wb') as txtfile:
            txtfile.write(text.encode(encoding='UTF-8'))

def handle_event(x, lower_limit, directory):
    a_day = x['dtstart'].dt.day
    if a_day >= lower_limit:
        a_summary = x['summary']
        if 'DESCRIPTION' in x:
            a_description = x['description']
        else:
            a_description = None
        if 'location' in x:
            a_loc = x['location']
        else:
            a_loc = None

        print("{0}: {1}\n{2}\n{3}".format(a_day, a_summary, a_description, a_loc))
        print("------------------------")
        write_file(a_day, directory, a_description)

@click.command()
@click.argument("icsfile", type=click.File('rb'))
@click.argument("directory", type=click.Path(exists=True))
@click.option("--start", default=1)
def main(icsfile, directory, start):
    ics = icalendar.Calendar.from_ical(icsfile.read())
    for i in ics.walk():
        if type(i) == icalendar.Event:
            handle_event(i, start, directory)

if __name__ == "__main__":
    main()
