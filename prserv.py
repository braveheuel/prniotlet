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
from gevent.server import StreamServer
from mprpc import RPCServer


class IOTPrinterServer(RPCServer, printer.File):
    """Printer Server for the escpos."""
    pass

if __name__ == "__main__":
    server = StreamServer(('0.0.0.0', 4242), IOTPrinterServer())
    server.serve_forever()
