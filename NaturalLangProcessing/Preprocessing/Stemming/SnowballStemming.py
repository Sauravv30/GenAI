from nltk.stem import SnowballStemmer

words = ["eat", "eaten", "go", "going", "goes", "do", "doing", "done", "program", "programming", "history",
         "historically",
         "previously", "fairly"]

stemmer = SnowballStemmer(language='english')
for word in words:
    print(f"{word} -> {stemmer.stem(word)}")
