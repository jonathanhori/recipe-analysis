#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:33:39 2019

@author: jonathanhori

I'm playing around with recipe data here. I'd like to compare recipes across 
ingredients, instructions, quantities, ratings, etc. 

Data:
* https://archive.org/download/recipes-en-201706/

NYTimes on cleaning recipe ingredients
* https://github.com/nytimes/ingredient-phrase-tagger
* https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-r
ecipes-using-conditional-random-fields/?_r=0


"""

import sys
sys.path.append(r'/Users/jonathanhori/Desktop/recipe-clustering')

import json
import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

filename = r'allrecipes-recipes.json'
DBNAME = 'recipes.db'
ingredient_results = r'/Users/jonathanhori/ingredient-phrase-tagger-master/results.json'

def export_data_to_sql(table, table_name):
    conn = sqlite3.connect(DBNAME)
    table.to_sql(table_name, conn, if_exists='replace')
    conn.close()
    
def read_data_from_sql(table, table_name):
    conn = sqlite3.connect(DBNAME)
    cursor = conn.cursor()
    query = 'SELECT * FROM {};'.format(table_name)
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    conn.close()
    return table

def load_data(filename):
    with open(filename) as file:
        recipe_list = file.readlines()
    
    recipe_data = list()
    for recipe in recipe_list:
        recipe_data.append(json.loads(recipe)) #.append# = json.loads(file.read())
    
    recipe_frame = pd.DataFrame.from_records(recipe_data)
    recipe_frame.to_csv('recipe_data.csv')
    return recipe_frame

'''
recipe_frame.columns

Index(['author', 'cook_time_minutes', 'description', 'error', 'footnotes',
       'ingredients', 'instructions', 'photo_url', 'prep_time_minutes',
       'rating_stars', 'review_count', 'time_scraped', 'title',
       'total_time_minutes', 'url'],
      dtype='object')


'''

def clean_data(recipe_frame):
    # Create a unique id number for each recipe
    recipe_frame['id'] = recipe_frame.index
        
    # Process ingredients separately
    ingredient_frame = pd.DataFrame({'id': recipe_frame.id, 
                                     'ingredients': recipe_frame.ingredients})
    ingredients = ingredient_frame.ingredients.apply(pd.Series) \
                                .join(ingredient_frame) \
                                .drop('ingredients', axis=1) \
                                .melt(id_vars=['id'], value_name='ingredient')\
                                .dropna()
    export_data_to_sql(ingredients, 'ingredients')
    recipe_frame = recipe_frame.drop('ingredients', axis=1)
           
    # Process instructions separately                     
    instruction_frame = pd.DataFrame({'id': recipe_frame.id,
                                      'instructions': recipe_frame.instructions})                
    instructions = instruction_frame.instructions.apply(pd.Series) \
                                .join(instruction_frame) \
                                .drop('instructions', axis=1) \
                                .melt(id_vars=['id'], value_name='instruction')\
                                .dropna()
    export_data_to_sql(instructions, 'instructions')
    recipe_frame = recipe_frame.drop('instructions', axis=1)

    # Process footnotes separately                     
    footnote_frame = pd.DataFrame({'id': recipe_frame.id,
                                   'footnotes': recipe_frame.footnotes})                
    footnotes = footnote_frame.footnotes.apply(pd.Series) \
                                .join(footnote_frame) \
                                .drop('footnotes', axis=1) \
                                .melt(id_vars=['id'], value_name='footnote')\
                                .dropna()
    export_data_to_sql(footnotes, 'footnotes')
    recipe_frame = recipe_frame.drop('footnotes', axis=1)
    
    # Export cleaned recipe frame
    export_data_to_sql(recipe_frame, 'recipes')

    return recipe_frame, ingredients, instructions, footnotes


def parse_ingredients(ingredients):
    '''Ingredients input is table of ingredients from db with columns [
    id, variable, ingredient]'''
    
    # First export column of ingredient field to .txt file.
    # Train NYTimes model from command line
    # Run model on exported data. 
    # Results are located here:
    # /Users/jonathanhori/ingredient-phrase-tagger-master/results.json
    
    # ingredients.iloc[:,-1].to_csv(r'ingredient_data_new.txt', 
     #               header=None, index=None, sep=' ', mode='a')
    
    with open(ingredient_results) as file:
        ingredients_parsed = json.load(file)
    ingredients_parsed_frame = pd.DataFrame(ingredients_parsed)
    ingredients_parsed_frame.input = ingredients_parsed_frame.input.str.strip('\"')
    ingredients_parsed_frame.qty = ingredients_parsed_frame.qty.str.strip('\"')
    ingredients_parsed_frame.name = ingredients_parsed_frame.name.str.strip('\"')
    ingredients_parsed_frame.comment = ingredients_parsed_frame.comment.str.strip('\"')
    ingredients_parsed_frame = ingredients_parsed_frame.drop('display', axis=1)

    export_data_to_sql(ingredients_parsed_frame, 'ingredients_parsed')
    
#    ingredients_merged = ingredients.join(ingredients_parsed_frame)

#    np.array_equal(ingredients_merged.input, 
#                   ingredients_merged.ingredient)
#    # This is false, need to merge on ingredient==input
##    ingredients_merged = ingredients.merge(ingredients_parsed_frame, 
##                                           left_on='ingredient', 
##                                           right_on='input')
#    
#    export_data_to_sql(ingredients_parsed_frame, 'ingredients_parsed')
    return ingredients_parsed_frame
    
def setup_for_analysis():
    return
    



    



