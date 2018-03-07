from PorterStemmer import PorterStemmer
import re

class SearchEngine(object):

    def __init__(self):
        self.dictionary = self.read_dictionary('dictionary.txt')
        self.stopwords = self.get_stopwords('stopwords.txt')

    def get_stopwords(self,filename):
        with open(filename, 'r') as f:
            stopwords = f.read().split('\n')
        return set(stopwords)


    def read_dictionary(self,filename):
        with open(filename, 'r') as f:
            data = f.read()
        return eval(data)


    def read_line(self,line_number):
        with open('inverted_index.txt', 'r') as f:
            for i, line in enumerate(f):
                if i == line_number :
                    return eval(line)


    def positional_intersect(self, pp1, pp2, k):

        answer = []

        i = j = 0
        l = []

        while i != len(pp1):
            while j != len(pp2):
                if abs(pp2[j]-pp1[i]) <= k:
                    l.append(pp2[j])
                elif pp2[j] > pp1[i]:
                    break

                j += 1

            for ps in l:
                answer.append( [pp1[i], ps] )


            i += 1

        print 'answer', answer
        return answer


    def handle_positional_query(self, index, intersections,distances,search_terms):
        answer = {}  # {doc_id1:[ [], [],..], doc_id2: }

        print 'intersections', intersections
        print 'dists',distances
        print 'terms', search_terms

        for doc_id in intersections:
            for i, token in enumerate(search_terms):
                if i + 1 < len(search_terms):

                    next_token = search_terms[i + 1]

                    pp1 = index[token][doc_id]
                    pp2 = index[next_token][doc_id]
                    k = distances[i]

                    if doc_id in answer:
                        pp1 = []
                        for list in answer[doc_id]:
                            pp1.append(list[-1])
                        intersect = self.positional_intersect(pp1, pp2, k)

                        if len(intersect) == 0:
                            break

                        # merge positional intersections
                        for group in intersect:
                            for i, list in enumerate(answer[doc_id]):
                                # for w1 /k1 w2 /k2 w3
                                # [p1,p2] is in answers but no [p1,p2,p3], so remove [p1,p2]
                                if list[-1] != group[0]:
                                    answer[doc_id].pop(i)
                                else:
                                    answer[doc_id][i].append(group[1])


                    else:
                        answer[doc_id] = self.positional_intersect(pp1, pp2, k)
        return answer


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
        print 'index', index
        return index


    def preprocess(self, query):
        p = PorterStemmer()
        result = []

        # remove any non-alphanumeric characters [a-zA-Z0-9_]
        query = re.sub("[^\w]", " ", query)
        query = query.lower().split(' ')
        for word in query:
            if word not in self.stopwords:
                result.append(p.stem(word, 0, len(word) - 1))
        return result

    def search(self,query):

        if query is None:
            return answer

        # lowercase, stem
        query = self.preprocess(query)

        query_type = int(query[0])

        search_terms = query[1:]

        # { token1 : {doc_id : [postings], ..}, token2 : ... }
        index = self.get_index(search_terms)

        postings_lists = []
        for token in index:
             # doc_ids will be a list
             doc_ids = index[token].keys()
             postings_lists.append(doc_ids)
        intersections = self.intersect_lists(postings_lists)


        if query_type == 1:
            answer = intersections

        elif query_type == 2:
            distances = [1] * (len(search_terms)-1)
            answer = self.handle_positional_query(index, intersections,distances,search_terms)


        elif query_type == 3:
            digit_strings = re.findall(r"\d+", ' '.join(search_terms) )
            distances = map(int, digit_strings)

            # remove /k AND etc..
            for term in search_terms:
                if term not in index:
                    search_terms.remove(term)

            answer = self.handle_positional_query(index, intersections,distances,search_terms)
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

