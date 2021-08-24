import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
import os
import re

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
    total_scores = {}
    for file in [file for file in os.listdir(articlespath) if ".txt" in file]:
        with open(articlespath + "/" + file) as article:
            scores = re.findall(r"(\d+)-(\d+)", article.read())
            largest_score = 0
        for score in [score for score in scores if len(score[0]) <= 2 and len(score[1]) <= 2]:
            score = int(score[0]) + int(score[1])
            if score > largest_score:
                largest_score = score
        total_scores[file] = largest_score
    csv_data = pd.DataFrame.from_dict(total_scores, orient = "index", columns = ["total_goals"])
    csv_data.sort_index().to_csv("task3.csv", index_label = "filename")
    return

def task4():
    plt.boxplot(pd.read_csv("task3.csv")["total_goals"])
    plt.title("Distribution of Total Goals from Soccer Matches")
    plt.xticks([])
    plt.savefig("task4.png")
    return
    
def task5():
    club_mentions = {}
    with open(datafilepath) as file:
        for club in json.load(file)["participating_clubs"]:
            club_mentions[club] = 0
    for file in [file for file in os.listdir(articlespath) if ".txt" in file]:
        with open(articlespath + "/" + file) as article:
            article = article.read()
            for club in club_mentions:
                club_mentions[club] += club in article
    csv_data = pd.DataFrame.from_dict(club_mentions, orient = "index", columns = ["number_of_mentions"])
    csv_data.sort_index().to_csv("task5.csv", index_label = "club_name")
    csv_data = pd.read_csv("task5.csv")
    plt.bar(csv_data["club_name"], csv_data["number_of_mentions"])
    plt.title("Soccer Club Mentions in Media")
    plt.xlabel("Club Name")
    plt.ylabel("Number of Articles Mentioning Club at Least Once")
    plt.xticks(rotation = 90)
    plt.savefig("task5.png", bbox_inches = "tight")
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