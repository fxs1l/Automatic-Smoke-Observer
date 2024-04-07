import cv2
import os
import glob

fileNumber = 0
path = 'C://users/Asil/Desktop/Haar Trainer Master Kit/pos'
for filename in glob.glob(os.path.join(path, '*.jpg')):
    print('Filename: ' + filename)
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    FILE = path + '/pos' + str(fileNumber) + '.jpg'
    cv2.imwrite(FILE, gray)
    fileNumber += 1
