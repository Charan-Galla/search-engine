'''
	The below code indexes all the documents and finds the tf-idf (term frequency and inverse document frequency) score for all the words in the documents

'''

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import nltk
import string
import numpy as np
import pickle

'''
	The corpus is read from an excel sheet using pandas dataframe
'''
corpus = pd.read_excel('input.xlsx')

ps = PorterStemmer()
n = 10000
stop = set(stopwords.words('english'))
unique_words = []
documents = []
for i in range(n):
    sentence = corpus.iloc[i,0]
    sentence = sentence.strip()
    sentence = sentence.lower()						#makes all letters lowercase
    sentence = re.sub('<[^<]+?>', ' ', sentence)   	#removes all html tags present in the text using regex
    sentence = re.sub(r'[^\w\s]',' ', sentence)    	#removes all punctuation present in the text using regex
    token = nltk.word_tokenize(sentence)			#tokenizes the sentence into a list token
    #token = [word for word in token if word not in stop]
    token = [ps.stem(word) for word in token]    	#Porter Stemming Algorithm for stemming of words
    documents.append(token)
    for word in token:
        if word not in unique_words:
            unique_words.append(word)

n = len(documents)
m = len(unique_words)
'''
	Occurences is a dictionary which has all unique words as key and has the document numbers with all the position of occurences as the value.
'''

occurences = {}
for word in unique_words:
    d = {}
    for i in range(n):
        tmp = [j for j, val in enumerate(documents[i]) if val==word]
        if tmp:
            d[i]=tmp
    occurences[word] = d

idf = {}
tf = {}
'''
	tf of a word in a document is calculated using the formula tf(word,document) = 1+log(n), where n=number of times the word appears in the document
	idf of a word for all documents is calculated using the formula idf(word) = log(N/tf(i)) where N=total number of documents and tf(i) = number of documents the ith word occurs
'''
for key,val in iter(occurences.items()):
    raw_tf = {}
    idf[key] = np.math.log((n/len(val.keys())),10)
    for doc_key,doc_val in iter(val.items()):
        if len(doc_val) > 0:
            raw_tf[doc_key] = 1 + np.math.log(len(doc_val),10)
        else:
            raw_tf[doc_key] = 0
    tf[key] = raw_tf

'''
	The tf vector needs to be length normalized so that the cosine formula can be used
'''
for i in range(n):
    tmp = []
    l = 0.0
    for word in documents[i]:
        if word not in tmp:
            tmp.append(word)
    for word in tmp:
        l = l + np.math.pow(tf[word][i],2)
    l = np.math.sqrt(l)
    for word in tmp:
        tf[word][i] = tf[word][i]/l
		
'''
	Using pickle library, the tf and idf dictionaries calculated are stored to be used by another python file
'''
filehandler = open("tf_dump",'wb+')
pickle.dump(tf,filehandler)

filehandler = open("idf_dump",'wb+')
pickle.dump(idf,filehandler)