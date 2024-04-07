#activate_this = "/home/pi/.virtualenvs/cv/bin/activate_this.py"
#exec(open(activate_this).read())
import cv2
import picamera
import serial
import numpy as np
import glob
import os
import time
from datetime import datetime
import RPi.GPIO as GPIO

# GPIO SETUP
flameSensor = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(flameSensor, GPIO.IN)

#Define HSV thresholds for smoke masking
lower_gray = np.array([0, 0, 0], np.uint8)
upper_gray = np.array([0, 100, 80 ], np.uint8)
lower_black = np.array([72, 19, 0], dtype="uint16")
upper_black = np.array([180, 255, 80], dtype="uint16")

#Define cascades classifier variables
smoke_cascade = cv2.CascadeClassifier('/home/pi/Desktop/cascadev2.xml')
flame_presence = False
def callback(channel):
    global flame_presence = var = True

def mask_and_find_contour(hsv, bgr):
	mask1 = cv2.inRange(hsv, lower_black, upper_black)
	mask2 = cv2.inRange(hsv, lower_gray, upper_gray)
	final_mask = mask1 + mask2

	_, thresh = cv2.threshold(final_mask, 40, 255, 0)
	cnts, hrchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	final = cv2.bitwise_and(bgr, bgr, mask=final_mask)
	return cnts, hrchy, final

def take_pic():
	print("PiCamera is taking a pic...")
	with picamera.PiCamera() as camera:
		camera.capture("/home/pi/Desktop/bgr_img.jpg")
		print("Pic taken!")
	piPic = cv2.imread("/home/pi/Desktop/bgr_img.jpg")
	return piPic

def classifyPic():
	smokeNumDetected = 0
	bgr_img = take_pic()
	#Convert BGR image to HSV
	hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
	contours, hierarchy, masked_img = mask_and_find_contour(hsv_img, bgr_img)
	try: hierarchy = hierarchy[0]
	except: hierarchy = []
	#computes the bounding box for the contour, and draws it on the frame,
	if len(contours) != 0:
		for contour, hier in zip(contours, hierarchy):
			(x,y,w,h) = cv2.boundingRect(contour)
			if w > 20 and h > 20:
					cv2.rectangle(hsv_img, (x,y), (x+w,y+h), (255, 0, 0), 2)
					toClassify = bgr_img[y:y + (h + 50) , x:x + (w + 50)]
					gray_img = cv2.cvtColor(toClassify, cv2.COLOR_BGR2GRAY)
					smokes = smoke_cascade.detectMultiScale(gray_img, 1.3, 5)
					print('Classifier matches: ' + str(len(smokes)))
					if len(smokes) == 0:
						fileDestination = "/home/pi/Desktop/detected_image.jpg"
						cv2.imwrite(fileDestination, bgr_img)
					else:
						smokeNumDetected = smokeNumDetected + len(smokes)
						for (x, y, w, h) in smokes:
							cv2.rectangle(toClassify, (x, y), (x + w, y + h), (0, 255, 0), 2)
							fileDestination = "/home/pi/Desktop/detected_image.jpg"
							cv2.imwrite(fileDestination, toClassify)
		print('Total classifier matches: ' + str(smokeNumDetected))
		now = datetime.now()
		#current_time = now.strftime("%H:%M:%S")
		#print("Current Time: ", current_time)
		with open("/home/pi/Desktop/QueryProgramRun.txt","a+") as f:
			f.write(str(now) + " Program took a picture with " + str(smokeNumDetected) + " classifier hit/s" + "\n")
	else:
		print('No contours found! Possible obstructions to camera found')
		#insert alert code here possible os


GPIO.add_event_detect(flameSensor, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(flameSensor, callback)  # assign function to GPIO PIN, Run function on change

while True:
	classifyPic()
	time.sleep(1)
	if flame_presence:
		print('Flame Detected!')













