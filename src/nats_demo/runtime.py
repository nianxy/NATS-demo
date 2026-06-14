from __future__ import annotations

import asyncio
import signal

import nats


async def connect(url: str):
    return await nats.connect(
        url,
        connect_timeout=2,
        allow_reconnect=False,
        max_reconnect_attempts=0,
    )


def install_signal_handlers(stop: asyncio.Event) -> None:
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)
