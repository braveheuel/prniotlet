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
from escpos import printer
from PIL import Image
import pigpio
import logging
from datetime import date
from docopt import docopt
import pathlib

PRINT_WIDTH = 384
PRINTER_FILE = "/dev/usb/lp0"
DOCUMENT_ROOT = "/home/ch/Dokumente/advent"
TASTER = 4

START_DATE = date(2015, 12, 1)
END_DATE = date(2015, 12, 24)

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

ESCPOS_PRINTER = printer.File(PRINTER_FILE)

def umlaut_to_ASCII(text):
    """Replace umlaut with ascii compliant chars

    :param text: String to replace
    :returns: text with replaced characters
    """
    text = text.replace('ä', "ae")
    text = text.replace('Ä', "Ae")
    text = text.replace('ö', "oe")
    text = text.replace('Ö', "Oe")
    text = text.replace('ü', "ue")
    text = text.replace('Ü', "Ue")
    text = text.replace('ß', "ss")
    return text


def print_advent_day():
    """Evaluate if print date is in date range"""
    if date.today() < START_DATE:
        logging.info("Too early!")
        ESCPOS_PRINTER.hw("init")
        ESCPOS_PRINTER.text("\nZu frueh gedrueckt!")
        ESCPOS_PRINTER.text("\n\n\n\n")
        ESCPOS_PRINTER.flush()
    elif date.today() > END_DATE:
        logging.info("Too late!")
        ESCPOS_PRINTER.hw("init")
        ESCPOS_PRINTER.text("\nZu spaet gedrueckt!")
        ESCPOS_PRINTER.text("\n\n\n\n")
        ESCPOS_PRINTER.flush()
    else:
        print_day(date.today().day)


def print_day(advent_day):
    """Print specified day

    :param advent_day: Number of date to print
    """
    logging.info("Starting with advent day %s", advent_day)
    img = Image.open("{0}/{1}.png".format(DOCUMENT_ROOT, advent_day))
    ESCPOS_PRINTER.image(img)
    ESCPOS_PRINTER.text("\n")
    ESCPOS_PRINTER.flush()
    logging.info("Printing image done.")
    filename = "{0}/{1}.txt".format(DOCUMENT_ROOT, advent_day)
    if pathlib.Path(filename).exists():
        text_file = open(filename, 'r')
        logging.info("Reading text...")
        lines = text_file.readlines()
        for i in lines:
            if i == "\n":
                ESCPOS_PRINTER.text("\n")
            else:
                ESCPOS_PRINTER.block_text(umlaut_to_ASCII(i))
                ESCPOS_PRINTER.text("\n")
        text_file.close()
        logging.info("Printing text done.")
    else:
        logging.info("No text found!")

    ESCPOS_PRINTER.text("\n\n\n\n")
    logging.info("Printing done.")
    ESCPOS_PRINTER.flush()


def main(args):
    """Main Function

    :param args: Arguments found by docopt
    """
    logging.info("Starting...")
    pi_instance = pigpio.pi()
    pi_instance.set_mode(TASTER, pigpio.INPUT)

    if args['<day>']:
        print_day(args["<day>"])
    else:
        logging.info("Going into loop...")
        while True:
            if pi_instance.wait_for_edge(TASTER):
                logging.info("Taster was pressed!")
                print_advent_day()
        logging.debug("Left the loop!")


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments)
