from nltk.stem import RegexpStemmer

# paragraph = '''
# '''

words = ["eat", "eaten", "go", "going", "do", "doing", "done", "program", "programming", "history"]
stemming = RegexpStemmer('ing$|s$|e$|able$', min=4)
for word in words:
    print(f"word {word} -> {stemming.stem(word)}")
