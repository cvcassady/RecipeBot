# RecipeBot
RecipeBot is a project by Colin Cassady for the Vision and Language
course at University of Virginia. The intent is to teach a deep
neural network to guess the ingredients of a dish simply through
viewing an image of it. All information will be scraped from the
website yummly.co.

# yummly.db schema
# ID is a guid
# JSON is all data returned from yummly per recipe
# Ingredients is a semicolon delimited string of ingredients
# Url holds the url to the recipe page on yummly.co
CREATE TABLE Recipe(
   ID TEXT PRIMARY KEY     NOT NULL,
   JSON TEXT    NOT NULL,
   Title TEXT,
   Ingredients TEXT,
   ImageUrl TEXT,
   Description TEXT,
   Url TEXT);