# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import datetime

from .. import sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "Ping"

    async def ping_cmd(self, event: sdk.Event, command: sdk.Command):
        start = datetime.datetime.now()
        await sdk.send(event.message, "🏓 <b>Calculating...</b>")
        end = datetime.datetime.now()
        await sdk.send(event.message, "🏓 Ping: <b>{}ms</b>".format((end - start).microseconds / 1000))
