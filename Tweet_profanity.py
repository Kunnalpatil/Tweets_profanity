# import nessecary packages

import pandas as pd
import re
import nltk



# Took this file of tweets for analysis from github
df = pd.read_csv('https://raw.githubusercontent.com/vzhou842/profanity-check/master/profanity_check/data/clean_data.csv')
df.drop('is_offensive',axis=1,inplace=True)


df['text']=df['text'].astype(str)
df['text'] = df['text'].apply(lambda x: x.lower())


# Assuming I need to do analysis after removing the mentions, hashtags, links etc.
#Text cleaning
df['clean_text'] = df['text'].apply(lambda x : re.sub(r'#[a-zA-z]+|#[a-zA-z]+\d+|https:\/\/\S+|http:\/\/\S+|\\n|@[a-z]+|@[a-z]+\d+',"",x))

# Breaking the tweet in to sentences Assuming I have to count the profanity for each sentence
# I have also counted it on whole tweet as well.
df['sentences'] = df['clean_text'].apply(lambda x: nltk.sent_tokenize(x))

# List to store the profane words
profane_words =[]

# Reading the profane words from file and appending it list above for use.
with open('C:/Users/kunna/Downloads/badwords.txt', 'r',encoding='latin-1') as input_file:
        for line in input_file.readlines():
          line = line.replace("\n", "")
          profane_words.append(line)
          
          

# this function computes the degree of profanity of a sentence
# formula used :- (total number of profane words in a sentence/ number of words in that senctence * 10)
# This outputs a list with score for each sentence , as there can be N number of sentences in a tweet
def degree_of_profanity(text):
  l1 = []
  for sentence in text:
    counter = 0
    for word in sentence.split():
      if word in profane_words:
        counter += 1
    l1.append(round(counter/len(sentence.split()),2)*10)

  return l1

# Sentence wise profanity stored in list format in below column
df['degree_of_profanity_sentence_wise'] = df['sentences'].apply(degree_of_profanity)


# The below function counts profanity tweet wise rather the for each sentence in it.
def degree_of_profanity_tweets(clean_text):
  counter = 0
  for word in clean_text.split():
      if word in profane_words:
        counter += 1
  try:
    return (round(counter/len(clean_text.split()),2)*10)
  except ZeroDivisionError:
   return 0


# profanity count tweet wise is stored in below column
df['degree_of_profanity_for_tweet'] = df['clean_text'].apply(degree_of_profanity_tweets)


# Storing the final output to excel
df.to_excel('C:/Users/kunna/Downloads/Final_file.xlsx',index=False)

























