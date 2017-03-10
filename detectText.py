#import modules
import pytesseract
from PIL import Image
#http://grimhacker.com/2014/11/23/installing-pytesseract-practically-painless/
import os, sys

#initialize empty list to store names of ppjgs
badPics = []
goodPics = []


path = "/Users/Kerry/Documents/UVA-DSI/Spring/Vision_and_Language /images_project/subset/"
dirs = os.listdir(path)

for items in dirs:
    x = pytesseract.image_to_string(Image.open(/Users/Kerry/Documents/UVA-DSI/Spring/Vision_and_Language /images_project/subset/+items))
    if bool(x) == True:
        badPics.append(items)
    else:
        if bool(x) == False:
            goodPics.append(items)

#check list
len(badPics)
len(goodPics)

#Percentage of Pics with text
len(badPics)/ (len(badPics)+len(goodPics))

#View Pics
for i in badPics:
    im = Image.open(path+i)
    im.show()
