import cv2
import numpy as np
import glob
import os

# define color thresholds in hsv
lower_gray = np.array([0, 5, 0], np.uint8)
upper_gray = np.array([120, 50, 80 ], np.uint8)
lower_black = np.array([72, 19, 0], dtype="uint16")
upper_black = np.array([180, 255, 80], dtype="uint16")

# define paths and file counts
path = 'C://users/asil/Desktop/raw'
contoured_dir = 'C://users/asil/Desktop/contoured'
positives_dir = 'C://users/asil/Desktop/newpos'
if not ((os.path.exists(positives_dir)) or (os.path.exists(contoured_dir))):
    os.mkdir(positives_dir)
fileNumber = 798

numPos = 0

# file = path + 'pos3.jpg'
# print('Filename: ' + file)
# test_pic(file)

def get_mask_find_contour(hsv, image):
    mask1 = cv2.inRange(hsv, lower_black, upper_black)
    mask2 = cv2.inRange(hsv, lower_gray, upper_gray)
    final_mask = mask1 + mask2

    _, thresh = cv2.threshold(final_mask, 40, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    masked_image = cv2.bitwise_and(image, image, mask=final_mask)
    return contours, masked_image

def draw_contours_and_crop(contour, masked, original):
    if len(contour) != 0:

        c = max(contour, key=cv2.contourArea)
        #print(int(c[0])* int(c[1]))
        x, y, w, h = cv2.boundingRect(c)
        info = str(x) + " " + str(y) + " " + str(w) + " " + str(h)
        # print(info)
        cv2.rectangle(masked, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.drawContours(masked, contour, -1, (0, 0, 255), 3)
        crop = original[y:y + h , x:x + w + 10]
        return crop, info

def resize(raw_image):
    height, width, _ = raw_image.shape
    if height > width:
        resized = cv2.resize(raw_image, (50, 55))
    elif height == width:
        resized = cv2.resize(raw_image, (50, 50))
    elif height < width:
        resized = cv2.resize(raw_image, (55, 50))
    # cv2.imshow('Resized Positive Image', resized)
    return resized

def create_positive_pic(raw):
    resized = cv2.resize(raw, (250, 200))
    #cv2.imshow('Resized', resized)
    hsv_img = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    contours_img, masked_img = get_mask_find_contour(hsv_img, resized)
    #cv2.imshow('Masked Image', masked_img)
    cropped_contour, pos_info = draw_contours_and_crop(contours_img, masked_img, resized)
    #cv2.imshow('Contours', masked_img)
    #cv2.imshow('Cropped Contour', cropped_contour)
    positive_image = resize(cropped_contour)
    #cv2.waitKey()
    return positive_image, masked_img

for filename in glob.glob(os.path.join(path, '*.jfif')):
    print('Filename: ' + filename)
    image = cv2.imread(filename)
    #cv2.imshow(filename, image)
    splitted = filename.split('\\')
    print (splitted[1])
    resized = resize(image)
    h, w, _ = resized.shape
    print('Height: ' + str(h) + ' Width: ' + str(w))
    line = '\npos/pos' + str(fileNumber) + '.jpg ' + '1 0 0 ' + str(w) + ' ' + str(h) + '\n'
    print(line)
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lenCon, _ = get_mask_find_contour(hsv_img, image)
    if len(lenCon) >=0:
        positive, masked = create_positive_pic(image)
        positives_file = positives_dir + '/pos' + str(fileNumber) + '.jpg'
        gray = cv2.cvtColor(positive, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(positives_file, gray)
        print('pos' + str(fileNumber) +'.jpeg')
        contoured_file = contoured_dir + '/posContour' + str(fileNumber) + '.jpeg'
        cv2.imwrite(contoured_file, masked)
        with open('info.dat','a') as f:
            f.write(line)

        fileNumber += 1
        numPos +=1
    #cv2.waitKey(0)

print('Number of positives made: ' + str(numPos))
