from __future__ import division
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
import urllib
from bs4 import BeautifulSoup
import sys 
import unicodedata
import csv
import nltk.data
import ast
import numpy as np 
import operator
reload(sys)  
sys.setdefaultencoding('utf-8')
freqTerms = dict()
f=open('frequencyDistribution.csv','wb')
counter = 0	
print 'hello'
def get_sentences_from_url(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html,'html.parser')

	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	for unwanted_tags in soup(['script', 'style', 'table']):
		unwanted_tags.extract()

	text = soup.get_text()

	sentences = tokenizer.tokenize(text)

	return sentences

def get_frequency_distribution():	
	url_list = ['https://www.sec.gov/Archives/edgar/data/320193/000119312511104388/d10q.htm','https://www.sec.gov/Archives/edgar/data/320193/000119312513416534/d590790d10k.htm','http://investor.apple.com/secfiling.cfm?filingid=1193125-14-275598&cik=320193','https://www.sec.gov/Archives/edgar/data/1288776/000128877614000040/goog10-qq12014.htm','https://www.sec.gov/Archives/edgar/data/1288776/000165204416000012/goog10-k2015.htm','https://www.sec.gov/Archives/edgar/data/1288776/000128877615000039/a20150810form8-k.htm','https://www.sec.gov/Archives/edgar/data/1318605/000119312513212354/d511008d10q.htm','https://www.sec.gov/Archives/edgar/data/1318605/000156459015001031/tsla-10k_20141231.htm','https://www.sec.gov/Archives/edgar/data/789019/000119312515144151/d860721d10q.htm','https://www.sec.gov/Archives/edgar/data/789019/000119312515272806/d918813d10k.htm','https://www.sec.gov/Archives/edgar/data/789019/000119312514271285/d758424d8k.htm']
	for url in url_list:
		sentence = ''.join(get_sentences_from_url(url)).lower()
		stop = set(stopwords.words('english'))
		res = list()
		resstem = list()
		#sentence.lower()
		tokenizer = RegexpTokenizer(r'\w+')
		wnotpun = tokenizer.tokenize(sentence)

		for i in wnotpun: 
			if (i not in stop) & (not i.isdigit()):
				res.append(i) 

		lmtzr = WordNetLemmatizer()
		for wrd in res:
			resstem.append(lmtzr.lemmatize(wrd))

		fdiston = FreqDist(resstem)
		final = fdiston.most_common(50)

		for one,two in final:
			if one in  freqTerms:
		  		freqTerms[one] = freqTerms[one] + two
			else:
		  		freqTerms[one] = two


def get_score_data():	
	f=open("scoresTraining3.csv","wb")
	#url_list = ['https://www.sec.gov/Archives/edgar/data/320193/000119312511104388/d10q.htm','https://www.sec.gov/Archives/edgar/data/1326801/000119312512325997/d371464d10q.htm','https://www.sec.gov/Archives/edgar/data/104169/000119312511335177/d233066d10q.htm','https://www.sec.gov/Archives/edgar/data/101830/000010183015000005/sprintcorp12-31x1410q.htm','https://www.sec.gov/Archives/edgar/data/63908/000006390813000028/mcd-3312013x10q.htm','https://www.sec.gov/Archives/edgar/data/27419/000002741915000012/tgt-20150131x10k.htm','https://www.sec.gov/Archives/edgar/data/37996/000003799615000064/f0930201510-q.htm']
	#url_list = ['https://www.sec.gov/Archives/edgar/data/320193/000119312511104388/d10q.htm','https://www.sec.gov/Archives/edgar/data/1288776/000128877614000040/goog10-qq12014.htm','https://www.sec.gov/Archives/edgar/data/1318605/000119312513212354/d511008d10q.htm','https://www.sec.gov/Archives/edgar/data/789019/000119312515144151/d860721d10q.htm']
	url_list = ['https://www.sec.gov/Archives/edgar/data/320193/000119312511104388/d10q.htm']
	#url_name = ['AAPL','GOOGL','TSLA','MSFT']
	count = 0	
	for url in url_list:
		company = "MSFT"		
		sentences = get_sentences_from_url(url)
		count = count + len(sentences)
		for sentence in sentences:
			stop = set(stopwords.words('english'))
			res = list()
			resstem = list()
			tokenizer = RegexpTokenizer(r'\w+')	
			wnotpun = tokenizer.tokenize(sentence)
			for i in wnotpun:
				if (i.decode('utf-8', 'ignore').lower() not in stop) & (not i.isdigit()):
					res.append(i.decode('utf-8', 'ignore').lower())
		    
			lmtzr = WordNetLemmatizer()
			for wrd in res:
				resstem.append(lmtzr.lemmatize(wrd))		    
		        lengt = len(resstem)
		        score = 0
		        sentencescore = 0
		        for wrding in resstem:
		        	if wrding in freqTerms:
		        		score = score + 1
		    	if lengt:
		    		sentencescore = score/lengt		   				   		
		   		if sentencescore >= 0.5:		   			
		   			 	print sentence, sentencescore
		   			 	

	print count
	f.close()

if __name__ == "__main__":
	
	get_frequency_distribution()
	np.save('my_file.npy', freqTerms)
	freqTerms = np.load('my_file.npy').item()
	#print read_dictionary
	#print type(read_dictionary)
	get_score_data()
	#print counter