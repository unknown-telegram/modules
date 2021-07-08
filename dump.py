# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

from .. import sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "Dump"

    async def dump_cmd(self, event: sdk.Event, command: sdk.Command):
        message = (
            (await event.message.get_reply_message())
            if event.message.is_reply
            else event.message
        )
        await sdk.send(
            event.message,
            f"<code>{sdk.escape_html(message.stringify())}</code>",
        )
