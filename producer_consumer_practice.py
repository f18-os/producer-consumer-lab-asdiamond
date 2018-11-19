"""
Solving producer-consumer problem using semaphores
Credit goes to: https://gist.github.com/mahdavipanah/b8b7999e9542458a9b908112c1e63cff
@author maydavipanah
"""

import threading
import time
import random

random.seed(0)  # I am using random delays in parts of this code to make my testing more robust

stuff = [10, 20, 30, 40, 50, 60, 70, 80, 90]  # stuff to produce
index = 0  # I update this as I produce an element from the array

# Buffer size
N = 10

# Buffer init
buf = [0] * N

fill_count = threading.Semaphore(0)
empty_count = threading.Semaphore(N)

# second buffer size
M = 10
buf2 = [0] * M
fill2_count = threading.Semaphore(0)
empty2_count = threading.Semaphore(M)


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
    print(f'Produced {k} in {delay:.2f} seconds')
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
    print(f"Consumed {y} in {delay:.2f} seconds")


def consumer():
    rear = 0
    front2 = 0
    while True:
        fill_count.acquire()
        y = buf[rear]
        empty_count.release()
        consume(y)
        rear = (rear + 1) % N

        # put val onto second blocking queue
        z = y * -1 if y is not None else None  # so pythonic
        empty2_count.acquire()
        buf2[front2] = z
        fill2_count.release()
        front2 = (front2 + 1) % M
        if y is None:
            return


def consume2(z):
    delay = random.uniform(1, 2)
    time.sleep(delay)
    print(f'Consume2ed {z} in {delay:.2f} seconds')


def consumer2():
    rear = 0
    while True:
        fill2_count.acquire()
        y = buf2[rear]
        empty2_count.release()
        consume2(y)
        rear = (rear + 1) % M
        if y is None:
            return


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
consumer2_thread = threading.Thread(target=consumer2)

producer_thread.start()
consumer_thread.start()
consumer2_thread.start()
