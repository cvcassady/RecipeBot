import sqlite3
import concurrent.futures
import os

images = os.listdir('images/')

image_dict = {image: 1 for image in images}

conn = sqlite3.connect("yummly.db")
recipe_ids = conn.execute("SELECT ID FROM Recipe;").fetchall()
conn.close()

thread_batch = [tuple([tuple(recipe_ids[x*1000:(x+1)*1000]), image_dict]) for x in range(0, (len(recipe_ids)//1000)+1)]

def findMissing(tup):
    conn = sqlite3.connect("yummly.db")

    for idx in tup[0]:
        #if (idx[0] + ".jpg" in tup[1]):
        if (tup[1].get(idx[0] + ".jpg", 0)):
            #print(idx[0] + " in images!")
            conn.execute("UPDATE Recipe SET ImageAvailable=? WHERE ID=?", (1, idx[0]))
    conn.commit()
    conn.close()

with concurrent.futures.ThreadPoolExecutor(4) as executor:
    executor.map(findMissing, thread_batch)