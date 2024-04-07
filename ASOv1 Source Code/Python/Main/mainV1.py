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

#Define HSV thresholds for smoke masking
lower_gray = np.array([0, 0, 0], np.uint8)
upper_gray = np.array([0, 100, 80 ], np.uint8)
lower_black = np.array([72, 19, 0], dtype="uint16")
upper_black = np.array([180, 255, 80], dtype="uint16")

#Define cascades classifier variables
smoke_cascade = cv2.CascadeClassifier('/home/pi/Desktop/cascadev2.xml')

#Define serial communication variables
arduino = serial.Serial('/dev/ttyACM0',9600 )
#arduino.flushInput()

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

def listenToArduino():
	read_serial=arduino.readline()
	serial_message = str(read_serial.strip())
	print("Serial message is: " + serial_message)
	l = list(serial_message)
	print(l)
	if len(l) < 4:
		message = l[2]
	else:
		message = l[3]
	if message == str(0):
		message = 0
	elif message == str(1):
		message = 1
	else:
		message = 0
	readState(message)
	return message
def sendToArduino(signal_encode):
	arduino.write(signal_encode)
def readState(state):
	if state is 0:
		print('Arduino says 0 so RasPi will sleep...')
	elif state is 1:
		print('Arduino says 1 so Raspi will take a pic...')
	elif state is 2:
		print('RasPi tells Arduino no smoke detected...')
	elif state is 3:
		print('RasPi tells Arduino smoke is detected!')
	else:
		print('Arduino is still busy....')
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
		if smokeNumDetected == 0:
			arduino.write(b'2')
			readState(2)
		elif smokeNumDetected > 0:
			arduino.write(b'3')
			readState(3)
		now = datetime.now()
		#current_time = now.strftime("%H:%M:%S")
		#print("Current Time: ", current_time)
		with open("/home/pi/Desktop/QueryProgramRun.txt","a+") as f:
			f.write(str(now) + " Program took a picture with " + str(smokeNumDetected) + " classifier hit/s" + "\n")
	else:
		print('No contours found/Black picture taken')
	arduino.write(b'2')
print('Booting up ASO')
time.sleep(10)
print('ASO booted. Starting serial communication with Arduino')
arduino.write(b'1')


while True:
	sendToArduino(b'1')
	classifyPic()
	readState(4)
	time.sleep(5)






