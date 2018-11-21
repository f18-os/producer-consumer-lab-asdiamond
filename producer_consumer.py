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
import base64
import numpy as np

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


# frame = 0  # really it is more like the filename, but whatever


def produce_frames(vidcap):
    # read a frame, encode it as a .jpg
    # encode it in base64, then return it
    # to be put on the queue
    success, image = vidcap.read()
    if not success:
        return None
    else:
        succ, jpg_image = cv2.imencode('.jpg', image)
        if not succ:
            # I am not really sure what to do in this situation,
            # so I will just give a halt
            return None

        # The comment says this is done in the example code to
        # make debugging easier, but I have no idea how
        # that can be true
        jpg_text = base64.b64encode(jpg_image)
        print('writing a frame into buf')
        return jpg_text


output_dir = 'frames'
clip_filename = 'clip.mp4'


def extractor():
    # open the clip_filename as a video and
    # read each frame. Encode it as a jpg image
    # for some weird reason, then encode that jpg
    # in base64, and put it on the queue
    vidcap = cv2.VideoCapture(clip_filename)

    front = 0
    while True:
        # put the jpg, base64 encoded frame into the queue
        encoded_frame = produce_frames(vidcap)
        empty_count.acquire()
        buf[front] = encoded_frame
        fill_count.release()
        front = (front + 1) % N
        if encoded_frame is None:
            # signal to S T O P
            return


def to_gray(encoded_frame):
    # decode it, convert it to
    # grayscale, then encode it
    # again and put it back
    # this is where I was having some issues
    # because it need to be jpg encoded twice

    if encoded_frame is None:
        # for stop signal
        return None

    jpg_raw = base64.b64decode(encoded_frame)
    jpg_img = np.asarray(bytearray(jpg_raw), dtype=np.uint8)

    img = cv2.imdecode(jpg_img, cv2.IMREAD_UNCHANGED)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # contrary to my initial understanding, cv2.IMREAD_UNCHANGED
    # does change the image. It does not keep its .jpg encoding
    # and needs to be encoded again.
    success, img_gray_jpg = cv2.imencode('.jpg', img_gray)

    img_gray_b64 = base64.b64encode(img_gray_jpg)

    return img_gray_b64


def middle():
    # Really more like a producer and a consumer
    # all in one thread
    # converts frames into grayscale, then puts
    # them onto the second queue because they are
    # ready to be displayed
    rear = 0
    front2 = 0
    while True:
        fill_count.acquire()
        frame = buf[rear]
        empty_count.release()
        gray_frame = to_gray(frame)
        rear = (rear + 1) % N

        # put val onto second blocking queue
        empty2_count.acquire()
        buf2[front2] = gray_frame
        fill2_count.release()
        front2 = (front2 + 1) % M
        if frame is None:
            # signal for stop
            return


frame_delay = 42  # a somewhat important number


def show(encoded_frame):
    if encoded_frame is None:
        return
    print(f'frame = {encoded_frame}')
    start_time = time.time()

    frame_d = base64.b64decode(encoded_frame)
    frame_im = np.asarray(bytearray(frame_d), dtype=np.uint8)

    img = cv2.imdecode(frame_im, cv2.IMREAD_UNCHANGED)

    cv2.imshow("Video", img)

    elapsed_time = int((time.time() - start_time) * 1000)

    wait_time = max(1, frame_delay - elapsed_time)

    if cv2.waitKey(wait_time) and 0xFF == ord("q"):
        return


def display():
    # show frames that are ready from the second queue
    rear = 0
    while True:
        fill2_count.acquire()
        encoded_frame = buf2[rear]
        empty2_count.release()
        show(encoded_frame)
        rear = (rear + 1) % M
        if encoded_frame is None:
            cv2.destroyAllWindows()
            return


extractor_thread = threading.Thread(target=extractor)
middle_thread = threading.Thread(target=middle)
display_thread = threading.Thread(target=display)

extractor_thread.start()
middle_thread.start()
display_thread.start()
