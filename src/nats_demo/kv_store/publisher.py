from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from nats_demo.config import load_config
from nats_demo.kv import ensure_bucket, get_jetstream
from nats_demo.runtime import connect, install_signal_handlers


async def run() -> None:
    config = load_config(default_url="nats://localhost:4222")
    stop = asyncio.Event()
    install_signal_handlers(stop)

    nc = await connect(config.nats_url)
    try:
        js = await get_jetstream(nc, config.js_domain)
        kv = await ensure_bucket(js, config.bucket)
        sequence = 0

        print(
            "kv publishing "
            f"bucket={config.bucket} key={config.key} "
            f"url={config.nats_url} domain={config.js_domain}",
            flush=True,
        )

        while not stop.is_set():
            sequence += 1
            payload = {
                "sequence": sequence,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "source": "hub-kv-publisher",
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
