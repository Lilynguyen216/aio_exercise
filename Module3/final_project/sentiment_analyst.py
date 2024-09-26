# -*- coding: utf-8 -*-
"""sentiment_analyst.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-FrZT2JORwY8mKDurLoUHuETe3Ycr4f4
"""

# !gdown 1nxR07ebVNc5bSgfTQjeUcAoyoaNuuH6s

import pandas as pd

# /workspaces/AIO_Exercise/Module3/dataset/IMDB-Dataset.csv
df = pd.read_csv('/workspaces/AIO_Exercise/Module3/dataset/IMDB-Dataset.csv')
df = df.drop_duplicates()
df.head()

# !pip install contractions

import os
import re
import string
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import contractions

stop = set(stopwords.words('english'))

def expand_contractions(text):
    return contractions.fix(text)

def preprocess_text(text):
    wl = WordNetLemmatizer()

    # if os.path.exists(text):  # Kiểm tra nếu text là đường dẫn tệp hợp lệ
    #     with open(text, 'r', encoding='utf-8') as file:
    #         text = file.read()

    # soup = BeautifulSoup(text, "html.parser")
    text = BeautifulSoup(text, "html.parser").get_text()
    text = expand_contractions(text)

    # emoji_clean = re.compile("[", flads=re.UNICODE)
    emoji_clean = re.compile( "["
                        u"\U0001F600-\U0001F64F" # emoticons
                        u"\U0001F300-\U0001F5FF" # symbols & pictographs
                        u"\U0001F680-\U0001F6FF" # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        "]+", flags=re.UNICODE )
    text = emoji_clean.sub(r'', text)
    text = re.sub(r'\.(?=\S)', '. ', text)
    text = re.sub(r'https\S+', '', text)
    text = "".join([
      word.lower () for word in text if word not in string . punctuation
    ]) # remove punctuation and make text lowercase
    text = " ".join([
      wl.lemmatize(word) for word in text.split() if word not in stop and word.isalpha()
    ]) # lemmatize
    return text

df['review'] = df['review'].apply(preprocess_text)

df['review'].head()

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Create autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)

freq_pos = len(df[df['sentiment'] == 'positive'])
freq_neg = len(df[df['sentiment'] == 'negative'])

data = [freq_pos, freq_neg]
labels = ['positive','negative']

# Create pie chart
pie, ax = plt.subplots(figsize=(11, 7))
plt.pie(x=data, autopct=lambda pct: func(pct, data),
        explode=[0.0025]*2, pctdistance=0.5, colors=[sns.color_palette()[0],'tab:red'], textprops ={'fontsize': 16})

labels = [r'Positive', r'Negative']
plt.legend(labels, loc='best', prop={'size': 14})
plt.savefig("PieChart.png")
plt.show()

words_len = df['review'].str.split().map(lambda x: len(x))
df_temp = df.copy()
df_temp['words length'] = words_len

# Positive
hist_positive = sns.displot(
    data=df_temp[df_temp['sentiment'] == 'positive'],
    x='words length', hue='sentiment', kde=True, height=7,
    aspect=1.1, legend=False
).set(title='Words in positive reviews')

plt.show()
# plt.show(hist_positive)

# Negative
hist_negative = sns.displot(
    data=df_temp[df_temp['sentiment'] == 'negative'],
    x='words length', hue='sentiment', kde=True, height=7,
    aspect=1.1, legend=False, palette=['red']
).set(title='Words in negative reviews')

plt.show()
# plt.show(hist_negative)

plt.figure(figsize=(7,7))

kernel_distribution_number_words_plot = sns.kdeplot(
    data=df_temp,
    x='words length',
    hue='sentiment',
    fill=True,
    palette=[sns.color_palette()[0],'red']
).set(title='Words in reviews')

plt.legend(title='Sentiment', labels=['negative', 'positive'])
plt.show(kernel_distribution_number_words_plot)

df.head()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

label_encode = LabelEncoder()
x_data = df['review']
y_data = label_encode.fit_transform(df['sentiment'])

x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data,
    test_size=0.2,
    random_state=42
)

tfidf_vectorizer = TfidfVectorizer(max_features=10000)
tfidf_vectorizer.fit(x_train, y_train)

x_train_encoded = tfidf_vectorizer.fit_transform(x_train)
x_test_encoded = tfidf_vectorizer.transform(x_test)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

dt_classifier = DecisionTreeClassifier(
    criterion='entropy',
    random_state=42
)

dt_classifier.fit(x_train_encoded, y_train)
y_pred = dt_classifier.predict(x_test_encoded)
dt_accuracy = accuracy_score(y_pred, y_test)
print("Decision Tree Accuracy:", dt_accuracy)

rf_classifier = RandomForestClassifier(
    n_estimators=100,
    criterion='entropy',
    random_state=42
)

rf_classifier.fit(x_train_encoded, y_train)
y_pred = rf_classifier.predict(x_test_encoded)
rf_accuracy = accuracy_score(y_pred, y_test)
print("Random Forest Accuracy:", rf_accuracy)