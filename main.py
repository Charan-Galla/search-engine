'''
	The tf-idf for the documents has been calculated in preprocessing.py
	The below code takes query as input and returns the relevant documents according to the scores calculated
'''
"""
	Flask package is used for making the GUI
"""
from flask import Flask, render_template, request
app = Flask(__name__)
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize
import nltk
import numpy as np
import pickle
import heapq
import itertools

'''
	Pickle is used to load the dictionaries saved from preprocessing.py
'''

n = 10000
filehandler = open("tf_dump", 'rb+')
tf = pickle.load(filehandler)

filehandler = open("idf_dump", 'rb+')
idf = pickle.load(filehandler)
lol=[];
@app.route('/')
def home():
    return render_template('form_it.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        for key,value in result.items():
            lol.append(value)
        query=lol[0]
        ps = PorterStemmer()
        query = query.strip()
        query = query.lower()						#makes all letters lowercase
        query = re.sub('<[^<]+?>', ' ', query)   	#removes all html tags present in the text using regex
        query = re.sub(r'[^\w\s]',' ', query)    	#removes all punctuation present in the text using regex
        token = nltk.word_tokenize(query)			#the query is tokenized
        token = [ps.stem(word) for word in token]	#Porter Stemming Algorithm for stemming of words
      
        wt = {}
        tf_query = {}
    
'''
	This finds the frequency of all the words in the query
'''

        for word in token:
            if word not in tf_query:
                tf_query[word] = 1
            else:
                k = tf_query[word]
                tf_query[word] = k+1
        
'''
	The tf for the query is calculated using the formula tf(word) = 1+log(n), where n=number of times the word appears in the query
'''

        for word in tf_query.keys():
            tf_query[word] = 1 + np.math.log(tf_query[word],10)
            if word in idf.keys():
                wt[word] = tf_query[word]*idf[word]
            else:
                wt[word] = 0.0

'''
	Normalizing the tf of the query
'''

        l = 0.0
        for word in wt.keys():
            l = l + pow(wt[word],2)
        l = np.math.sqrt(l)
        for word in wt.keys():
            if l != 0:
                wt[word] = wt[word]/l
            else:
                wt[word] = 0.0

'''
	The normalized tf-idf of the queries and documents are multiplied. Higher score implies that the document is more relevant to the query
'''				
        score = [0]*n
        for word in wt:
            if word in tf.keys():
                for doc in tf[word]:
                    score[doc] = score[doc] + wt[word]*tf[word][doc]
 
'''
	The top 10 document id's and scores are returned
''' 
        top_id = heapq.nlargest(10, range(len(score)), score.__getitem__)
        top_score = heapq.nlargest(10, score);
        corpus = pd.read_excel("input.xlsx")
        documents = [];
        for i in range(10):
            j = top_id[i]
            document = corpus.iloc[j,0]
            documents.append(document)
    return render_template("result_ir.html",top_id=top_id,top_score=top_score,documents=documents)

if __name__ == '__main__':
   app.run(debug = True)



