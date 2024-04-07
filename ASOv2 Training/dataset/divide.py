import os 
import shutil
import random
import time
images = []
txt = []

cwd = os.getcwd()

for file in os.listdir(cwd):
    if file.endswith(".txt"):
        if file != 'missing.txt':
            if file != 'classes.txt':
                if file != 'unedited.txt':
                    txt.append(file)
    elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
        images.append(file)
        
train = len(images) * 0.8
train = round(train)
valid = len(images) - train
print("Total pictures", len(images))
print("Number of training pictures:", train)
print("Number of validation pictures:", valid)

def split_exception(split=[]):
    split.pop()
    for i in range(len(split)):
        if i > 0:
            split[0] = split [0] + "." + split[i]
    return split[0]

random.shuffle(images)
count = 1
for i in images:
    split_i = i.split(".")
    if len(split_i) > 2:
        split_i[0] = split_exception(split_i)
    for t in txt:
        split_t = t.split(".")
        if len(split_t) > 2:
            split_t[0] = split_exception(split_t)
        if split_i[0] == split_t[0]:
            print(split_i[0])
            if count <= train:
                shutil.move(t, cwd + "/labels/train")
                shutil.move(i, cwd + "/images/train")
            elif count > train:
                shutil.move(t, cwd + "/labels/valid")
                shutil.move(i, cwd + "/images/valid")
            count = count + 1
