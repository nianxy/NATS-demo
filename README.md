# NATS Demo Project

This project demonstrates NATS KV synchronization with Python publisher and consumer processes. NATS runs with JetStream enabled in two supported Hub/Leaf deployment modes:

1. Hub acts as Leaf Node server, Leaf acts as Leaf Node client.
2. Leaf acts as Leaf Node server, Hub acts as Leaf Node client.

The default demo flow writes KV data from the Hub side and reads it from the Leaf side.

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

## Run The Demo

Start the publisher in one terminal. It connects to Hub and writes JSON values into a KV bucket:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.publisher
```

Start the consumer in another terminal. It connects to Leaf but accesses the Hub JetStream domain, then prints KV updates:

```bash
/home/nianxingyan/miniconda3/bin/conda run -n nats-demo \
  python -m nats_demo.consumer
```

Expected consumer output looks like:

```text
watching bucket=demo_kv key=demo.message url=nats://localhost:4223 domain=hub
revision=1 value={"sequence":1,...}
revision=2 value={"sequence":2,...}
```

## Configuration

The Python processes read these environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `NATS_URL` | publisher: `nats://localhost:4222`, consumer: `nats://localhost:4223` | NATS client URL |
| `JS_DOMAIN` | `hub` | JetStream domain used for KV operations |
| `KV_BUCKET` | `demo_kv` | KV bucket name |
| `KV_KEY` | `demo.message` | KV key |
| `PUBLISH_INTERVAL` | `1.0` | Seconds between publisher writes |

Examples:

```bash
NATS_URL=nats://localhost:4222 JS_DOMAIN=hub \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.publisher

NATS_URL=nats://localhost:4223 JS_DOMAIN=hub \
  /home/nianxingyan/miniconda3/bin/conda run -n nats-demo python -m nats_demo.consumer
```

## Notes

NATS Leaf Node connections share the core NATS subject space, while JetStream is scoped by domain. The consumer connects through the Leaf server and uses `JS_DOMAIN=hub` so both processes operate on the same Hub KV bucket.
