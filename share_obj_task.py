import multiprocessing as mp
import vineyard

import numpy as np
import pandas as pd

socket = '/tmp/vineyard.sock'

def produce(name):
   client = vineyard.connect(socket)
   client.put(pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD')),
              persist=True, name=name)

def consume(name):
   client = vineyard.connect(socket)
   print(client.get(name=name).sum())

if __name__ == '__main__':
   name = 'dataset'

   producer = mp.Process(target=produce, args=(name,))
   producer.start()
   consumer = mp.Process(target=consume, args=(name,))
   consumer.start()

   producer.join()
   consumer.join()