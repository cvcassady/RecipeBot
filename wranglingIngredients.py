import datetime
import json
from json import JSONDecodeError
import urllib.request
from urllib.error import HTTPError
import sqlite3
import os
import sys
import numpy as np
import re
import difflib

conn = sqlite3.connect("yummly.db")
ingredients = conn.execute("SELECT Ingredients FROM Recipe;").fetchall()
conn.close()

ingredients = [x[0].lower().split("; ") for x in ingredients]
#ingredients = [re.findall(r"[a-zA-Z]+", x[0].lower()) for x in ingredients]

ingredients = np.array([item for sublist in ingredients for item in sublist])


unique_ing = np.unique(ingredients, return_counts = True)
argsort_results = np.argsort(unique_ing[1])

sorted_ing = unique_ing[0][argsort_results]
sorted_vals = unique_ing[1][argsort_results]
sorted_ing = sorted_ing[::-1]
sorted_vals = sorted_vals[::-1]

f = open("ingredients_by_frequency.txt", "w")
[f.write(str(sorted_vals[i]) + "\t\t" + sorted_ing[i] + "\n") for i in range(0, len(sorted_vals))]
f.close()

findRoot("gluten-free chocolate chips", sorted_ing)

#ing = the ingredient in question
#ingredients_list is a SORTED list of ingredients, 
#   With 0 being the most common ingredient
def findRoot(ing, ingredients_list):
    ing = ing.split(" ")
    len_ingredients_list = len(ingredients_list)

    # This terrible looking line of code generates bigrams backwards, then taks on the split
    # ingredients string, backwards. The idea being that the identifying information is usually
    # at the end of the string (from basic visual analysis)
    ing = [ing[x] + " " + ing[x+1] for x in reversed(range(0,(len(ing) - 1)))] + ing[::-1]

    # we then pair each candidate with a zero, to denote our confidence that it is that ingredient
    candidates = [[x, 0] for x in ing]

    for can_index, candidate in enumerate(candidates):
        # give a slight bump to things near the front of the list
        candidate[1] = 0.01 / (can_index+1)
        
        #search for the bigram in the ingredients list
        candidate = searchList(candidate, ingredients_list)
    return candidates



def searchList(candidate, ingredients_list):
    for index, ingredient in enumerate(ingredients_list):

        current_ingredient_depluralized = ingredient.replace('es','').replace('s','')
        current_candidate_depluralized = candidate[0].replace('es','').replace('s','')

        if current_ingredient_depluralized == current_candidate_depluralized:
            candidate[1] = candidate[1] + (len_ingredients_list - index) / len_ingredients_list
            return candidate
