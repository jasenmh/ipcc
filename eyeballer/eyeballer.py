import numpy as np
import cv2

class eyeballer:
    # ---------- Private methods ----------
	def __init__(self):
		self.detect_targets = False
		self.last_image = None
		self.average_image = None

	def _target_bounding_boxes(self):
		pass

    # ---------- Public methods ----------
	def add_image(self, image):
		""" 
		This method takes a new image, adds it to the average image, and
		applies all CV algorithms it is set to use. It then returns the 
		average image.
		:param image: next image to add to scene average
		:return: average image
		"""

		if self.average_image == None:
			irows, icols, idep = image.shape
			self.average_image = np.float32(image) #np.zeros((irows, icols, idep), np.uint8)
			return None

		smooth_image = cv2.GaussianBlur(image, (5, 5), 0)
		cv2.accumulateWeighted(smooth_image, self.average_image, 0.25, None)
		show_image = self.average_image

		return show_image

