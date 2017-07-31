# RecipeBot
RecipeBot is a project by Colin Cassady and Kerry Jones for the Machine Vision and Language
course at University of Virginia. The intent is to teach a deep neural network to guess the 
ingredients of a dish simply through viewing an image of it.

# Required Libraries and Packages
SQLite
TensorFlow
Keras
Numpy
Urlib
Scikit-Learn
Scikit-Image
Matplotlib
Bokeh


# yummly.db schema
* **ID** is a guid
* **JSON** is all data returned from yummly per recipe
* **Title** is the title of the recipe
* **Ingredients** is a semicolon delimited string of unprocessed ingredients
* **ImageUrl** contains the url to the image on yummly.co
* **Description** is a short description of the dish
* **Url** holds the url to the recipe page on yummly.co
* **Course** is the course of the dish in context of different types of meals. (Breakfast, dessert, drinks etc.)
* **CleanIngredients** is a semicolon delimited string of processed ingredients
* **ImageAvailable** describes whether or not an image exists for a given recipe (some don't have images)
* **English** describes whether or not the recipe was written in the English language

To make this table, open SQLite in the desired folder and paste the following table creation statement:

>     CREATE TABLE Recipe(
>        ID TEXT PRIMARY KEY     NOT NULL,
>        JSON TEXT    NOT NULL,
>        Title TEXT,
>        Ingredients TEXT,
>        ImageUrl TEXT,
>        Description TEXT,
>        Url TEXT,
>        Course TEXT,
>        CleanIngredients TEXT,
>        ImageAvailable INT,
>        English INT);

# Flow of the project
The project generally flows in the following script order.


**scrapingyummly.py**
Queries yummly.co for the search term 'recipe', and iterates through
all of the results, storing them in yummly.db.

**downloadimages.py**
Reads all image URL and ID's from yummly.db, then downloads all images
contained within.

**resizingImages.py**
Resizes all images in the folder 'images' to 224x224 (input size of VGG)
and stores them in folder 'resized_thumbs'. This allows for faster training.

**markImagelessRecipes.py**
Iterates through all files in resized_thumbs and for each one found sets
ImageAvailable=1 in yummly.db

**wranglingIngredients.py**
Attempts to clean the ingredients from each recipe, storing the cleaned
ingredients in the CleanIngredients column of yummly.db
(e.g. 1 cup low fat cottage cheese => cottage cheese)

**IngredientsPredictionModel.ipynb**
Defines and trains the network.

# Sample Output
![Sample output from the network. Picture of tacos taken by my brother, the network has never seen it before.](http://i.imgur.com/uU5Nw1K.png)

