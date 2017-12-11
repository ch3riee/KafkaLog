from confluent_kafka import Consumer, KafkaError

#default.topic.config: value is a dict of topic-level configuration properties that are applied to all used topics for the instance.
c = Consumer({'bootstrap.servers': 'localhost:29092', 'group.id': 'mygroup',
              'default.topic.config': {'auto.offset.reset': 'smallest'}, 'sasl.mechanisms': 'PLAIN', 'security.protocol': 'SASL_PLAINTEXT',
                  'sasl.username': 'cherie', 'sasl.password' : 'cherie-secret'})
#Action to take when there is no initial offset in offset store or the desired offset is out of range: 'smallest','earliest' - automatically reset the offset to the smallest offset,
c.subscribe(['general'])
running = True
while running:
    msg = c.poll() #must continue calling poll or consumers will be considered dead and the partitions they are consuming will be passed to another consumer
    if not msg.error():
        type, time =  msg.timestamp()
        print('Received message: %s at time %d and partition: %d' % (msg.value().decode('utf-8'), time, msg.partition()))
    elif msg.error().code() != KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False
c.close()