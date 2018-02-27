from bs4 import BeautifulSoup 
import os 
from PorterStemmer import PorterStemmer


def readFiles():
	reuters21578 = 'reuters21578'
	

	for file in os.listdir(reuters21578):
		if file.endswith(".sgm"):
  	  		f = open(os.path.join(reuters21578, file), 'r')
  	  		data = f.read()
  	  		f.close()
  	  		soup = BeautifulSoup(data, 'html.parser')
  	  		print file
			for news_article in soup.find_all('reuters'):
				print news_article
				#print news_article.get('title')
				#print news_article.get('body')

			'''
			f = open(os.path.join('clean', file), 'a+')
			f.write(soup.title.string + '\n')
			f.write(soup.body.string)
			f.close()
			'''

			f.close()


def test():
	f = open(os.path.join('reuters21578', 'reut2-000.sgm'), 'r')
	data = f.read()
	f.close()
	soup = BeautifulSoup(data, 'html.parser')


	for news_article in soup.find_all('reuters'):
		#print news_article.get('newid')
		if news_article.title:
			# print news_article.title.string
			continue
		if news_article.body:
			#
			continue

def do_stemming():
	p = PorterStemmer()
	print p.stem(word,0,len(word)-1)

def go():
	#readFiles()
	test()

if __name__ == "__main__":
	go()