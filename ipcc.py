from pyFoscamLib import FI8918W
import sys
import os.path
import numpy as np
import cv2
import time

ipAddr = ""
userName = ""
passWord = ""
iWidth = 640
iHeight = 480
class ipcc:
  def __init__(self, ipAddr, userName, passWord):
    self.ipAddr = ipAddr
    self.userName = userName
    self.passWord = passWord

  def run(self):
    """
    Motion tracking code adapted from:
    http://derek.simkowiak.net/motion-tracking-with-python/
    http://opencvpython.blogspot.com/2012/07/background-extraction-using-running.html
    """
    cam = FI8918W.fi8918w(self.ipAddr, self.userName, self.passWord)
    cam.get_status()
    font = cv2.FONT_HERSHEY_SIMPLEX
    t0 = time.clock()
    uInput = 0
    tmpImg = captureImage()
    irows, icols, idep = tmpImg.shape
    convertImg = np.zeros((irows, icols, idep), np.uint8)
    imgAvgs = np.float32(tmpImg)
        
    while True:
      img = captureImage()
      if type(img) == int:    # error returns -1, else return numpy array 
        continue

      smoothImg = cv2.GaussianBlur(img, (5, 5), 0)
      cv2.accumulateWeighted(smoothImg, imgAvgs, 0.50, None)
      cv2.convertScaleAbs(imgAvgs, convertImg, 1.0, 0.0)
      showImg = cv2.absdiff(smoothImg, convertImg)

      tNow = time.clock()
      tStr = str(tNow - t0)
      cv2.putText(img, 'frm time: ' + tStr, (5, 30), font, 1, (255, 255, 255), 1)
      #cv2.putText(img, 'ir: ' + cam.irStatus, (5, 60), font, 1, (255, 255, 255), 1)
      cv2.imshow(cam.cameraName, img)
      cv2.imshow('Avg Image', showImg)

      uInput = cv2.waitKey(1)

      if uInput == ord('q'):
        break
      if uInput == ord('i'):
        cam.ir_on()
        print "IR on"
        cam.get_status()
      if uInput == ord('o'):
        cam.ir_off()
        print "IR off"
        cam.get_status()

      t0 = time.clock()

    cv2.destroyAllWindows()

  def captureImage():
    tmpImgStr = cam.get_snapshot()
    nparr = np.fromstring(tmpImgStr, np.uint8)
    tmpImg = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    return tmpImg


if __name__ == '__main__':
  argc = len(sys.argv)
  if argc == 2:
    configFile = "cameras/%s" % sys.argv[1]
    if not os.path.isfile(configFile):
      print "unable to find configuration for camera '%s'" % sys.argv[1]
      sys.exit()

    cf = open(configFile, "r")
    c = cf.read().split('\n')
    cf.close()

    ipAddr = c[0]
    userName = c[1]
    passWord = c[2]
  elif argc == 4:
    ipAddr = sys.argv[1]
    userName = sys.argv[2]
    passWord = sys.argv[3]
  else:
    print "expecting: %s <ip address:port> <user name> <password>" % (sys.argv[0])
    sys.exit()


  client = ipcc(ipAddr, userName, passWord)
  client.run()
