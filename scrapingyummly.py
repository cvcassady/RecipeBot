import datetime
import json
import urllib.request
import sqlite3
import os

os.chdir(r"C:\Users\Colin\Documents\Vision And Language\yummly")


current = 0
rate = 500

url = r"https://mapi.yummly.com/mapi/v13/content/search?q=recipe&start=" + str(current) + r"&maxResult=" + str(rate) + r"&fetchUserCollections=false&allowedContent[]=single_recipe&allowedContent[]=suggested_source&allowedContent[]=suggested_search&allowedContent[]=related_search&facetField[]=diet&facetField[]=holiday&facetField[]=technique&facetField[]=cuisine&facetField[]=course&facetField[]=source&facetField[]=brand&facetField[]=difficulty&facetField[]=dish&facetField[]=adtag&solr.view_type=search_internal"

yummly_raw_json = urllib.request.urlopen(url, timeout = 30).read().decode('utf8')
yummly = json.loads(accounts_json)

print("Received " + str(len(yummly["feed"])) + " recipes.")

recipes = yummly["feed"]
#[print(x["content"]["details"]["globalId"]) for x in accounts_small]

conn = sqlite3.connect("yummly.db")

for recipe in recipes:
    conn.execute("")


print("Done!")