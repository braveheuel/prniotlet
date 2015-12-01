#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""
Print party gag after keypress
"""
from escpos import *
from PIL import Image
import pigpio
import logging
from datetime import date

print_width = 384
printer_file = "/dev/usb/lp0"
doc = "/home/ch/Dokumente/advent"
TASTER = 4

start_date = date(2015, 12, 1)
end_date = date(2015, 12, 24)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

ep = printer.File(printer_file)

def Umlaut_toASCII(s):
    s = s.replace('ä', "ae")
    s = s.replace('Ä', "Ae")
    s = s.replace('ö', "oe")
    s = s.replace('Ö', "Oe")
    s = s.replace('ü', "ue")
    s = s.replace('Ü', "Ue")
    s = s.replace('ß', "ss")
    return s

def print_advent_day():
    if date.today() < start_date:
        logging.info("Too early!")
        ep.hw("init")
        ep.text("\nZu frueh gedrueckt!")
        ep.text("\n\n\n\n")
        ep.flush()
    elif date.today() > end_date:
        logging.info("Too late!")
        ep.hw("init")
        ep.text("\nZu spaet gedrueckt!")
        ep.text("\n\n\n\n")
        ep.flush()
    else:
        print_day(date.today().day)

def print_day(advent_day):
    wd = "{0}/{1}".format(doc, advent_day)
    logging.info("Path: %s", wd)
    img = Image.open("{0}/{1}.png".format(wd, advent_day))
    ep.text("\n")
    ep.direct_image(img)
    ep.flush()
    logging.info("Printing image done.")
    f = open("{0}/{1}/t.txt".format(doc, advent_day), 'r')
    logging.info("Reading text...")
    x = f.readlines()
    for i in x:
        ep.block_text(Umlaut_toASCII(i))
        ep.text("\n")
    f.close()
    ep.text("\n\n\n\n")
    logging.info("Printing text done.")
    ep.flush()


def main():
    """Main Function"""
    logging.info("Starting...")
    pi = pigpio.pi()
    pi.set_mode(TASTER, pigpio.INPUT)

    logging.info("Going into loop...")
    while True:
        if pi.wait_for_edge(TASTER):
            logging.info("Taster was pressed!")
            #print_advent_day()
            print_day(1)
        else:
            logging.info("wait_for_edge timeout occurred.")
    logging.debug("Left the loop!")


if __name__ == "__main__":
    main()
