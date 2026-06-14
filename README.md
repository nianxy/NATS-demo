# NATS Demo Project

This project demonstrates three NATS communication patterns with Python processes:

- JetStream KV Store state synchronization.
- Core NATS Pub/Sub control messages.
- Core NATS Request-Reply, initiated by Hub and handled by Leaf.

NATS runs with JetStream enabled in two supported Hub/Leaf deployment modes:

1. Hub acts as Leaf Node server, Leaf acts as Leaf Node client.
2. Leaf acts as Leaf Node server, Hub acts as Leaf Node client.

The default flow connects Hub-side processes to `nats://localhost:4222` and Leaf-side processes to `nats://localhost:4223`.

## Requirements

- Docker with `docker compose`
- Conda at `/home/nianxingyan/miniconda3/bin/conda`

## Setup

```bash
./scripts/setup_env.sh
```

Activate the environment:

```bash
source /home/nianxingyan/miniconda3/etc/profile.d/conda.sh
conda activate nats-demo
```

If you do not want to activate the shell, use `conda run` as shown below.

## Start NATS

Mode 1: Hub is the Leaf Node server, Leaf is the Leaf Node client.

```bash
./scripts/up_hub_server.sh
```

Mode 2: Leaf is the Leaf Node server, Hub is the Leaf Node client.

```bash
./scripts/up_leaf_server.sh
```

Stop either mode:

```bash
./scripts/down.sh
```

Both modes expose:

- Hub client URL: `nats://localhost:4222`
- Leaf client URL: `nats://localhost:4223`
- Hub JetStream domain: `hub`
- Leaf JetStream domain: `leaf`

## KV Store Demo

Start the publisher in one terminal. It connects to Hub and writes JSON values into a KV bucket:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.kv_store.publisher
```

Start the consumer in another terminal. It connects to Leaf but accesses the Hub JetStream domain, then prints KV updates:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.kv_store.consumer
```

Expected consumer output looks like:

```text
kv watching bucket=demo_kv key=demo.message url=nats://localhost:4223 domain=hub
revision=1 value={"sequence":1,...}
revision=2 value={"sequence":2,...}
```

The old module names still work as KV aliases:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.publisher
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.consumer
```

## Pub/Sub Control Demo

Start the Leaf subscriber first:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.control_pubsub.subscriber
```

Start the Hub publisher in another terminal:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.control_pubsub.publisher
```

Expected subscriber output looks like:

```text
control subscribing subject=control.leaf.command url=nats://localhost:4223
subject=control.leaf.command value={"sequence":1,"command":"reload",...}
```

## Request-Reply Demo

Start the Leaf responder first:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.request_reply.responder
```

Start the Hub requester in another terminal:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.request_reply.requester
```

Expected requester output looks like:

```text
rpc requesting subject=rpc.leaf.status url=nats://localhost:4222 timeout=2.0
subject=rpc.leaf.status request={...} reply={"status":"ok",...}
```

## Configuration

The Python processes read these environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `NATS_URL` | Hub processes: `nats://localhost:4222`, Leaf processes: `nats://localhost:4223` | NATS client URL |
| `JS_DOMAIN` | `hub` | JetStream domain used for KV operations |
| `KV_BUCKET` | `demo_kv` | KV bucket name |
| `KV_KEY` | `demo.message` | KV key |
| `CONTROL_SUBJECT` | `control.leaf.command` | Pub/Sub control subject |
| `CONTROL_COMMAND` | `reload` | Command value used by the control publisher |
| `RPC_SUBJECT` | `rpc.leaf.status` | Request-Reply subject |
| `REQUEST_TIMEOUT` | `2.0` | Seconds to wait for an RPC reply |
| `PUBLISH_INTERVAL` | `1.0` | Seconds between publisher writes |

Examples:

```bash
NATS_URL=nats://localhost:4222 JS_DOMAIN=hub \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.kv_store.publisher

NATS_URL=nats://localhost:4223 JS_DOMAIN=hub \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.kv_store.consumer

CONTROL_COMMAND=restart \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.control_pubsub.publisher

REQUEST_TIMEOUT=5 \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.request_reply.requester
```

## Notes

NATS Leaf Node connections share the Core NATS subject space, so Pub/Sub and Request-Reply messages can cross Hub and Leaf through normal subjects. JetStream is scoped by domain. The KV consumer connects through the Leaf server and uses `JS_DOMAIN=hub` so both KV processes operate on the same Hub KV bucket.
