import os
import re
from PorterStemmer import PorterStemmer
from bs4 import BeautifulSoup


class Preprocessor(object):

    def __init__(self):
        self.dict = {}
        self.stopwords = self.get_stopwords('stopwords.txt')


    def get_stopwords(self,filename):
        with open(filename, 'r') as f:
            stopwords = f.read().split('\n')
        return set(stopwords)


    # {'towel': 42} --> { '42':{ 1:[3,5], 4:[5,9],..}, ... }
    def create_index_files(self):
        with open('inverted_index.txt', 'w') as f:
            # dictionary value of a token will be the line number in the index
            # we will just read the necessary line and have super fast search
            for i, key in enumerate( sorted(self.dict) ):
                f.write( str( self.dict[key] )+'\n' )
                self.dict[key] = i

        with open('dictionary.txt', 'w') as f:
            f.write( str(self.dict) )


    def update_dict(self, token, doc_id, position):
        if token in self.dict:
            if doc_id in self.dict[token]:
                temp = self.dict[token][doc_id]
                temp.append(position)
                self.dict[token][doc_id] = temp
            else:
                self.dict[token][doc_id] = [position]
        else:
            self.dict[token] = {}
            self.dict[token][doc_id] = [position]


    def stem(self,word):
        p = PorterStemmer()
        return p.stem(word, 0, len(word) - 1)


    def tokenize(self, news_text, doc_id):
        news_text = news_text.lower().encode('utf8')
        # remove any non-alphanumeric characters [a-zA-Z0-9_]
        word_list = re.sub("[^\w]", " ", news_text).split()

        # remove stopwords, stem tokens, add tokens to dictionary
        for position, word in enumerate(word_list):
            token = self.stem(word)
            if token not in self.stopwords:
                self.update_dict(token, doc_id, position)


    def read_file(self,filename):
        with open(filename, 'r') as f:
            data = f.read()

        soup = BeautifulSoup(data, 'html.parser')

        for news_article in soup.find_all('reuters'):
            doc_id = int(news_article.get('newid'))
            news_text = ''

            if news_article.title:
                news_text += news_article.title.string + '\n'
            if news_article.body:
                news_text += news_article.body.string

            self.tokenize(news_text, doc_id)


    def process(self, dataset):
        for file in os.listdir(dataset):
            if file.endswith(".sgm"):
                filename = os.path.join(dataset, file)
                self.read_file(filename)
        self.create_index_files()


if __name__ == "__main__":
    sonic = Preprocessor()
    sonic.process('Dataset')