# Recipe Analysis

This is a repository I'm using to experiment with different tools and 
techniques on a dataset of recipes scraped from allrecipes.com.

The data comes from https://archive.org/download/recipes-en-201706/

I followed the approach from the New York Times with parsing recipe ingredients
described here: 
* https://github.com/nytimes/ingredient-phrase-tagger
* https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-r
ecipes-using-conditional-random-fields/?_r=0

## Things I'd like to do with this repository
* Cluster recipes on ingredients and instructions
    * What kind of recipes are similar in terms of ingredients or techniques?
    * How does the same recipe vary across different authors and styles?
* Analysis of ingredients and instructions by cuisine or type of food
    * What kind of simlarities and differences are there among different styles
    of food?
    * Given a new recipe with a set of ingredients and instructions, what kinds
    of recipes is this recipe most simlar to? 
* Communcation and visualization of instructions
    * What other ways can recipe instructions be presented or communicated? 
* Prediction of ingredients, instructions, or reviews
    * If we know any of these three things, can we predict the others? E.g. if 
    there are fewer ingredients or "easier" instructions, can we predict how 
    many stars the recipe will recieve?
