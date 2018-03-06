
## Intro
this repo implements a document retrieval system for simple boolean queries
using the positional inverted indexing scheme.

Data set is Reuters-21578 which contains 21578 Reuters news stories.

## Source Code
main.py traverses the files in 'Dataset' directory and creates 2 files:
+ dictionary.txt
+ inverted_index.txt

processor.py searches for 3 types of queries.
+ 1 oil AND price
+ 2 oil price
+ 3 oil /3 price

first digit indicates query type
queries can include any number of words.