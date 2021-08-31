# comp20008-2021sm2a1
Dylan Cookson-Mleczko (1173182)

#### Project Description
- *Task 1:* Returns `team_codes` as list from `data.json` sorted by team code
- *Task 2:* Creates `task2.csv` displaying goals scored by and against each team from `data.json` sorted by team code
- *Task 3:* Creates `task3.csv` disaplying largest match score indentified in each article sorted by article name
- *Task 4:* Creates `task4.png` displaying boxplot showing distribution of values for `total_goals` in `task3.csv`
- *Task 5:* Creates `task5.csv` and `task5.png` both displaying number of times each team is mentioned by an article at least once sorted by team name
- *Task 6:* Creates `task6.png` displaying heatmap showing similarity score for each pair of teams
- *Task 7:* Creates `task7.png` displaying scatterplot comparing the number of articles mentioning each team with the total number of goals scored by each team
- *Task 8:* Returns article located at provided `filepath` as string after removing non-alphabetic characters, excess whitespace, uppercase, stopwords and single characters
- *Task 9:* Creates `task9.csv` containing top 10 article pairs with highest cosine similarity measures by comparing TF-IDF vectors sorted in descending order

#### Dependencies
- json
- pyplot (matplotlib)
- nltk
- numpy
- os
- pandas
- re
- seaborn
- TfidfTransformer (sklearn.feature_extraction.text)