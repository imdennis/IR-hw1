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


# tf-idf
def tf_idf(index=0, word='3310', series=doc_series):

    # tf
    tf = series[index].get_value(word)
    tf = 1 + math.log2(tf)

    # idf
    idf = 0
    for s in series:
        if word in s.index:
            idf += 1

    if series == doc_series:
        idf = math.log10(2265/(idf+0.5))
    else:
        idf = math.log10(16/(idf+0.5))

    return tf*idf


# print submission title
with open('submission.txt', 'w') as t:
    t.write('Query,RetrievedDocuments\n')


for query_i in range(16):

    sim_array = {}
    for doc_j in range(2265):

        dot = 0
        for word in query_series[query_i]:
            dot += tf_idf(query_i, word, query_series) * \
                tf_idf(doc_j, word, doc_series)

        # dist of query
        dist_query = 0
        for word in query_series[query_i]:
            dist_query += math.pow(tf_idf(query_i, word, query_series), 2)

        # dist of doc
        dist_doc = 0
        for word in doc_series[doc_j]:
            dist_doc += math.pow(tf_idf(doc_j, word, doc_series), 2)

        sim = dot / (dist_query * dist_doc)
        sim_array[doc_array[doc_j]] = sim

    # sort dict
    result_turple = sorted(
        sim_array.items(), key=lambda kv: kv[1], reverse=True)

    # print this query result:
    with open('submission.txt', 'a') as t:
        t.write('%s,' % query_array[query_i])

        for rt in result_turple:
            t.write('%s ' % rt[0])
        t.write('\n')
