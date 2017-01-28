'''
Reads all image URL and ID's from yummly.db, then downloads all images
contained within.
'''

import sqlite3
from urllib.request import urlopen
import urllib.request
from threading import Thread
import os
import re
import concurrent.futures

#os.chdir(r"C:\Users\Colin\Documents\Vision And Language\RecipeBot")

def download(tup):
    url = tup[0]
    iden = tup[1]
    
    urllib.request.urlretrieve(url, "images/" + iden + ".jpg")


conn = sqlite3.connect("yummly.db", timeout = 600)
urls = conn.execute("SELECT ImageUrl, ID from Recipe;").fetchall()
conn.close()
  
with concurrent.futures.ThreadPoolExecutor(32) as executor:
    executor.map(download, urls)


