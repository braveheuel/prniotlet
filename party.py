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

print_width = 384
printer_file = "/dev/usb/lp0"
logo = "/home/ch/Bilder/party-logo.png"
underline = "/home/ch/Bilder/underline.png"

def Umlaut_toASCII(s):
    s = s.replace('ä', "ae")
    s = s.replace('Ä', "Ae")
    s = s.replace('ö', "oe")
    s = s.replace('Ö', "Oe")
    s = s.replace('ü', "ue")
    s = s.replace('Ü', "Ue")
    s = s.replace('ß', "ss")
    return s

def main():
    """Main Function"""
    img = Image.open(logo)
    img_underline = Image.open(underline)
    ep = printer.File(printer_file)
    ep.hw("init")
    ep.charcode("EURO")
    ep.direct_image(img)
    ep.text("\n")
    fortprocess = subprocess.Popen("fortune -e /home/ch/Dokumente/fortune/ruhrpott /home/ch/Dokumente/fortune/ruhrpott-trilogie", stdout=subprocess.PIPE, shell=True)
    (output, err) = fortprocess.communicate()

     ## Wait for date to terminate. Get return returncode ##
    p_status = fortprocess.wait()
    if p_status == 0:
        #print(output)
        print("output: %s\n" % output)
        text = Umlaut_toASCII(output.decode("utf-8"))
        print("text: %s\n" % text)
        ep.block_text(text)
    ep.text("\n")
    ep.direct_image(img_underline)
    ep.text("\n\n\n\n")

if __name__ == "__main__":
    main()
