#!/usr/bin/python

import Image
import Tkinter
from Tkinter import PhotoImage
import pyFoscamLib
import time


class Ipcc():
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title('My Pictures')
        self.camera_width = 640
        self.camera_height = 480
        self.camera_response_times = [500, 500, 500, 500, 500]
        self.camera_delay = 500
        self.camera_img = PhotoImage(Image.new("RGB", (self.camera_width, self.camera_height), (128, 128, 128)))
        self.camera_updated = False
        self.camera = pyFoscamLib.CamLoader.create_camera("den")
        self.camera_frame = 0

        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (self.camera_width, self.camera_height + 10, 0, 0))

        self.camera_panel = Tkinter.Label(self.root, image=self.camera_img)
        self.camera_panel.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=Tkinter.YES)
        self.root.after(self.camera_delay, self.update_camera_image)
        self.root.mainloop()

    def update_camera_image(self):
        start_time = time.time()
        raw_image = self.camera.get_snapshot()
        pil_img = PhotoImage(Image.fromstring('RGB', (self.camera_width, self.camera_height), raw_image))
        # TODO: eyeballer calls go here
        if pil_img:
            self.camera_img = pil_img
            self.camera_panel.configure(image=self.camera_img)
            self.camera_updated = True
        else:
            self.camera_updated = False
        self.camera_panel.update_idletasks()
        end_time = time.time()

        self.camera_frame = (self.camera_frame + 1) % 9999
        self.camera_response_times.pop()
        self.camera_response_times.insert(0, end_time - start_time)
        self.camera_delay = sum(self.camera_response_times)/len(self.camera_response_times)

        self.root.after(self.camera_delay, self.update_camera_image)


def main():
    app = Ipcc()

if __name__ == '__main__':
    main()