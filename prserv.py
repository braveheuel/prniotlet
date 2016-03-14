#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Christoph Heuel <mail@christoph-heuel.net>
#
# Distributed under terms of the MIT license.

"""
Printserver for thermoprinter
"""
from escpos import printer
import msgpackrpc

class IOTPrinterServer(printer.File):
    """Printer Server for the escpos."""

    def __init__(self, printer_file, columns=32):
        super().__init__(printer_file, columns)


if __name__ == "__main__":
    server = msgpackrpc.Server(IOTPrinterServer("/dev/usb/lp0"))
    server.listen(msgpackrpc.Address("0.0.0.0", 4242))
    server.start()
