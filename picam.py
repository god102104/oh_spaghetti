from picamera import PiCamera

picam_check = False

if not picam_check:
 IM_WIDTH = 320    #Use smaller resolution for
 IM_HEIGHT = 240   #slightly faster framerate

 camera = PiCamera()
 camera.resolution = (IM_WIDTH,IM_HEIGHT)
 camera.framerate = 30

