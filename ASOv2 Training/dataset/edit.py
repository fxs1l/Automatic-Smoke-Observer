import os 
import shutil
import sys
'''
    TO DO LIST: 
    1. Add folder options
    2. Add unedited options
    3. Fix rename function
'''
cwd = os.getcwd()
folder = ""

def check_missing(folder=""):
    images = []
    txt = []
    safe = []
    with_images = []
    global cwd
    check_in = os.path.join(cwd, folder)
    # get text and image files
    for file in os.listdir(check_in):
        if file.endswith(".txt"):
            if file != 'missing.txt':
                if file != 'classes.txt':
                    if file != 'unedited.txt':
                        txt.append(file)
        elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            images.append(file)
    # warn about no files found
    if len(txt) == 0:
        print("W: No text files found in this directory")
    if len(images) == 0:
        print("W: No images found in this directory")
    print(len(images), "images found")
    if len(txt) >= 0 and len(images) >= 0:
        # find images with txt files
        for t in txt:
            filename = t.split(".")
            if len(filename) > 2:
                filename[0] = split_exception(filename)
            for i in images:
                img_name = i.split(".")
                if len(img_name) > 2: 
                    img_name[0] = split_exception(img_name)
                if filename[0] == img_name[0]:
                    safe.append(i)
        # find txt files without images
        for i in images:
            img_name = i.split(".")
            if len(img_name) > 2: 
                img_name[0] = split_exception(img_name)
            for t in txt:
                filename = t.split(".")
                if len(filename) > 2:
                    filename[0] = split_exception(filename)
                if filename[0] == img_name[0]:
                    with_images.append(t)
        count1 = 0
        count2 = 0
        missing = []
        without_images = []
        for i in images:
            if i not in safe:
                #print(i, "has missing annotation files")
                count1 = count1 + 1
                missing.append(i)
        for t in txt:
            if t not in with_images:
                #print(i, "has missing annotation files")
                count2 = count2 + 1
                without_images.append(t)
        # create txt document of missing files
        total = count1 + count2
        if total > 0 :
            create_txt = os.path.join(check_in,"missing.txt")
            f = open(create_txt, "w")
            for miss in missing:
                f.write(miss + "\n")
            for out in without_images:
                f.write(out + "\n")
            f.close()
        
        # count number of missing files
        if total > 0:
            print(count1 + count2 ,"files with missing pairs. Listed in 'missing.txt'")
        else: 
            print("I: No missing files.")
        return safe, images, txt
    return safe, images, txt

def remove_missing():
    safe, images, txt = check_missing()          
    # remove missing images 
    count = 0
    for i in images:
        if i not in safe:
            os.remove(i)
            print("Removing", i , "...")
            count = count + 1
    # count number of pictures deleted
    if count > 0:
        print(count ,"pictures deleted")
    else: 
        print("I: No missing pictures found.")
        
def edit_class_index(og,final):
    safe, images, txt = check_missing()
    unedited_txt = []
    unedited = False
    for t in txt:
        try:
            print("Editing", t, "index from", og, "to", final, "...")
            file = open(t, 'r+')
            Lines = file.readlines()
            file.truncate(0)
            for line in Lines:
                line_split = line.split(" ")
                edited_line = ""
                for index, element in enumerate(line_split):
                    if og == element:
                        line_split[index] = final
                    if element == "16" or element == "15":
                        print("-----Line is unedited-----")
                        unedited = True
                for element in line_split:
                    edited_line = edited_line + " " + element
                    cleaned_line = edited_line.lstrip()
                print(cleaned_line)
                file.write(cleaned_line)
            if unedited:
                unedited_txt.append(t)
                unedited = False
            file.close()
        except FileNotFoundError:
            print("No such file or directory:", t)
    f = open("unedited.txt","w")
    if len(unedited_txt) > 0:
        print("Listing" , len(unedited_txt), " text files to 'unedited.txt'...")
        for text in unedited_txt:
            f.write(text + "\n")
    clean_x00()
            
