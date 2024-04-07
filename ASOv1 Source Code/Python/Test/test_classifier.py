import cv2
import numpy as np

smoke_cascade = cv2.CascadeClassifier('C://users/asil/Desktop/cascade.xml')
smokeNumDetected = 0

image = cv2.imread('C://users/asil/Desktop/slum.jpg')
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

smokes = smoke_cascade.detectMultiScale(gray_img, 1.3, 5)
print('Classifier matches: ' + str(len(smokes)))
smokeNumDetected = smokeNumDetected + len(smokes)

for (x, y, w, h) in smokes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #fileDestination = '/home/pi/Desktop/FoundContours/' + str(contourNum) + 'contour.jpg'
        fileDestination = 'C://users/asil/Desktop/Hello/' + 'detected_smoke.jpg'
        cv2.imwrite(fileDestination, image)