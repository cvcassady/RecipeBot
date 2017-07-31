'''
Retrieves all ingredients from yummly.db, removes extraneous
descriptors, and then uses a frequency list to selectively score
sections of each ingredient in an attempt to reduce the ingredient
to its most basic form. Utilizes synonymDict.py for ingredients
that could not be automatically reduced. The clean ingredients
list per recipe is then stored in yummly.db in the CleanIngredients
column as a semicolon delimited string.
'''

import datetime
import json
from json import JSONDecodeError
import sqlite3
import sys
import numpy as np
import re
import concurrent.futures
import timeit
import synonymdict as sd

print("Reading ingredients...")
conn = sqlite3.connect("yummly.db")
ingredients = conn.execute("SELECT ID, Ingredients FROM Recipe WHERE English=1;").fetchall()
conn.close()

remove_list = ['fresh', 'frozen', 'ground', 'powdered', 'low', 'extra', 'virgin',
    'all purpose', 'sodium', 'fat', 'less', 'freshly', 'dried', 'salted', 'whole', 'crispy',
    'grated', 'melted', 'filtered', 'unfiltered', 'sweetened', 'unsweetened', 'shredded',
    'small', 'petite', 'large', 'crumbles', 'chunks', 'toasted', 'cracked', 'chopped',
    'cooked', 'nonfat', 'plain', 'double', 'raw', 'minced', 'spray', 'pure', 'granulated',
    'dry', 'roasted', 'smoked', 'vidalia', 'hot', 'florets', 'slices', 'kosher', 'light',
    'sliced', 'reduced', '1%', '2%', '3%', '4%', 'crumbled', 'prepared', 
    'sprigs', 'diced', 'morsels', 'filet', 'unsalted',  'slivered', 'firm', 'fillets',
    'halves', 'unflavored', 'mashed', 'new', 'blanched', 'heirloom', 'refrigerated', 'silken'
    'rind', 'shelled', 'coarse', 'cutlets', 'sticks' ]

remove_pattern = re.compile("\\b(" + "|".join(remove_list) + ")\\W", re.I)

def prepIngredients(ingredients_string, remove_pattern):
    ingredients_string = ingredients_string.lower()
    ingredients_string = ingredients_string.replace(";"," ;")
    ingredients_string = ingredients_string.replace("-"," ")
    ingredients_string = ingredients_string.replace(","," ")
    ingredients_string = ingredients_string.replace("?","")

    ingredients_string = remove_pattern.sub("", ingredients_string)

    return [x.strip() for x in ingredients_string.split(";")]

print("Prepping ingredients...")
ingredients = [tuple([x[0], prepIngredients(x[1], remove_pattern)])for x in ingredients]

print("Calculating unique values...")
ingredients = np.array([item for sublist in ingredients for item in sublist[1]])


unique_ing = np.unique(ingredients, return_counts = True)
argsort_results = np.argsort(-unique_ing[1])

sorted_ing = unique_ing[0][argsort_results]
sorted_vals = unique_ing[1][argsort_results]

# Calculating the ingredient dictionary
# ing_dict scores each ingredient with how frequent they are.
# Salt gets a 1, since it's the most frequent
# Liver might get 0.5 since it's half-way down
# Szechuan chilies would get a low score due to its infrequency
ing_dict = {}
len_sorted_ing = len(sorted_ing)
for i in range(0,len(sorted_ing)):
    if (sorted_ing[i].replace('es','').replace('s','') not in ing_dict):
        ing_dict[sorted_ing[i].replace('es','').replace('s','')] = (len_sorted_ing - i) / len_sorted_ing

ing_dict[""] = 0

Print the list to file
f = open("ingredients_by_frequency_cleaned.txt", "w")
[f.write(str(sorted_vals[i]) + "\t\t" + sorted_ing[i].encode(sys.stdout.encoding, \
      errors='replace').decode(sys.stdout.encoding, errors='replace') + "\n") for i in range(0, len(sorted_vals))]
f.close()

# findRoot attempts to find the basic ingredient within a string
# e.g. 1tbps dehydrated onion => onion
# ing = the ingredient in question
# ing_dict = dictionary precalculated with ingredient scores
def findRoot(ing, ing_dict):
    full_name = ing
    ing = ing.lower().split(" ")

    can_index_max = 0
    can_conf_max = 0

    # This terrible looking line of code generates bigrams backwards, then taks on the split
    # ingredients string, backwards. The idea being that the identifying information is usually
    # at the end of the string (from basic visual analysis)
    ing = [ing[x] + " " + ing[x+1] for x in reversed(range(0,(len(ing) - 1)))] + ing[::-1] + [full_name]
    # we then pair each candidate with a zero, to denote our confidence that it is that ingredient
    candidates = [[x, 0] for x in ing]

    for can_index, candidate in enumerate(candidates):
        # give a slight bump to things near the front of the list
        candidate[1] = 0.20 / (can_index+1)
        
        #search for the bigram in the ingredients list
        candidate = searchList(candidate, ing_dict)

        if (candidate[1] > can_conf_max):
            can_index_max = can_index
            can_conf_max = candidate[1]

    return candidates[can_index_max][0]


#candidate[0] = ingredient name
#candidate[1] = confidence that that's the name we actually want
def searchList(candidate, ing_dict):
    current_candidate_depluralized = candidate[0].replace('es','').replace('s','')

    candidate[1] = candidate[1] + ing_dict.get(current_candidate_depluralized, 0)

    return candidate

# cleanIngredients uses findRoot on every ingredient from every recipe
# storing the cleaned ingredients in the recipe's CleanIngredients in yummly.db
# tup is a tuple of 4 values
# [0] = [ID, ingredients]
# [1] = ing_dict, a dictionary precalculated with ingredient scores
# [2] = the manually created synonym dictionary
# [3] = the manually created removal dictionary
def cleanIngredients(tup):
    conn = sqlite3.connect("yummly.db", timeout = 600)
    print("Starting batch of 1000...")


    for iden, ingredients in tup[0]:

        # first, we want to reduce the ingredients using "findRoot"
        ingredients = [findRoot(x, tup[1]) for x in ingredients]

        #then we want to do manual reductions, facilitated by synonymdict
        ingredients = [tup[2].get(x, x) for x in ingredients if x not in tup[3]]

        ingredients = "; ".join(ingredients)

        #print(iden, ingredients.encode(sys.stdout.encoding, errors='replace'))

        conn.execute("UPDATE Recipe SET CleanIngredients=? where ID=?", (ingredients, iden))
    
    conn.commit()
    conn.close()
    
print("Starting cleaning process...")
#Split into batches for processing
start = timeit.default_timer()

thread_batch = [tuple([tuple(ingredients[x*1000:(x+1)*1000]), ing_dict, sd.synonymdict, sd.deletethese]) for x in range(0, (len(ingredients)//1000)+1)]

with concurrent.futures.ThreadPoolExecutor(3) as executor:
    executor.map(cleanIngredients, thread_batch)

stop = timeit.default_timer()
print(str(stop - start)) 