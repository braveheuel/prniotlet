#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""
Print party gag after keypress
Usage:
    advent.py [<day>]
"""
from escpos import *
from PIL import Image
import pigpio
import logging
from datetime import date
from docopt import docopt
import pathlib

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
    logging.info("Starting with advent day %s", advent_day)
    img = Image.open("{0}/{1}.png".format(doc, advent_day))
    ep.direct_image(img)
    ep.text("\n")
    ep.flush()
    logging.info("Printing image done.")
    filename = "{0}/{1}.txt".format(doc, advent_day)
    if pathlib.Path(filename).exists():
        f = open(filename, 'r')
        logging.info("Reading text...")
        x = f.readlines()
        for i in x:
            if i == "\n":
                ep.text("\n")
            else:
                ep.block_text(Umlaut_toASCII(i))
                ep.text("\n")
        f.close()
        logging.info("Printing text done.")
    else:
        logging.info("No text found!")

    ep.text("\n\n\n\n")
    logging.info("Printing done.")
    ep.flush()


def main(args):
    """Main Function"""
    logging.info("Starting...")
    pi = pigpio.pi()
    pi.set_mode(TASTER, pigpio.INPUT)

    if args['<day>']:
        print_day(args["<day>"])
    else:
        logging.info("Going into loop...")
        while True:
            if pi.wait_for_edge(TASTER):
                logging.info("Taster was pressed!")
                print_advent_day()
        logging.debug("Left the loop!")


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
