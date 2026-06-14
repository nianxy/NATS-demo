from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from nats.errors import TimeoutError as NatsTimeoutError

from nats_demo.config import load_rpc_config
from nats_demo.runtime import connect, install_signal_handlers


async def run() -> None:
    config = load_rpc_config(default_url="nats://localhost:4222")
    stop = asyncio.Event()
    install_signal_handlers(stop)

    nc = await connect(config.nats_url)
    try:
        sequence = 0
        print(
            "rpc requesting "
            f"subject={config.subject} url={config.nats_url} "
            f"timeout={config.request_timeout}",
            flush=True,
        )

        while not stop.is_set():
            sequence += 1
            payload = {
                "sequence": sequence,
                "requested_at": datetime.now(timezone.utc).isoformat(),
                "source": "hub-rpc-requester",
            }

            try:
                msg = await nc.request(
                    config.subject,
                    json.dumps(payload).encode(),
                    timeout=config.request_timeout,
                )
                print(
                    f"subject={config.subject} request={json.dumps(payload)} "
                    f"reply={msg.data.decode()}",
                    flush=True,
                )
            except NatsTimeoutError:
                print(
                    f"subject={config.subject} request={json.dumps(payload)} timeout",
                    flush=True,
                )

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
