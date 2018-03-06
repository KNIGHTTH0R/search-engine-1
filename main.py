import os
import re
from PorterStemmer import PorterStemmer
from bs4 import BeautifulSoup

dict = {}


def go():
    dataset = 'Dataset'

    for file in os.listdir(dataset):
        if file.endswith(".sgm"):

            filename = os.path.join(dataset, file)
            with open(filename, 'r') as f:
                data = f.read()

            soup = BeautifulSoup(data, 'html.parser')

            for news_article in soup.find_all('reuters'):
                doc_id = int(news_article.get('newid'))
                news_text = ''

                if news_article.title:
                    news_text += news_article.title.string.lower() + '\n'
                if news_article.body:
                    news_text += news_article.body.string.lower()

                tokenize(news_text, doc_id)

    create_index_files()


def tokenize(news_text, doc_id):
    f = open('stopwords.txt', 'r')
    stopwords = f.read()
    f.close()
    stopwords = {stopwords}  # set for faster run

    # [\w] means any alphanumeric characters [a-zA-Z0-9_]
    word_list = re.sub("[^\w]", " ", news_text).split()

    # create a dict of dicts
    # { 'happy':{ 1:[3,5,..], 2:[4,9],..}, 'sad':{ 2:[], 3:[],..},..}
    for position, word in enumerate(word_list):
        if word not in stopwords:
            token = stem(word)
            if token in dict:
                if doc_id in dict[token]:
                    temp = dict[token][doc_id]
                    temp.append(position)
                    dict[token][doc_id] = temp
                else:
                    dict[token][doc_id] = [position]
            else:
                dict[token] = {}
                dict[token][doc_id] = [position]


def stem(word):
    p = PorterStemmer()
    return p.stem(word, 0, len(word) - 1).encode('utf8')



# {'towel': 42} --> { '42':{ 1:[3,5], 4:[5,9],..}, ... }
def create_index_files():



    with open('inverted_index.txt', 'w') as f:
        for i, key in enumerate(sorted(dict)):
            f.write(str( (i,dict[key]) )+'\n')
            dict[key] = i

    with open('dictionary.txt', 'w') as f:
        f.write( str(dict) )




def read_line(line_number):
    with open('inverted_index.txt', 'r') as f:
        for i, line in enumerate(f):
            if i == line_number :
                print type(line), line
                t = eval(line)
                print type(list(t)[1])

if __name__ == "__main__":
    go()