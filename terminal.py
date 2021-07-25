# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import asyncio

import chardet

from .. import sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "Terminal"

    def decode(self, data: bytes) -> str:
        encoding = chardet.detect(data)["encoding"]
        result = "No data received"
        if encoding is not None:
            result = data.decode(encoding).strip()
        return result

    async def run(self, event: sdk.Event, command: str):
        sh = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await sdk.send(event.message, "<b>Process is running...</b>")
        await sh.wait()

        await sdk.send(
            event.message,
            "<b>Command: </b><code>{}</code>\n<b>Status code: </b><code>{}</code>\n\n<b>Output:</b>\n<code>{}</code>\n\n<b>Errors:</b>\n<code>{}</code>".format(
                sdk.escape_html(command), sh.returncode,
                sdk.escape_html(self.decode(await sh.stdout.read())),
                sdk.escape_html(self.decode(await sh.stderr.read()))
            ),
        )

    async def neofetch_cmd(self, event: sdk.Event, command: sdk.Command):
        await self.run(event, "neofetch --stdout")

    async def terminal_cmd(self, event: sdk.Event, command: sdk.Command):
        if command.arg == "":
            await sdk.send(event.message, "<b>You need to specify command.</b>")
            return

        await self.run(event, command.arg)
