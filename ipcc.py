# http://stackoverflow.com/questions/17073227/display-an-opencv-video-in-tkinter-using-multiprocessing

#import numpy as np
from multiprocessing import Process, Queue
#from Queue import Empty
import cv2
#import cv2.cv as cv
#import ImageTk
from PIL import Image
#import time
import Tkinter as Tk
from Tkinter import PhotoImage


# tkinter GUI functions----------------------------------------------------------
def quit_(rooot, process):
    process.terminate()
    rooot.destroy()


def update_image(imaage_label, queuee):
    frame = queuee.get()
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    a = Image.fromarray(im)
    b = PhotoImage(image=a)
    imaage_label.configure(image=b)
    imaage_label._image_cache = b  # avoid garbage collection
    root.update()


def update_all(rooot, imaage_label, queuee):
    update_image(imaage_label, queuee)
    root.after(0, func=lambda: update_all(rooot, imaage_label, queuee))


#multiprocessing image processing functions-------------------------------------
def image_capture(queuee):
    vid_file = cv2.VideoCapture(0)
    while True:
        try:
            flag, frame = vid_file.read()
            if flag == 0:
                break
            queuee.put(frame)
            cv2.waitKey(20)
        except:
            continue


if __name__ == '__main__':
    queue = Queue()
    print 'queue initialized...'
    root = Tk.Tk()
    print 'GUI initialized...'
    image_label = Tk.Label(master=root)  # label for the video frame
    image_label.pack()
    print 'GUI image label initialized...'
    p = Process(target=image_capture, args=(queue,))
    p.start()
    print 'image capture process has started...'
    # quit button
    quit_button = Tk.Button(master=root, text='Quit', command=lambda: quit_(root, p))
    quit_button.pack()
    print 'quit button initialized...'
    # setup the update callback
    root.after(0, func=lambda: update_all(root, image_label, queue))
    print 'root.after was called...'
    root.mainloop()
    print 'mainloop exit'
    p.join()
    print 'image capture process exit'