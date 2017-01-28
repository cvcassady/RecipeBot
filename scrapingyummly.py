import datetime
import json
from json import JSONDecodeError
import urllib.request
from urllib.error import HTTPError
import sqlite3
import os
import sys

#os.chdir(r"C:\Users\Colin\Documents\Vision And Language\RecipeBot")


current = 0
rate = 500
query = "recipe"

while True:
    yummly_url = r"https://mapi.yummly.com/mapi/v13/content/search?q=" + query + r"&start=" + str(current) + r"&maxResult=" + str(rate) + r"&fetchUserCollections=false&allowedContent[]=single_recipe&allowedContent[]=suggested_source&allowedContent[]=suggested_search&allowedContent[]=related_search&facetField[]=diet&facetField[]=holiday&facetField[]=technique&facetField[]=cuisine&facetField[]=course&facetField[]=source&facetField[]=brand&facetField[]=difficulty&facetField[]=dish&facetField[]=adtag&solr.view_type=search_internal"

    try:
        yummly_raw_json = urllib.request.urlopen(yummly_url, timeout = 30).read().decode('utf8')
    except HTTPError as err:
        print(str(err))
        if "408: Request Timeout" in str(err):
            print("Retrying...")
            continue
        print(yummly_url)
        sys.exit()

    try:
        yummly = json.loads(yummly_raw_json)
    except JSONDecodeError as err:
        print(str(err))
        print(yummly_url)
        print(page[:300])
        sys.exit()

    num_recipes_received = len(yummly["feed"])
    print("Received " + str(num_recipes_received) + " recipes.")

    recipes = yummly["feed"]
    #[print(x["content"]["details"]["globalId"]) for x in accounts_small]

    conn = sqlite3.connect("yummly.db")
    num_recipes_before = conn.execute("SELECT count(*) FROM Recipe;").fetchone()[0]

    for recipe in recipes:
        try:
            r_url = recipe["seo"]["web"]["link-tags"][0]["href"]
            r_id = recipe["content"]["details"]["globalId"]
            title = recipe["display"]["displayName"]
            ingredients = "; ".join([ingredient["ingredient"] for ingredient in recipe["content"]["ingredientLines"]])
            image_url = recipe["display"]["images"][0]
            r_description = recipe["seo"]["web"]["meta-tags"]["description"]

            r_json = str(recipe)

            insert_list = [r_id, r_json, title, ingredients, image_url, r_description, r_url]

            conn.execute("INSERT OR IGNORE INTO Recipe VALUES (?,?,?,?,?,?,?)", insert_list)
        except:
            e = str(sys.exc_info()[0])
            print("Error: " + e)
            print(r_url)
            continue

    conn.commit()

    num_recipes_after = conn.execute("SELECT count(*) FROM Recipe;").fetchone()[0]
    print(str(num_recipes_after - num_recipes_before) + " of " + str(num_recipes_received) + " were inserted.")

    conn.close()

    current = current + rate



