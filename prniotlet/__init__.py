import aiomas
import asyncio
from escpos import printer
import configparser
from xdg import BaseDirectory
import os

class PrnIOTlet:

    def __init__(self, cfg_file=None):
        self.proxy = printer.Dummy()
        self.config = configparser.ConfigParser()
        if cfg_file:
            self.config.read(cfg_file)
        else:
            self.config.read(os.path.join(BaseDirectory.xdg_config_home, "prniotlet", "config"))

    async def _final_print(self):
        rpc_con = await aiomas.rpc.open_connection((self.config["connection"]["host"],
                                                   self.config.getint("connection", "port", fallback=5555)),
                                                   codec=aiomas.MsgPack)
        try:
            session = await rpc_con.remote.start_session()
            await rpc_con.remote.raw_data(session, self.proxy.output)
            await rpc_con.remote.final_print(session)
            self.proxy.clear()
        except Exception as e:
            print("Error occurred!", e)
        finally:
            await rpc_con.remote.close_session(session)
            await rpc_con.close()

    def final_print(self):
        aiomas.run(self._final_print())
