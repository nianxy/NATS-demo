在当前目录下生成一个 NATS Demo Project，要求如下：

1. 用 Python 实现一个发布者进程和一个消费者进程。Python 使用 Condo 创建环境，Conda 位于 `/home/nianxingyan/miniconda3/bin/conda`
2. 生产者和消费都通过 NATS KV 存储来进行数据同步
3. NATS 分为两种部署模式，一种是 Hub 做 Server, Leaf 做 Client, 另一种是 Hub 做 Client, Leaf 做 Server
4. NATS 开启 JetStream 存储
