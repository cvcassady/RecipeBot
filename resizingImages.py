# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:01:46 2016

@author: Colin
"""

import concurrent.futures
import os
import glob
import subprocess
from skimage import transform
from skimage import io
import skimage

files = os.listdir("images")

def resize(filename):
    io.imsave("resized_thumbs/" + filename, transform.resize(io.imread("images/" + filename), (224,224)))
    
    print(filename + " done.")

with concurrent.futures.ThreadPoolExecutor(4) as executor:
    executor.map(resize, files)
    