#CS F469
##Information Retrieval Assignment – 1
##Domain Specific Search Engine

##Contributors:
Mahicharan Galla		2016A7PS0054H
Dhulipudi Avinash		2016A7PS0113H
Bharath KNS			    2016A7PS0103H
M Tejo Vardhan			2016AAPS0150H

###Language:	Python 3.5

##Working:

1.	The entire corpus is preprocessed by the preprocess.py file which saves 2 dictionaries in the same directory.
2.	Two html files are present in the folder ‘’templates” which is present in the directory. These html files are required for the GUI which is run on localhost port. The GUI was built using Flask.
3.	The directory also contains tf_dump and idf_dump which are 2 dictionaries which are produced by preprocess.py. These two files are read by main.py
4.	The search engine can be started by running the main.py.
5.	The results will be random if the searched words are not present in any document in the corpus.
6.	Each search can be finished within 4 seconds.
7.	After each search, the top 10 documents are printed along with the relevance score.

##Installation:

To run the following code, Anaconda, Flask and nltk have to be readily installed.
•	Anaconda can be installed by following the following link: https://docs.anaconda.com/anaconda/install/
•	Flask can be installed by following the documentation in the below link. http://flask.pocoo.org/docs/0.12/installation/
•	ntlk can be installed using ‘ntlk.download()’ in a python shell. For further queries refer: http://www.nltk.org/install.html
