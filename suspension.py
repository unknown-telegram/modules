# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import time

from .. import sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "Suspension"

    async def suspend_cmd(self, event: sdk.Event, command: sdk.Command):
        if command.arg == "":
            await sdk.send(event.message, "<b>You need to specify suspension time (in seconds).</b>")
            return

        try:
            seconds = int(command.arg)
            await sdk.send(
                event.message, f"<b>Bot is sleeping for {seconds} seconds 😴</b>"
            )
            time.sleep(seconds)
        except ValueError:
            await sdk.send(event.message, "<b>Invalid suspension time.</b>")
