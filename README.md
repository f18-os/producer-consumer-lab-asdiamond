# My Producer Consumer Lab
## producer_consumer.py

* I used counting semaphores in pythons 'threading' library to implement a multithreaded 
video player. 

* One thread reads frames from the .mp4 and encodes them as .jpg's in base64
and throws them onto a blocking queue. 

* Another thread takes from this queue, decodes the images, converts them to grayscale,
then puts them onto another queue. 

* A third thread reads from this second queue and displays the grayscale images.

* When there aren't any more frames left, the first thread will throw a 'None' onto the queue,
which will cause all of the other threads to very cleanly stop at the end of the video.

The video plays pretty smoothly, and with no artifacts. 

I also did not use any classes or anything, the code is fairly simple.
I made a 'Contributors.md' file listing my references. I took some inspiration from
very simple code, but in general, any other code here is mine. 

## PS
In producer_consumer_practice.py I made my idioms with a simple array to test if they
worked before I integrated them with the video code. It may be easier to test my idioms
There if you want to take a look. It takes numbers from an array, negates them, then prints 
them, all in separate threads using the same producer-consumer idioms as the video 
player. 



