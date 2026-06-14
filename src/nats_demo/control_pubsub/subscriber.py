from __future__ import annotations

import asyncio

from nats_demo.config import load_control_config
from nats_demo.runtime import connect, install_signal_handlers


async def run() -> None:
    config = load_control_config(default_url="nats://localhost:4223")
    stop = asyncio.Event()
    install_signal_handlers(stop)

    nc = await connect(config.nats_url)
    try:
        sub = await nc.subscribe(config.subject)
        await nc.flush()
        print(
            f"control subscribing subject={config.subject} url={config.nats_url}",
            flush=True,
        )

        while not stop.is_set():
            try:
                msg = await sub.next_msg(timeout=0.5)
            except asyncio.TimeoutError:
                continue

            print(
                f"subject={msg.subject} value={msg.data.decode()}",
                flush=True,
            )
    finally:
        await nc.drain()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
