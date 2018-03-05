from PorterStemmer import PorterStemmer
import re

class SearchEngine(object):

    def __init__(self):
        self.dictionary = None
        self.postings_list = None
        self.get_ready()

    def get_ready(self):
        f = open('dictionary.txt', 'r')
        data = f.read()
        self.dictionary = eval(data)
        f.close()

        f = open('postings_list.txt', 'r')
        data = f.read()
        self.index = eval(data)
        f.close()

    def positional_intersect(self,index,intersections,distances ):






    def intersect_lists(self,list_of_lists):
        # map applies set() function to every sublist
        setlist = map(set, list_of_lists)

        # *args means arbitrary number of arguments
        answer = set.intersection(*setlist)

        return list(answer)


    # returns a list of postings_lists of query terms
    def get_index(self,terms):
        dict = {}
        for term in terms:
            if term in self.dictionary:
                token_id = self.dictionary[term]
                dict[token_id] = self.index[token_id]
        return dict


    def preprocess(self, query):
        p = PorterStemmer()
        return p.stem(query, 0, len(query) - 1).lower().split(' ')


    def search(self,query):
        answer = []
        postings_lists = []

        # lowercase, stem and split query
        query = self.preprocess(query)

        search_terms = query[1:]

        index = self.get_index(search_terms)

        for token_id in index:
            document_ids = index[token_id].keys()
            postings_lists.append(document_ids)

        intersections = self.intersect_lists(postings_lists)

        print query
        print search_terms
        print index
        print postings_lists

        # {'towel': 42, '':..} --> { '42':{ 1:[3,5], .. }, ... }

        query_type = int(query[0])
        if query_type == 1:
            answer = intersections

        elif query_type == 2:
            query = ' '.join(query)
            digit_strings = re.findall(r"\d+", ' '.join(search_terms) )
            distances = map(int, digit_strings)


            for doc_id in intersections:


            for i, distance in enumerate(distances):

            return self.positional_intersect(index,intersections,distances)


        elif query_type == 3:
            pass

        else:
            answer = 'incorrect input'

        return answer


if __name__ == "__main__":
    whitefang = SearchEngine()
    while True:
        query = raw_input("Your query:\n")
        print 'answer:', whitefang.search(query)
        continue
