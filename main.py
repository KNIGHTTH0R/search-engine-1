from bs4 import BeautifulSoup 
import os 
from PorterStemmer import PorterStemmer
import re
import json 



def go():

	f = open('stopwords.txt', 'r')
	stopwords = f.read()
	f.close()
	stopwords = {stopwords}
	print type(stopwords)

	dataset = 'Dataset'
	tokens_dict = {}
	inverted_index = {}

	for file in os.listdir(dataset):
		
		tokens = []

		if file.endswith(".sgm"):
			
			f = open(os.path.join(dataset, file), 'r')
			data = f.read()
			f.close()
			soup = BeautifulSoup(data, 'html.parser')


			for news_article in soup.find_all('reuters'):
				
				news_id = news_article.get('newid')
				news_text = ''

				if news_article.title:
					news_text += news_article.title.string.lower()+'\n'				
				if news_article.body:
					news_text += news_article.body.string.lower()
				
				# [\w] means any alphanumeric characters [a-zA-Z0-9_]
				word_list = re.sub("[^\w]", " ",  news_text).split()
				
				p = PorterStemmer()
				for word in word_list:
					if word not in stopwords:
						token = p.stem(word,0,len(word)-1)
						tokens.append(token.encode('utf8'))								


				f = open(os.path.join('test.txt'), 'a+')
				#f.write(json.dumps(tokens_dict)+'\n')
				f.close()



if __name__ == "__main__":
	go()