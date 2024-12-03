import gensim.downloader as api

w2v = api.load("word2vec-google-news-300")
vec_king = w2v["king"]

print(vec_king)

print(w2v['cricket'])
print(w2v.shape)  # 300

print(w2v.most_similar('happy'))

vec = w2v['king'] - w2v['man'] + w2v['woman']
print(w2v.most_similar([vec])) #queen
