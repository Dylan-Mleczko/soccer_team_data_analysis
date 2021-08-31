import json
from matplotlib import pyplot as plt
import nltk
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from sklearn.feature_extraction.text import TfidfTransformer

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
    csv_data = pd.DataFrame.from_dict(club_data, orient = "index", columns = ["goals_scored_by_team", "goals_scored_against_team"]).sort_index()
    csv_data.to_csv("task2.csv", index_label = "club_code")
    return
      
def task3():
    total_scores = {}
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()    
        scores = re.findall(r"(\d+)-(\d+)", article)
        largest_score = 0
        for score in [score for score in scores if len(score[0]) <= 2 and len(score[1]) <= 2]:
            score = int(score[0]) + int(score[1])
            if score > largest_score:
                largest_score = score
        total_scores[file] = largest_score
    pd.DataFrame.from_dict(total_scores, orient = "index", columns = ["total_goals"]).sort_index().to_csv("task3.csv", index_label = "filename")
    return

def task4():
    plt.boxplot(pd.read_csv("task3.csv")["total_goals"])
    plt.title("Distribution of Total Goals from Soccer Matches")
    plt.xticks([])
    plt.savefig("task4.png")
    return
    
def task5():
    with open(datafilepath) as file:
        clubs = json.load(file)["participating_clubs"]
    club_mentions = {}
    for club in clubs:
        club_mentions[club] = 0
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()
        for club in clubs:
            club_mentions[club] += club in article
    pd.DataFrame.from_dict(club_mentions, orient = "index", columns = ["number_of_mentions"]).sort_index().to_csv("task5.csv", index_label = "club_name")
    csv_data = pd.read_csv("task5.csv")
    plt.bar(csv_data["club_name"], csv_data["number_of_mentions"])
    plt.title("Soccer Team Mentions in Media")
    plt.xlabel("Team Name")
    plt.ylabel("Number of Articles Mentioning Team at Least Once")
    plt.xticks(rotation = 90)
    plt.savefig("task5.png", bbox_inches = "tight")
    return
    
def task6():
    with open(datafilepath) as file:
        clubs = json.load(file)["participating_clubs"]
    single_club_mentions = [0 for i in range(len(clubs))]
    pair_club_mentions = [len(clubs) * [0] for i in range(len(clubs))]
    similarity_scores = [len(clubs) * [0] for i in range(len(clubs))]
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()
        for i in range(len(clubs)):
            if clubs[i] in article:
                single_club_mentions[i] += 1
                for j in range(i + 1, len(clubs)):
                    if clubs[j] in article:
                        pair_club_mentions[i][j] += 1
                        pair_club_mentions[j][i] += 1
    for i in range(len(clubs)):
        for j in range(len(clubs)):
            if i == j:
                similarity_scores[i][j] = similarity_scores[j][i] = 1
            elif single_club_mentions[i] + single_club_mentions[j] > 0:
                similarity_scores[i][j] = similarity_scores[j][i] = (2 * pair_club_mentions[i][j]) / (single_club_mentions[i] + single_club_mentions[j])
    similarity_scores_dataframe = pd.DataFrame(similarity_scores, index = clubs, columns = clubs).sort_index(axis = 0).sort_index(axis = 1)
    sns.heatmap(similarity_scores_dataframe, cbar_kws = {"label": "Similarity Score of Team Pair"}, cmap = "rainbow")
    plt.title("Similarity in Media Mentions between Soccer Teams")
    plt.savefig("task6.png", bbox_inches = "tight")
    return
    
def task7():
    plt.scatter(pd.read_csv("task5.csv")["number_of_mentions"], pd.read_csv("task2.csv")["goals_scored_by_team"])
    plt.title("Correlation between Soccer Team Mentions in Media and Goals")
    plt.xlabel("Number of Articles Mentioning Team at Least Once")
    plt.ylabel("Number of Total Goals Scored by Team")
    plt.savefig("task7.png")
    return
    
def task8(filename):
    with open(filename) as file:
        article = file.read()
    return [word for word in nltk.word_tokenize(re.sub(r"[^A-Za-z]+", " ", article.lower())) if (word not in nltk.corpus.stopwords.words("english")) and (len(word) > 1)]
    
def task9():
    transformer = TfidfTransformer()
    article_names = [file for file in sorted(os.listdir(articlespath)) if ".txt" in file]
    articles = [task8(articlespath + "/" + article) for article in article_names]
    terms = []
    for article_terms in articles:
        terms += article_terms
    terms = sorted(list(set(terms)))
    term_counts = [len(terms) * [0] for i in range(len(articles))]
    for i in range(len(articles)):
        for word in articles[i]:
            term_counts[i][terms.index(word)] += 1
    tfidf = transformer.fit_transform(term_counts).toarray()
    similarity_scores = []
    for i in range(len(article_names)):
        for j in range(i + 1, len(article_names)):
            similarity_scores += [[article_names[i], article_names[j], np.dot(tfidf[i], tfidf[j]) / (np.linalg.norm(tfidf[i]) * np.linalg.norm(tfidf[j]))]]
    pd.DataFrame(similarity_scores, columns = ["article1", "article2", "similarity"]).nlargest(10, "similarity").to_csv("task9.csv", index = False)
    return