#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue


def extract_frames(file_name, output_buffer):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(file_name)

    # read first image
    success, image = vidcap.read()

    print(f"Reading frame {count} {success} ")
    while success:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        # encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        output_buffer.put(jpgAsText)

        success, image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print("Frame extraction complete")


def display_frames(input_buffer):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while not input_buffer.empty():
        # get the next frame
        frameAsText = input_buffer.get()

        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

        # get a jpg encoded frame
        img = cv2.imdecode(jpgImage, cv2.IMREAD_UNCHANGED)

        print(f"Displaying frame {count}")

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()


# filename of clip to load
filename = 'clip.mp4'

# shared queue  
extractionQueue = queue.Queue()

# extract the frames
extract_frames(filename, extractionQueue)

# display the frames
display_frames(extractionQueue)
