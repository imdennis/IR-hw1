import numpy as np
import pandas as pd
import operator

querys = []
with open('query_list.txt') as f:
    for line in f:
        querys.append(line.strip())

# print(querys)

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
        # y = pd.value_counts(doc_array)[x][0]
        # print(x)
    doc_series.append(x)

# print(doc_series)

with open('submission.txt', 'w') as t:
    t.writelines('Query,RetreievedDocuments')

# compute tf for each word in a doc
for query in querys:

    query_array = []
    with open('Query/'+query) as f:
        for line in f:
            words = line.split(' ')
            for word in words:
                if word != '-1\n':
                    query_array.append(word)
                    np.unique(query_array)

    tf_idf = []
    for word in query_array:

        idf = 0
        tf_array = []
        for doc in docs:
            i = docs.index(doc)
            series = doc_series[i]
            if word in series.index:
                idf += 1
                tf = series.get_value(word)
                tf_array.append(tf)
            else:
                tf_array.append(0)

        new_tf_idf = [tf/(idf+1) for tf in tf_array]
        if tf_idf == []:
            tf_idf = new_tf_idf
        else:
            for x in range(len(tf_idf)):
                tf_idf[x] += new_tf_idf[x]

    # print(len(tf_idf))
    result = {}
    for x in range(len(tf_idf)):
        result[docs[x]] = tf_idf[x]

    result2 = sorted(result.items(), key=lambda kv: kv[1], reverse=True)


    # for x in result2:
    #     print(x[0])
    # break

    with open('submission.txt', 'a') as t:
        t.write('%s,' % query)
        for x in result2:
            t.write('%s ' % x[0])
        t.writelines(' ')


# compute idf for all docs
