import picamera

print("PiCamera is taking a pic...")
with picamera.PiCamera() as camera:
    camera.capture("/home/pi/Desktop/test.jpg")
print("Pic taken!")
piPic = cv2.imread("/home/pi/Desktop/test.jpg")
