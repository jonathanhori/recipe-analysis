#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:33:39 2019

@author: jonathanhori

I'm playing around with recipe data here. I'd like to compare recipes across 
ingredients, instructions, quantities, ratings, etc. 

https://github.com/nytimes/ingredient-phrase-tagger
https://archive.org/download/recipes-en-201706/
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

def export_data_to_sql(table, table_name):
    conn = sqlite3.connect(DBNAME)
    table.to_sql(table_name, conn)


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
    
    export_data_to_sql(recipe_frame, 'recipes')

    




    



