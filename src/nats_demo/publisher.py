from __future__ import annotations

import asyncio
import json
import signal
from datetime import datetime, timezone

import nats

from nats_demo.config import load_config
from nats_demo.kv import ensure_bucket, get_jetstream


async def run() -> None:
    config = load_config(default_url="nats://localhost:4222")
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
        sequence = 0

        print(
            "publishing "
            f"bucket={config.bucket} key={config.key} "
            f"url={config.nats_url} domain={config.js_domain}",
            flush=True,
        )

        while not stop.is_set():
            sequence += 1
            payload = {
                "sequence": sequence,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "source": "hub-publisher",
            }
            revision = await kv.put(config.key, json.dumps(payload).encode())
            print(f"revision={revision} value={json.dumps(payload)}", flush=True)

            try:
                await asyncio.wait_for(stop.wait(), timeout=config.publish_interval)
            except asyncio.TimeoutError:
                pass
    finally:
        await nc.drain()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
