#!/usr/bin/env python3
#
"""Print QR-Code for WLAN through python-escpos"""
from escpos import printer
import click


def wlanQR_prn(prn, ssid, security):
    prn.qr("WIFI:S:{0}:T:WPA:P:{1};;".format(ssid, security), size=12)


@click.command()
@click.option("--ssid", required=True)
@click.option("--security", required=True)
def print_data(ssid, security):
    """Print the specified data

    :param ssid: SSID of the WLAN
    :param security: Security of that WLAN
    """
    escpos_printer_real = printer.Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x02)
    escpos_printer = printer.Dummy()
    escpos_printer.hw("init")
    escpos_printer.set(align="center", bold=True, width=2, height=2)
    escpos_printer.block_text(ssid, columns=16)
    escpos_printer.print_and_feed(1)
    wlanQR_prn(escpos_printer, ssid, security)
    escpos_printer.print_and_feed()
    escpos_printer.set(align="center", bold=False, width=1, height=1)
    escpos_printer.text("Key:\n")
    escpos_printer.block_text(security, font='a', columns=16)
    escpos_printer.print_and_feed(4)
    escpos_printer_real._raw(escpos_printer.output)


if __name__ == "__main__":
    print_data()
