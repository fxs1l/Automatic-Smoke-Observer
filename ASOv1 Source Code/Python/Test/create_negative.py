import cv2
import os
import glob

source_path = 'C://users/asil/Desktop'
negatives_dir ='C://users/asil/Desktop/extraniggas'

if not os.path.exists(negatives_dir) :
    os.mkdir(negatives_dir)
fileNumber = 2009

for filename in glob.glob(os.path.join(source_path, '*.jpg')):
    print('Filename: ' + filename)
    image = cv2.imread(filename)
    height, width, _ = image.shape
    if width > height:
        final = cv2.resize(image, (550,500))
    elif width < height:
        final = cv2.resize(image, (500,550))
    elif width == height:
        final = cv2.resize(image, (500,500))
    file = negatives_dir + '/neg' + str(fileNumber) + '.jpg'
    gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(file, gray)
    splitted = filename.split('\\')
    line = 'neg/neg' + str(fileNumber) + '.jpg ' + '\n'
    print(line)
    with open('bg.txt','a') as f:
        f.write(line)
    fileNumber += 1
