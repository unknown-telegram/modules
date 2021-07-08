# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import time

from telethon.tl.types import User

from .. import sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "AFK"
        self.storage: dict

    async def afk_cmd(self, event: sdk.Event, command: sdk.Command):
        if not self.storage.get("afk", False):
            self.storage.update(
                {
                    "afk": True,
                    "note": command.arg,
                    "know": [],
                    "since": time.time(),
                }
            )
            await sdk.send(
                event.message,
                "<b>I'm going AFK</b>"
                + (("\n<b>Note: </b>" + command.arg) if command.arg else ""),
            )
        else:
            await sdk.send(
                event.message,
                "<b>I'm already AFK</b>"
                + (
                    ("\n<b>Note: </b>" + self.storage["note"])
                    if self.storage["note"]
                    else ""
                ),
            )

    async def unafk_cmd(self, event: sdk.Event, command: sdk.Command):
        if not self.storage.get("afk", False):
            await sdk.send(event.message, "<b>I haven't been AFK</b>")
        else:
            spent = sdk.format_seconds(time.time() - self.storage["since"])
            self.storage.clear()
            await sdk.send(
                event.message,
                f"<b>I'm no longer AFK</b>\n<b>Time spent in AFK: </b><i>{spent}</i>",
            )

    async def incoming(self, event: sdk.Event):
        if not self.storage.get("afk", False) or not event.message.is_private:
            return

        sender = await event.message.get_sender()
        if (
            isinstance(sender, User)
            and not sender.bot
            and sender.id not in self.storage["know"]
        ):
            await sdk.send(
                event.message,
                "<b>I'm AFK for</b> <i>{}</i>{}".format(
                    sdk.format_seconds(time.time() - self.storage["since"]),
                    "\n<b>Note: </b>" + self.storage["note"]
                    if self.storage["note"]
                    else "",
                ),
            )
            self.storage["know"].append(sender.id)
