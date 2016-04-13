#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""

"""
from mprpc import RPCClient


client = RPCClient('raspberrypi', 4242)
client.call('hw', b"INIT")
client.call('text', b"blaaa ")
client.call('text', b"blaaa")
client.call('text', b"\n")
client.call('flush')
