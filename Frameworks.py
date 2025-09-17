#Load it into a pandas DataFrame:
import pandas as pd

# Load the metadata CSV file
df = pd.read_csv('metadata.csv')

# Examine the first few rows and data structure
print(df.head())
print(df.info())

#Basic Data Exploration:
#Check the DataFrame dimensions:
print("DataFrame dimensions:", df.shape)  # (rows, columns)

#Identify data types of each column:
print("Data types of each column:\n", df.dtypes)

#Check for missing values in important columns:

print("Missing values:\n", df.isnull().sum())

#Generate basic statistics for numerical columns:
print("Basic statistics for numerical columns:\n", df.describe())

#2.Data Cleaning and Preparation
#Identify columns with many missing values:

missing_values = df.isnull().mean() * 100
print("Percentage of missing values:\n", missing_values[missing_values > 0])

#Create a cleaned version of the dataset:

# Dropping columns with more than 50% missing values
df_cleaned = df.drop(columns=missing_values[missing_values > 50].index)

# Filling missing values in specific columns
df_cleaned['abstract'].fillna('', inplace=True)  # Example of filling with an empty string

#Prepare data for analysis:
#Convert date columns to datetime format:

df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')

#Extract year from publication date:
df_cleaned['publish_year'] = df_cleaned['publish_time'].dt.year

#Create new columns if needed (e.g., abstract word count):
df_cleaned['abstract_word_count'] = df_cleaned['abstract'].apply(lambda x: len(x.split()))

#Data Analysis and Visualization
#Count papers by publication year

papers_per_year = df_cleaned['publish_year'].value_counts().sort_index()
print("Papers by publication year:\n", papers_per_year)

#top_journals = df_cleaned['journal'].value_counts().head(10)
print("Top journals:\n", top_journals)

#Find most frequent words in titles:

from collections import Counter
import re

titles = df_cleaned['title'].dropna().tolist()
words = [word for title in titles for word in re.findall(r'\w+', title.lower())]
most_common_words = Counter(words).most_common(10)
print("Most common words in titles:\n", most_common_words)

#Create visualizations:
#Plot number of publications over time:

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
papers_per_year.plot(kind='bar')
plt.title('Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.show()

#Create a bar chart of top publishing journals:
plt.figure(figsize=(10, 5))
top_journals.plot(kind='bar')
plt.title('Top Journals Publishing COVID-19 Research')
plt.xlabel('Journal')
plt.ylabel('Number of Publications')
plt.show()

#Generate a word cloud of paper titles:

from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=400).generate(' '.join(titles))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#Plot distribution of paper counts by source:

source_counts = df_cleaned['source'].value_counts()
plt.figure(figsize=(10, 5))
source_counts.plot(kind='bar')
plt.title('Distribution of Paper Counts by Source')
plt.xlabel('Source')
plt.ylabel('Number of Publications')
plt.show()

#Build a simple Streamlit app:

import streamlit as st

st.title('COVID-19 Research Publications Analysis')
st.write('This app provides insights into the COVID-19 research publications.')

# Add interactive widgets
year = st.slider('Select Year', min_value=int(df_cleaned['publish_year'].min()), max_value=int(df_cleaned['publish_year'].max()))
filtered_data = df_cleaned[df_cleaned['publish_year'] == year]

st.write(f'Number of publications in {year}: {len(filtered_data)}')
st.write(filtered_data[['title', 'journal', 'abstract']].head())

# Display visualizations
st.subheader('Number of Publications Over Time')
st.bar_chart(papers_per_year)

st.subheader('Top Journals Publishing COVID-19 Research')
st.bar_chart(top_journals)

st.subheader('Word Cloud of Paper Titles')
st.image(wordcloud.to_array())






