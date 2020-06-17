import aiomas
import asyncio
from escpos import printer

class PrnIOTlet:

    def __init__(self):
        self.dummy = printer.Dummy()

    @asyncio.coroutine
    def final_print(self):
        rpc_con = yield from aiomas.rpc.open_connection(('raspberrypi', 5555), codec=aiomas.MsgPack)
        try:
            session = yield from rpc_con.remote.start_session()
            yield from rpc_con.remote.raw_data(session, self.dummy.output)
            yield from rpc_con.remote.final_print(session)
            self.dummy.clear_output()
        except Exception as e:
            print("Error occurred!", e)
        finally:
            yield from rpc_con.remote.close_session(session)
            yield from rpc_con.close()
