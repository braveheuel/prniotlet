#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ch <christoph@heuel-web.de>
#
# Distributed under terms of the MIT license.

"""
aimoas print server
"""
from escpos import printer, config
import aiomas
import uuid


class SessionException(Exception):
    """
    Exception Class showing another that an other session is active/in use
    """
    pass


class ESCPOSServer(printer.Dummy):
    router = aiomas.rpc.Service()
    printer_real = config.Config().printer()
    active_session = None

    def __init__(self):
        super().__init__()

    @aiomas.expose
    def start_session(self):
        """
        Start a Session for the server. If a session is active, no other
        requests can be done
        """
        if not ESCPOSServer.active_session:
            ESCPOSServer.active_session = uuid.uuid4().__str__()
            print("Starting Session ", ESCPOSServer.active_session)
            return ESCPOSServer.active_session
        else:
            raise SessionException("Another Session is active")

    @aiomas.expose
    def close_session(self, session_id):
        """
        Close a existing session
        """
        if session_id == ESCPOSServer.active_session:
            print("Closing Session ", ESCPOSServer.active_session)
            ESCPOSServer.active_session = None
        else:
            print("Wrong Session:", session_id, "Active One:",
                  ESCPOSServer.active_session)
            raise SessionException("Wrong Session")

    @aiomas.expose
    def raw_data(self, session_id, msg):
        """
        Print raw data to the Dummy Device
        """
        if session_id == ESCPOSServer.active_session:
            print("Receiving Raw Data")
            super()._raw(msg.encode())
        else:
            print("Wrong Session:", session_id, "Active One:",
                  ESCPOSServer.active_session)
            raise SessionException("Wrong Session")

    @aiomas.expose
    def final_print(self, session_id):
        """
        Print to the actual server
        """
        if session_id == ESCPOSServer.active_session:
            print("Printing...")
            ESCPOSServer.printer_real._raw(self.output)
        else:
            print("Wrong Session:", session_id, "Active One:",
                  ESCPOSServer.active_session)
            raise SessionException("Wrong Session")


if __name__ == "__main__":
    server = aiomas.run(aiomas.rpc.start_server(('0.0.0.0', 5555),
                                                ESCPOSServer()))
    aiomas.run(server.wait_closed())
