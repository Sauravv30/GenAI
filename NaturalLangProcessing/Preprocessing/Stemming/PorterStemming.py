from nltk.stem import PorterStemmer

# paragraph = '''
# '''

words = ["eat", "eaten", "go", "going", "do", "doing", "done", "program", "programming", "history", "previously",
         "fairly"]
stemming = PorterStemmer()
for word in words:
    print(f"word {word} ->  and stemming {stemming.stem(word)}")
