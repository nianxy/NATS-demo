from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from nats_demo.config import load_control_config
from nats_demo.runtime import connect, install_signal_handlers


async def run() -> None:
    config = load_control_config(default_url="nats://localhost:4222")
    stop = asyncio.Event()
    install_signal_handlers(stop)

    nc = await connect(config.nats_url)
    try:
        sequence = 0
        print(
            "control publishing "
            f"subject={config.subject} command={config.command} url={config.nats_url}",
            flush=True,
        )

        while not stop.is_set():
            sequence += 1
            payload = {
                "sequence": sequence,
                "command": config.command,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "source": "hub-control-publisher",
            }
            await nc.publish(config.subject, json.dumps(payload).encode())
            await nc.flush()
            print(f"subject={config.subject} value={json.dumps(payload)}", flush=True)

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
