#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""
Printserver for thermoprinter
"""
from escpos import *
import zerorpc

class IOTPrinterServer(printer.file):
    """Printer Server for the escpos."""

    def __init__(self, printer_file, columns=32):
        super().__init__(printer_file, columns)



if __name__ == "__main__":
    srv = zerorpc.Server(IOTPrinterServer("/dev/usb/lp0"))
    srv.bind("tcp://0.0.0.0:4242")
    srv.run()
