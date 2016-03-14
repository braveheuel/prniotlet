#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 ch <ch@silversurfer.deepspace.local>
#
# Distributed under terms of the MIT license.

"""

"""
import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("raspberrypi", 4242))
client.call("text", "asdasdsa")
