import numpy as np 
import pandas as pd

querys = []
with open('query_list.txt') as f:
  for line in f:
    querys.append(line.strip())

#print(querys)

docs = []
with open('doc_list.txt') as f:
  for line in f:
    docs.append(line.strip())

#print(docs)


#make IDF table 
idf = []


doc_series = []
for doc in docs :
  doc_array = []
  with open('Document/'+doc) as f:
    next(f) 
    next(f)
    next(f)
    for line in f:
      words = line.split(' ')
      for word in words:
          if word != '-1\n':
            doc_array.append(word)
    
    x = pd.value_counts(doc_array)
    # y = pd.value_counts(doc_array)[x][0]
    # print(x) 
  doc_series.append(x)
  
# print(doc_series)      

#compute tf for each word in a doc
# for query in querys:
#   query_array = []
#   with open('Query/'+query) as f:
#     for line in f:
#       words = line.split(' ')
#       for word in words:
#         if word != '-1\n':
#           query_array.append(word)
#           np.unique(query_array)
#   for word in query_array:
#      for doc in docs:
#        if doc_series[docs.index(doc)] != -1:



#compute idf for all docs
