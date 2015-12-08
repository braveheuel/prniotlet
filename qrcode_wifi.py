#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""
Print qrcode data
"""
from escpos import *
import qrcode

print_width = 384

printer_file = "/dev/usb/lp0"

qr = qrcode.QRCode()
qr.add_data("Wifi:S:beteigeuze_gast:T:WPA:P:EiVuowoh4koe3baW;;")
qr.make(fit=True)
image = qr.make_image(size=print_width)
image = image.resize((print_width, print_width))

ep = printer.File(printer_file)
ep.hw("init")
ep.set(align="center", type="b")
ep.block_text("Gast-WiFi", 16)
ep.text("\n")
ep.set(align="left", type="normal")
ep.direct_image(image)
ep.text("\n")



