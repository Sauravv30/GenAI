from nltk.stem import WordNetLemmatizer

'''
POS - Noun(n)
Verb (v)
adjective (a)
adverb (r)
'''
lemmatize = WordNetLemmatizer()
words = ["eat", "eaten", "go", "going", "do", "doing", "done", "program", "programming", "history", "previously",
         "fairly"]

for word in words:
    print(f"{word} -> {lemmatize.lemmatize(word, pos='r')}")
    print(f"{word} -> {lemmatize.lemmatize(word, pos='v')}")

#
