import numpy as np
import pandas as pd
import operator
import math

querys = []
with open('query_list.txt') as f:
    for line in f:
        querys.append(line.strip())


docs = []
with open('doc_list.txt') as f:
    for line in f:
        docs.append(line.strip())

# print(docs)


# read all docs
doc_series = []
for doc in docs:
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
    doc_series.append(x)




# read all querys
query_series = []
for query in querys:

    query_array = []
    with open('Query/'+query) as f:
        for line in f:
            words = line.split(' ')
            for word in words:
                if word != '-1\n':
                    query_array.append(word)

    x = pd.value_counts(query_array)
    query_series.append(x)


history_tf_idf = {}
history_idf ={}
# tf-idf
def tf_idf(index, word, series):
    series_no = 2 #query
    if series == doc_series:
        series_no = 1 #document
    
    if '%d%s%d' % (index, word, series_no) in history_tf_idf:
        return history_tf_idf['%d%s%d' % (index, word, series_no)]


    #tf
    tf = 1
    if word in series[index].index:
        tf = series[index].get_value(word)
        tf = 1 + math.log2(tf)
    else:
        tf = 1
    # print('tf: %d,series : %d ,index:%d, word:%s'%(tf,series_no,index,word))


    # idf
    idf = 0
    if word not in history_idf:
        for s in doc_series:
            if word in s.index:
                idf += 1
        history_idf[word] =idf
    else:
        idf = history_idf[word]

    # print('idf: %d,series : %d ,index:%d, word:%s'%(idf,series_no,index,word))

    idf = math.log10(2265/(idf+1))

    # result = tf*idf
    result = tf

    history_tf_idf['%d%s%d' % (index, word, series_no)] = result
    return result


# print submission title
with open('submission.txt', 'w') as t:
    t.write('Query,RetrievedDocuments\n')


for query_i in range(16):
    print("in query %d" % query_i)

    # dist of query
    print('compute dist query')
    dist_query = 0
    for word in query_series[query_i].index:
        dist_query += math.pow(tf_idf(query_i, word, query_series), 2)
    # print(dist_query)

    sim_array = {}
    for doc_j in range(2265):
        print("in doc %d" % doc_j)

        dot = 0
        print('compute dot')
        for word in query_series[query_i].index:
            dot +=  tf_idf(query_i, word, query_series) * tf_idf(doc_j, word, doc_series)
        # print(dot)
        
        # dist of doc
        print('compute dist doc')
        dist_doc = 0
        for word in doc_series[doc_j].index:
            dist_doc += math.pow(tf_idf(doc_j, word, doc_series), 2)

        sim = dot / ( math.sqrt(dist_query) * math.sqrt(dist_doc) )
        sim_array[docs[doc_j]] = sim


    # sort dict
    print('compute sorting')
    result_turple = sorted(
        sim_array.items(), key=lambda kv: kv[1], reverse=True)

    # print this query result:
    with open('submission.txt', 'a') as t:
        t.write('%s,' % querys[query_i])

        for rt in result_turple:
            t.write('%s ' % rt[0])
        t.write('\n')

    # print(query_series[0])
    # break