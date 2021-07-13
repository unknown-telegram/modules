# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import platform
import time

from git import Repo
from telethon import __version__

from .. import const, sdk


class Module(sdk.Module):
    def __init__(self):
        self.name: str = "System Information"
        self.init_time: float = time.time()

    def get_distribution(self) -> str:
        try:
            with open("/etc/os-release") as file:
                for line in file:
                    key, val = line.rstrip().split("=")
                    if key == "NAME":
                        return val.strip('"')
        except:
            pass
        return None

    async def info_cmd(self, event: sdk.Event, command: sdk.Command):
        _os = platform.system()
        commit = None
        try:
            commit = str(Repo(const.ROOT_DIRECTORY).commit("main"))[:10]
        except:
            pass

        info = [
            f"<b>• {key}</b>: <code>{value}</code>"
            for key, value in {
                "OS": _os,
                "Release": platform.release(),
                "Distribution": (self.get_distribution() if _os == "Linux" else None),
                "Arch": platform.machine(),
                "Python": platform.python_version(),
                "Telethon": __version__,
                "Commit": commit,
                "Uptime": sdk.format_seconds(time.time() - self.init_time),
            }.items()
            if value
        ]
        await sdk.send(event.message, "<b>System Info:</b>\n\n" + "\n".join(info))
