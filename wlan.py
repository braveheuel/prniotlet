#!/usr/bin/env python3
#
"""Print QR-Code for WLAN through python-escpos"""
import os
import io
from PIL import Image
import shutil
from escpos import printer
import qrcode
import click

PRINT_WIDTH = 384
PRINTER_FILE = "/dev/usb/lp0"


def wlanQR(ssid, security):
    # Create QR code
    qr = qrcode.QRCode()
    qr.add_data("WIFI:S:{0}:T:WPA:P:{1};;".format(ssid, security))
    image = qr.make_image(size=PRINT_WIDTH)._img
    image = image.resize((PRINT_WIDTH, PRINT_WIDTH))
    return image


@click.command()
@click.option("--ssid", required=True)
@click.option("--security", required=True)
def print_data(ssid, security):
    """Print the specified data

    :param ssid: SSID of the WLAN
    :param security: Security of that WLAN
    """
    escpos_printer = printer.File(PRINTER_FILE)
    escpos_printer.hw("init")
    escpos_printer.set(align="center", text_type="b")
    escpos_printer.block_text(ssid, 16)
    escpos_printer.text("\n")
    escpos_printer.set(align="left", text_type="normal")
    escpos_printer.image(wlanQR(ssid, security))
    escpos_printer.text("\n")
    escpos_printer.set(align="center")
    escpos_printer.text("Key:\n")
    escpos_printer.block_text(security)
    escpos_printer.text("\n\n\n\n")


if __name__ == "__main__":
    print_data()
