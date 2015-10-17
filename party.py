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
import subprocess
import pigpio
import logging

print_width = 384
printer_file = "/dev/usb/lp0"
logo = "/home/ch/Bilder/party-logo.png"
underline = "/home/ch/Bilder/underline.png"
TASTER = 4

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def Umlaut_toASCII(s):
    s = s.replace('ä', "ae")
    s = s.replace('Ä', "Ae")
    s = s.replace('ö', "oe")
    s = s.replace('Ö', "Oe")
    s = s.replace('ü', "ue")
    s = s.replace('Ü', "Ue")
    s = s.replace('ß', "ss")
    return s

def print_note(ep, header, footer):
    logging.info("Call fortune...")
    fortprocess = subprocess.Popen("fortune -e /home/ch/Dokumente/fortune/ruhrpott /home/ch/Dokumente/fortune/ruhrpott-trilogie", stdout=subprocess.PIPE, shell=True)
    (output, err) = fortprocess.communicate()

     ## Wait for date to terminate. Get return returncode ##
    p_status = fortprocess.wait()
    logging.info("fortune finished")
    if p_status == 0:
        ep.hw("init")
        logging.debug("Printing header...")
        ep.direct_image(header)
        ep.text("\n")
        text = Umlaut_toASCII(output.decode("utf-8"))
        logging.info("Printing text")
        ep.block_text(text)
        ep.text("\n")
        logging.debug("Printing footer")
        ep.direct_image(footer)
        ep.text("\n\n\n\n")
        ep.flush()
        logging.info("Printing finished")
    else:
        ep.text("Fehler: Kein Spruch verfuegbar")
        ep.text("\n\n\n\n")


def main():
    """Main Function"""
    logging.info("Starting... Loading Logo...")
    img = Image.open(logo)
    logging.info("Loading footer...")
    img_underline = Image.open(underline)
    ep = printer.File(printer_file)
    pi = pigpio.pi()
    pi.set_mode(TASTER, pigpio.INPUT)

    logging.info("Going into loop...")
    while True:
        if pi.wait_for_edge(TASTER):
            logging.info("Taster was pressed!")
            print_note(ep, img, img_underline)
        else:
            logging.info("wait_for_edge timeout occurred.")
    logging.debug("Left the loop!")


if __name__ == "__main__":
    main()
