from pyFoscamLib import FI8918W
import sys
import numpy as np
import cv2
import time

ipAddr = ""
userName = ""
passWord = ""
iWidth = 640
iHeight = 480

def main():
	"""
	Motion tracking code borrowed from:
	http://derek.simkowiak.net/motion-tracking-with-python/
	http://opencvpython.blogspot.com/2012/07/background-extraction-using-running.html
	"""
	cam = FI8918W.fi8918w(ipAddr, userName, passWord)
	cam.getStatus()
	font = cv2.FONT_HERSHEY_SIMPLEX
	t0 = time.clock()
	uInput = 0
	tmpImg = cam.getSnapshotToImage()
	irows, icols, idep = tmpImg.shape
	convertImg = np.zeros((irows, icols, idep), np.uint8)
	imgAvgs = np.float32(tmpImg)
	
	while uInput != 42:

		img = cam.getSnapshotToImage()
		if type(img) == int:	# error returns -1, else return numpy array 
			continue

		smoothImg = cv2.GaussianBlur(img, (5, 5), 0)
		cv2.accumulateWeighted(smoothImg, imgAvgs, 0.50, None)
		cv2.convertScaleAbs(imgAvgs, convertImg, 1.0, 0.0)
		showImg = cv2.absdiff(smoothImg, convertImg)

		tNow = time.clock()
		tStr = str(tNow - t0)
		cv2.putText(img, 'frm time: ' + tStr, (5, 30), font, 1, (255, 255, 255), 1)
		cv2.putText(img, 'ir: ' + cam.irStatus, (5, 60), font, 1, (255, 255, 255), 1)
		cv2.imshow(cam.cameraName, img)
		cv2.imshow('Avg Image', showImg)

		uInput = cv2.waitKey(1)

		if uInput == ord('q'):
			break
		if uInput == ord('i'):
			cam.setIr(True)
			print "IR on"
			cam.getStatus()
		if uInput == ord('o'):
			cam.setIr(False)
			print "IR off"
			cam.getStatus()

		t0 = time.clock()

	cv2.destroyAllWindows()


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "expecting: %s <ip address:port> <user name> <password>" % (sys.argv[0])
		sys.exit()

	ipAddr = sys.argv[1]
	userName = sys.argv[2]
	passWord = sys.argv[3]

	main()