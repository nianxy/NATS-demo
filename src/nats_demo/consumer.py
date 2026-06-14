from __future__ import annotations

import asyncio
import signal

import nats

from nats_demo.config import load_config
from nats_demo.kv import ensure_bucket, get_jetstream


async def run() -> None:
    config = load_config(default_url="nats://localhost:4223")
    stop = asyncio.Event()

    def request_stop() -> None:
        stop.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, request_stop)

    nc = await nats.connect(
        config.nats_url,
        connect_timeout=2,
        allow_reconnect=False,
        max_reconnect_attempts=0,
    )
    try:
        js = await get_jetstream(nc, config.js_domain)
        kv = await ensure_bucket(js, config.bucket)

        print(
            "watching "
            f"bucket={config.bucket} key={config.key} "
            f"url={config.nats_url} domain={config.js_domain}",
            flush=True,
        )

        watcher = await kv.watch(config.key)
        try:
            while not stop.is_set():
                try:
                    entry = await asyncio.wait_for(watcher.updates(), timeout=0.5)
                except asyncio.TimeoutError:
                    continue

                if entry is None:
                    continue

                value = entry.value.decode() if entry.value else ""
                print(f"revision={entry.revision} value={value}", flush=True)
        finally:
            await watcher.stop()
    finally:
        await nc.drain()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