def rename_files(new_name, index):
    safe, images, txt = check_missing()
    print("Starting renaming process...")
    for img in images:
        split_img = img.split(".")
        extension = "." + split_img[len(split_img)-1]
        if len(split_img[0]) > 2:
            split_img[0] = split_exception(split_img)
        for t in txt:
            split_txt = t.split(".")
            if len(split_txt) > 2:
                split_txt[0] = split_exception(split_txt)
            if split_txt[0] == split_img[0]:
                #print("Renaming..." , split[0])
                txt_filename = new_name + "_" + str(index) + ".txt"
                img_filename = new_name + "_" + str(index) + extension
                # skip index number if file exists
                if os.path.isfile(txt_filename) or os.path.isfile(img_filename):
                    index = index + 1 
                print("Renaming",img,"to",img_filename)
                os.rename(img, img_filename)
                print("Renaming",t,"to",txt_filename)
                os.rename(t, txt_filename)
                index = index + 1

# moves files to specified folder
def move(option):
    global cwd
    option = str(option)
    if not os.path.isdir(option):
        os.mkdir(option)
    destination = option
    text = option + ".txt"
    f = open(text, "r")
    Lines = f.readlines()
    to_move = []
    if len(Lines) == 0:
        print("W: No files found")
    else:
        for line in Lines:
            split = line.split(".")
            if len(split) > 2:
                split[0] = split_exception(split)
            to_move.append(split[0])
            # move all images assosciated with unedited files
            for img in os.listdir(os.getcwd()):
                if img.endswith(".jpg") or img.endswith(".png") or img.endswith(".jpeg"):
                    split = img.split(".")
                    if len(split) > 2:
                        split[0] = split_exception(split)
                    for m in to_move:
                        if split[0] == m:
                            shutil.move(img, os.path.join(cwd,destination))
                            print("Moving", img, "to", cwd, "/", destination)
        # move all unedited files
        for txt in os.listdir(os.getcwd()):
            if txt.endswith(".txt"):
                split = txt.split(".")
                if len(split) > 2:
                    split[0] = split_exception(split)
                for m in to_move:
                    if split[0] == m:
                        shutil.move(txt, os.path.join(cwd,destination))
                        print("Moving", txt, "to", cwd ,"/", destination)
        check_missing(destination)

# cleans /x00/ characters found when editing txt files
def clean_x00():
    for files in os.listdir(cwd):
        if files.endswith(".txt"):
            f = open(files, "r")
            Lines = f.readlines()
            for i, line in  enumerate(Lines):
                Lines[i] = line.replace('\x00','')
            f = open(files, "w")
            f.writelines(Lines)
            f.close()
    print("Cleaned annoying /x00/")

# handles a case when the filename has multiple "."
def split_exception(split=[]):
    split.pop()
    for i in range(len(split)):
        if i > 0:
            split[0] = split [0] + "." + split[i]
    return split[0]

# print error 
def throw_error():
    print("E: Missing arguments!\nArguments:\ncheck\t\t-checks for missing pairsn\nremove\t\t-removes images with no annotation files\n\t\t-output is saved to 'missing.txt'\nmove\t\t-moves files with certain characteristics (missing,unedited)\nclean\t\t-clears '/x00/' characters in annotation files\nclass\t\t-edits class indeces in annotation files\nrename\t\t-renames all images")

# get arguments
try:
    if sys.argv[1] == "remove":
        remove_missing()
    elif sys.argv[1] == "check":
        s, i, t = check_missing()
    elif sys.argv[1] == "clean":
        clean_x00()
    elif sys.argv[1] == "move":
        try:
            if sys.argv[2] == "missing":
                move(sys.argv[2])
            elif sys.argv[2] == "unedited":
                move(sys.argv[2])
        except IndexError:
            print("E: Usage: python3 edit.py move <file-description>")
    elif sys.argv[1] == "class":
        try:
            edit_class_index(str(sys.argv[2]), str(sys.argv[3]))
        except IndexError:
            print("E: Usage: python3 edit.py class <index-to-edit> <correct-index>")
    elif sys.argv[1] == "rename":
        try:
            print(sys.argv[2], sys.argv[3])
            rename_files(sys.argv[2], int(sys.argv[3]))
        except IndexError:
            print("E: Usage: python3 edit.py rename <new_name> <starting-index>")
    else:
        print("E: Incorrect argument!")
except IndexError:
    throw_error()
