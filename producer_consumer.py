"""
Solving producer-consumer problem using semaphores
Credit goes to: https://gist.github.com/mahdavipanah/b8b7999e9542458a9b908112c1e63cff
@author maydavipanah
"""

import threading
import time
import random
import cv2
import os


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


count = 0  # really it is more like the filename, but whatever
def produce(vidcap):
    global count
    success, image = vidcap.read()
    if not success:
        return None
    else:
        print(f'writing frame {count}')
        cv2.imwrite(f'{output_dir}/frame_{count:04d}.jpg', image)
        count += 1
        return count


output_dir = 'frames'
clip_filename = 'clip.mp4'
def producer():
    vidcap = cv2.VideoCapture(clip_filename)

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} didn't exist, creating")
        os.makedirs(output_dir)

    front = 0
    while True:
        # put the number that represents the frame number and filename into the queue
        # the file will be in f'{output_dir}/frame_{count:04d}.jpg
        x = produce(vidcap)
        empty_count.acquire()
        buf[front] = x
        fill_count.release()
        front = (front + 1) % N
        if x is None:
            # signal to S T O P
            return


def consume(y):
    # y is the frame number
    # write it into a new file that is the grayscale
    # conversion of the frame
    print(f'converting frame {y}')
    in_filename = f'{output_dir}/frame_{y:04d}.jpg'
    in_frame = cv2.imread(in_filename, cv2.IMREAD_COLOR)

    grayscale_frame = cv2.cvtColor(in_frame, cv2.COLOR_BGR2GRAY)
    out_filename = f'{output_dir}/grayscale_{y:04d}.jpg'

    cv2.imwrite(out_filename, grayscale_frame)


def consumer():
    # Really more like a producer and a consumer
    # converts frames into grayscale, then puts
    # them onto the second queue because they are
    # ready to be displayed
    rear = 0
    front2 = 0
    while True:
        # y is that count variable, the frame number
        fill_count.acquire()
        y = buf[rear]
        empty_count.release()
        consume(y)
        rear = (rear + 1) % N

        # put val onto second blocking queue
        empty2_count.acquire()
        buf2[front2] = y
        fill2_count.release()
        front2 = (front2 + 1) % M
        if y is None:
            # signal for stop
            return


frame_delay = 42  # a somewhat important number
def consume2(z):
    start_time = time.time()

    frame_filename = f'{output_dir}/grayscale_{z:04d}.jpg'
    frame = cv2.imread(frame_filename)

    cv2.imshow("Video", frame)

    elapsed_time = int((time.time() - start_time) * 1000)

    wait_time = max(1, frame_delay - elapsed_time)

    if cv2.waitKey(wait_time) and 0xFF == ord("q"):
        return



def consumer2():
    rear = 0
    while True:
        fill2_count.acquire()
        z = buf2[rear]
        empty2_count.release()
        consume2(z)
        rear = (rear + 1) % M
        if z is None:
            cv2.destroyAllWindows()
            return


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
consumer2_thread = threading.Thread(target=consumer2)

producer_thread.start()
consumer_thread.start()
consumer2_thread.start()
