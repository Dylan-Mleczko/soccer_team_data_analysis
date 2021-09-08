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
        team_codes = json.load(file)["teams_codes"]
    return sorted(team_codes)
    
def task2():
    with open(datafilepath) as file:
        data = json.load(file)
    team_goals = {}
    for team in data["clubs"]:
        team_goals[team["club_code"]] = [team["goals_scored"], team["goals_conceded"]]
    csv_data = pd.DataFrame.from_dict(team_goals, orient = "index", columns = ["goals_scored_by_team", "goals_scored_against_team"]).sort_index()
    csv_data.to_csv("task2.csv", index_label = "team_code")
    return
      
def task3():
    total_scores = {}
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()    
        article_scores = re.findall(r"(\d+)-(\d+)", article)
        article_largest_score = 0
        for score in [score for score in article_scores if len(score[0]) <= 2 and len(score[1]) <= 2]:
            score = int(score[0]) + int(score[1])
            if score > article_largest_score:
                article_largest_score = score
        total_scores[file] = article_largest_score
    pd.DataFrame.from_dict(total_scores, orient = "index", columns = ["total_goals"]).sort_index().to_csv("task3.csv", index_label = "filename")
    return

def task4():
    plt.boxplot(pd.read_csv("task3.csv")["total_goals"])
    plt.title("Distribution of Total Scores from Soccer Matches", fontweight = "bold")
    plt.ylabel("Soccer Match Total Score", fontweight = "bold")
    plt.xticks([])
    plt.yticks(range(0, 101, 10))
    plt.grid(True, which = "major", axis = "y")
    plt.savefig("task4.png", bbox_inches = "tight")
    plt.clf()
    return
    
def task5():
    with open(datafilepath) as file:
        teams = json.load(file)["participating_clubs"]
    team_mentions = {}
    for team in teams:
        team_mentions[team] = 0
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()
        for team in teams:
            team_mentions[team] += team in article
    pd.DataFrame.from_dict(team_mentions, orient = "index", columns = ["number_of_mentions"]).sort_index().to_csv("task5.csv", index_label = "club_name")
    csv_data = pd.read_csv("task5.csv")
    plt.bar(csv_data["club_name"], csv_data["number_of_mentions"])
    plt.title("Mentions for Soccer Teams in Articles", fontweight = "bold")
    plt.xlabel("Team", fontweight = "bold")
    plt.ylabel("Articles Mentioning Team at Least Once", fontweight = "bold")
    plt.xticks(rotation = 90)
    plt.yticks(range(0, 91, 10))
    plt.grid(True, which = "major", axis = "y")
    plt.savefig("task5.png", bbox_inches = "tight")
    plt.clf()
    return
    
def task6():
    with open(datafilepath) as file:
        teams = json.load(file)["participating_clubs"]
    single_team_mentions = [0 for i in range(len(teams))]
    pair_team_mentions = similarity_scores = [len(teams) * [0] for i in range(len(teams))]
    for file in [file for file in os.listdir(articlespath) if file.endswith(".txt")]:
        with open(articlespath + "/" + file) as article:
            article = article.read()
        for i in range(len(teams)):
            if teams[i] in article:
                single_team_mentions[i] += 1
                for j in range(i + 1, len(teams)):
                    if teams[j] in article:
                        pair_team_mentions[i][j] += 1
                        pair_team_mentions[j][i] += 1
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i == j:
                similarity_scores[i][j] = similarity_scores[j][i] = 1
            elif single_team_mentions[i] + single_team_mentions[j] > 0:
                similarity_scores[i][j] = (2 * pair_team_mentions[i][j]) / (single_team_mentions[i] + single_team_mentions[j])
    dataframe = pd.DataFrame(similarity_scores, index = teams, columns = teams).sort_index(axis = 0).sort_index(axis = 1)
    sns.heatmap(dataframe, cbar_kws = {"label": "Team Pair Similarity Score", "ticks": np.arange(0, 1.1, 0.1)}, cmap = "rainbow")
    plt.title("Similarity of Article Mentions between Soccer Teams", fontweight = "bold")
    plt.savefig("task6.png", bbox_inches = "tight")
    plt.clf()
    return
    
def task7():
    with open(datafilepath) as file:
        team_data = json.load(file)["clubs"]
    team_name_codes = {}
    for team in team_data:
        team_name_codes[team["name"]] = team["club_code"]
    task5_csv_data = pd.read_csv("task5.csv")
    for row in range(len(task5_csv_data)):
        task5_csv_data.loc[row, "club_name"] = team_name_codes[task5_csv_data.loc[row, "club_name"]]
    plt.scatter(pd.read_csv("task2.csv")["goals_scored_by_team"], task5_csv_data.sort_values(by = "club_name")["number_of_mentions"])
    plt.title("Relationship between Goals Scored by Soccer Teams and Mentions in Articles", fontweight = "bold")
    plt.xlabel("Total Goals Scored by Team", fontweight = "bold")
    plt.ylabel("Articles Mentioning Team at Least Once", fontweight = "bold")
    plt.xticks(range(0, 13, 1))
    plt.yticks(range(0, 101, 10))
    plt.grid(True)
    plt.savefig("task7.png", bbox_inches = "tight")
    plt.clf()
    return
    
def task8(filename):
    with open(filename) as file:
        article = file.read()
    return [word for word in nltk.word_tokenize(re.sub(r"[^A-Za-z]+", " ", article.lower())) if (word not in nltk.corpus.stopwords.words("english")) and (len(word) > 1)]
    
def task9():
    transformer = TfidfTransformer()
    article_names = [file for file in sorted(os.listdir(articlespath)) if file.endswith(".txt")]
    articles = [task8(articlespath + "/" + article) for article in article_names]
    all_terms = []
    cosine_similarity_scores = []
    for article in articles:
        all_terms += article
    all_terms = sorted(list(set(all_terms)))
    term_counts = [len(all_terms) * [0] for i in range(len(articles))]
    for i in range(len(articles)):
        for term in articles[i]:
            term_counts[i][all_terms.index(term)] += 1
    tfidf = transformer.fit_transform(term_counts).toarray()
    for i in range(len(article_names)):
        for j in range(i + 1, len(article_names)):
            cosine_similarity_scores += [[article_names[i], article_names[j], np.dot(tfidf[i], tfidf[j]) / (np.linalg.norm(tfidf[i]) * np.linalg.norm(tfidf[j]))]]
    pd.DataFrame(cosine_similarity_scores, columns = ["article1", "article2", "similarity"]).nlargest(10, "similarity").to_csv("task9.csv", index = False)
    return