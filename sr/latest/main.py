# encoding: utf-8
from sr.latest.meta import TaskScheduler
from sr.latest.dht import DHT
scheduler = TaskScheduler(10000)
scheduler.start()
dht1 = DHT(scheduler, "0.0.0.0", 6881, 10)
dht1.start()
dht1.auto_send_find_node()
