from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from nats_demo.config import load_rpc_config
from nats_demo.runtime import connect, install_signal_handlers


async def run() -> None:
    config = load_rpc_config(default_url="nats://localhost:4223")
    stop = asyncio.Event()
    install_signal_handlers(stop)

    nc = await connect(config.nats_url)
    try:
        sub = await nc.subscribe(config.subject)
        await nc.flush()
        print(
            f"rpc responding subject={config.subject} url={config.nats_url}",
            flush=True,
        )

        while not stop.is_set():
            try:
                msg = await sub.next_msg(timeout=0.5)
            except asyncio.TimeoutError:
                continue

            request = msg.data.decode()
            payload = {
                "status": "ok",
                "responder": "leaf-rpc-responder",
                "received": request,
                "replied_at": datetime.now(timezone.utc).isoformat(),
            }
            await msg.respond(json.dumps(payload).encode())
            print(
                f"subject={msg.subject} request={request} reply={json.dumps(payload)}",
                flush=True,
            )
    finally:
        await nc.drain()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
