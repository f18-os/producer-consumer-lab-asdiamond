"""
Solving producer-consumer problem using semaphores
Credit goes to: https://gist.github.com/mahdavipanah/b8b7999e9542458a9b908112c1e63cff
@author maydavipanah
"""

import threading
import time
import random

random.seed(0)

stuff = [10, 20, 30, 40, 50, 60, 70, 80, 90]
index = 0

# Buffer size
N = 10

# Buffer init
buf = [0] * N

fill_count = threading.Semaphore(0)
empty_count = threading.Semaphore(N)


def produce():
    global index
    # return whatever is produced
    delay = random.uniform(1, 2)
    if index < len(stuff):
        k = stuff[index]
        index += 1
    else:  # we've produced everything, send signal to stop
        k = None
    time.sleep(delay)
    print(f'Produced {k} in {delay} seconds')
    return k


def producer():
    front = 0
    while True:
        x = produce()
        empty_count.acquire()
        buf[front] = x
        fill_count.release()
        front = (front + 1) % N
        if x is None:
            return


def consume(y):
    # do whatever you need to to consume 'y'
    delay = random.uniform(1, 2)
    time.sleep(delay)
    print(f"Consumed {y} in {delay} seconds")


def consumer():
    rear = 0
    while True:
        fill_count.acquire()
        y = buf[rear]
        empty_count.release()
        consume(y)
        rear = (rear + 1) % N
        if y is None:
            return


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()
