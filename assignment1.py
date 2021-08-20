# This is the file you will need to edit in order to complete assignment 1
# You may create additional functions, but all code must be contained within this file


# Some starting imports are provided, these will be accessible by all functions.
# You may need to import additional items
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json

# You should use these two variable to refer the location of the JSON data file and the folder containing the news articles.
# Under no circumstances should you hardcode a path to the folder on your computer (e.g. C:\Chris\Assignment\data\data.json) as this path will not exist on any machine but yours.
datafilepath = 'data/data.json'
articlespath = 'data/football'

def task1():
    with open(datafilepath) as file:
        data = json.load(file)
    return sorted(data["teams_codes"])
    
def task2():
    with open(datafilepath) as file:
        data = json.load(file)
    club_data = {}
    for club in data["clubs"]:
        club_data[club["club_code"]] = [club["goals_scored"], club["goals_conceded"]]
    csv_data = pd.DataFrame.from_dict(club_data, orient = "index", columns = ["goals_scored_by_team", "goals_scored_against_team"])
    csv_data.sort_index().to_csv("task2.csv", index_label = "club_code")
    return
      
def task3():
    #Complete task 3 here
    return

def task4():
    #Complete task 4 here
    return
    
def task5():
    #Complete task 5 here
    return
    
def task6():
    #Complete task 6 here
    return
    
def task7():
    #Complete task 7 here
    return
    
def task8(filename):
    #Complete task 8 here
    return
    
def task9():
    #Complete task 9 here
    return