import aio_pika

class MessageBroker:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.config.get('rabbitmq_url'))
        self.channel = await self.connection.channel()

    async def publish(self, routing_key, message):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=routing_key
        )

    async def consume(self, queue_name, callback):
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback)

    async def close(self):
        await self.connection.close()
