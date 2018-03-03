import os 
from bs4 import BeautifulSoup 
from PorterStemmer import PorterStemmer
import re


class Preprocessor(object):
	dict = {}

	def go(self):

		dataset = 'Dataset'	

		for file in os.listdir(dataset):	
			if file.endswith(".sgm"):
				
				with open(os.path.join(dataset, file), 'r') as f:
					data = f.read()

				soup = BeautifulSoup(data, 'html.parser')

				for news_article in soup.find_all('reuters'):

					news_id = int(news_article.get('newid'))
					news_text = ''

					if news_article.title:
						news_text += news_article.title.string.lower()+'\n'				
					if news_article.body:
						news_text += news_article.body.string.lower()

					self.tokenize(news_text)

		self.create_index_files(dict)
					

					
				
	def tokenize(self,news_text):
		f = open('stopwords.txt', 'r')
		stopwords = f.read()
		f.close()
		stopwords = {stopwords} # set for faster run 
				
		# [\w] means any alphanumeric characters [a-zA-Z0-9_]
		word_list = re.sub("[^\w]", " ",  news_text).split()

		for word in word_list:
			if word not in stopwords:
				token = self.stem(word)
				if token in dict:
					dict[token].append(news_id)
				else:
					dict[token] = [news_id]



	def create_index_files(self,dict):

		postings_list = {}

		for i, key in enumerate(sorted(dict.keys())):
			postings_list[i] = sorted(dict[key])
			dict[key] = i
		
		with open('x.txt', 'w') as f:
			f.write(str(dict))
		with open('y.txt', 'w') as f:
			f.write(str(postings_list))


				
	def stem(self,word):
		p = PorterStemmer()
		return p.stem(word,0,len(word)-1).encode('utf8')

if __name__ == "__main__":
	matrix = Preprocessor()
	matrix.go()