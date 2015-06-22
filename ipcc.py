from PIL import Image
import Tkinter
from Tkinter import PhotoImage
import pyFoscamLib
import time
from StringIO import StringIO
import numpy as np


class Ipcc():
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title('My Pictures')
        self.camera_width = 640
        self.camera_height = 480
        self.camera_response_times = [500, 500, 500, 500, 500]
        self.camera_delay = 500
        self.camera_img = None #PhotoImage(Image.new("RGB", (self.camera_width, self.camera_height), (128, 128, 128)))
        self.camera_updated = False
        self.camera = pyFoscamLib.CamLoader.create_camera("den")
        self.camera_frame = 0
        self.fps_time = None
        self.fps = None

        self.camera.get_status()
        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (self.camera_width, self.camera_height + 10, 0, 0))

        self.camera_panel = Tkinter.Canvas(self.root, width=self.camera_width, height=self.camera_height)
        self.camera_panel.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=Tkinter.YES)
        # self.camera_panel.create_image(self.camera_width, self.camera_height,
        #                                image=self.camera_img
        self.root.after(self.camera_delay, self.update_camera_image)
        self.root.mainloop()

    def update_camera_image(self):
        if self.fps_time is None:
            self.fps_time = time.time()
        start_time = time.time()
        raw_image = self.camera.get_snapshot()
        # TODO: eyeballer calls go here
        if raw_image:
            raw_image = StringIO(raw_image).read()
            # nparray = np.fromstring(raw_image, np.uint8)
            # nparray = np.resize(nparray, (self.camera_height, self.camera_width))
            # tmp_img = Image.fromarray(nparray, 'RGBA')
            # tmp_img = Image.frombytes(mode='RGB', size=(self.camera_width, self.camera_height), data=raw_image)
            #tmp_img.resize((self.camera_width, self.camera_height))
            #pil_img = PhotoImage(tmp_img)
            self.camera_img = raw_image
            self.camera_panel.create_image(self.camera_width, self.camera_height,
                                           image=None)  # pil_img)
            self.camera_updated = True
        else:
            self.camera_updated = False
        end_time = time.time()

        self.camera_frame += 1
        if time.time() - self.fps_time >= 1000:
            self.fps_time = None
            self.fps = self.camera_frame
            self.camera_frame = 0
        self.camera_response_times.pop()
        self.camera_response_times.insert(0, end_time - start_time)
        self.camera_delay = int(sum(self.camera_response_times) / len(self.camera_response_times))

        old_text = self.camera_panel.find_withtag('ipcc-text')
        if len(old_text):
            for t in old_text:
                self.camera_panel.delete(t)

        self.camera_panel.create_text(3, 5, text='cam del: %dms' % self.camera_delay, tags='ipcc-text', anchor='nw',
                                      fill='red')
        self.camera_panel.create_text(3, 20, text='frame: %d' % self.camera_frame, tags='ipcc-text', anchor='nw',
                                      fill='red')
        self.camera_panel.create_text(3, 35, text='raw sz: %d' % len(raw_image), tags='ipcc-text', anchor='nw',
                                      fill='red')
        if self.fps:
            self.camera_panel.create_text(3, 50, text='fps: %d' % self.fps, tags='ipcc-text', anchor='nw',
                                          fill='red')
        else:
            self.camera_panel.create_text(3, 50, text='fps_build: %d' % (time.time() - self.fps_time), tags='ipcc-text', anchor='nw',
                                          fill='red')
        self.camera_panel.update_idletasks()

        self.root.after(self.camera_delay, self.update_camera_image)


def main():
    Ipcc()


if __name__ == '__main__':
    main()
