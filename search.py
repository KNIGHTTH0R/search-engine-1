from PorterStemmer import PorterStemmer
import re

class SearchEngine(object):

    def __init__(self):
        self.dictionary = self.read_dictionary('dict.txt')


    def read_dictionary(self,filename):
        with open(filename, 'r') as f:
            data = f.read()
        return eval(data)


    def read_line(self,line_number):
        with open('inverted_index.txt', 'r') as f:
            for i, line in enumerate(f):
                if i == line_number :
                    return list(eval(line))[1]

    def positional_intersect(self,p1,p2,k):
        answer = []

        while p1 is not None and p2 is not None:
            pass



    def intersect_lists(self,list_of_lists):
        # map applies set() function to every sublist
        setlist = map(set, list_of_lists)

        # *args means arbitrary number of arguments
        answer = set.intersection(*setlist)

        return list(answer)


    # returns the index entries for query terms as a dict
    def get_index(self,terms):
        index = {}
        for term in terms:
            if term in self.dictionary:
                token_id = self.dictionary[term]
                index[term] = self.read_line(token_id)
        return index


    def preprocess(self, query):
        p = PorterStemmer()
        return p.stem(query, 0, len(query) - 1).lower().split(' ')


    def search(self,query):
        answer = []

        if query is not None:
            # lowercase, stem and split query
            query = self.preprocess(query)

        query_type = int(query[0])
        search_terms = query[1:]

        # { token1 : {doc_id : [postings], ..}, token2 : ... }
        inverted_index = self.get_index(search_terms)
        print inverted_index
        postings_lists = []
        for token_id in inverted_index:
             # doc_ids will be a list
             doc_ids = inverted_index[token_id].keys()
             postings_lists.append(doc_ids)

        intersections = self.intersect_lists(postings_lists)

        if query_type == 1:
            answer = intersections

        elif query_type == 2:
            digit_strings = re.findall(r"\d+", ' '.join(search_terms) )
            distances = map(int, digit_strings)

            for doc_id in intersections:
                positional_index = []

                for token in inverted_index:
                    positional_index[doc_id] = inverted_index[token_id][doc_id]

                    self.positional_intersect(positional_index, distances, doc_id)



        elif query_type == 3:
            pass

        else:
            answer = 'incorrect input'

        return answer


def go():
    whitefang = SearchEngine()
    while True:
        query = raw_input("Your query:\n")
        print whitefang.search(query)
        continue

if __name__ == "__main__":
    go()

