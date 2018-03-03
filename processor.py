from PorterStemmer import PorterStemmer



class SearchEngine(object):
	
	def __init__(self):
		self.dictionary = None
		self.postings_list = None
		self.get_ready()

	def get_ready(self):
		f= open('dictionary.txt','r')
		data = f.read()
		self.dictionary = eval(data)
		f.close()
		
		f= open('postings_list.txt','r')
		data = f.read()
		self.postings_list = eval(data)
		f.close()


	def preprocess(self, query):
		p = PorterStemmer()
		return p.stem(query,0,len(query)-1).encode('utf8').lower()


	def search(self,query):
		answer = None
		query = self.preprocess(query)
		if self.dictionary[query]:
			hash_key = self.dictionary[query]
			answer = self.postings_list[hash_key]

		return answer 
		


if __name__ == "__main__":
	whitefang = SearchEngine()
	while True:
		query = raw_input("Your search query:\n")
		if query == 'break':
			break
		print whitefang.search(query)
		continue
		