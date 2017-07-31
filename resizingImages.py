"""
Resizes all images in the folder 'images' to 224x224 (input size of VGG)
and stores them in the folder 'resized_thumbs'. creating the folder if
it doesn't exist.
"""

import concurrent.futures
import os
import subprocess
from skimage import transform
from skimage import io
import skimage

files = os.listdir("images")

if not os.path.exists('resized_thumbs'):
    os.makedirs('resized_thumbs')

def resize(filename):
    io.imsave("resized_thumbs/" + filename, transform.resize(io.imread("images/" + filename), (224,224)))
    
    print(filename + " done.")

with concurrent.futures.ThreadPoolExecutor(4) as executor:
    executor.map(resize, files)
    
