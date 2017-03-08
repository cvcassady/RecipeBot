'''
    We saved all of the JSON returned by yummly in our first scrape
    in case we missed any data we wanted to extract after scraping.
    This file utilizes that JSON field to extract more data.
'''

import datetime
import json
from json import JSONDecodeError
import urllib.request
from urllib.error import HTTPError
import sqlite3
import os
import sys

conn = sqlite3.connect("yummly.db")

while True:
    num_recipes_before = conn.execute("SELECT ID, JSON FROM Recipe;").fetchmany(5000)

    if (len(num_recipes_before) == 0):
        break
    
    for recipe in num_recipes_before:
        course_pos = recipe[1].find("course^course")
        
        if (course_pos == -1):
            continue

        course = recipe[1][course_pos+14:course_pos+35]
        course = course[0:course.find("'")]
        print(recipe[0], course)

        conn.execute("UPDATE Recipe SET Course=? WHERE id=?", (course, recipe[0]))

conn.commit()
conn.close()