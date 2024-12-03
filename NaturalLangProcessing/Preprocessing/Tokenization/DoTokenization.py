# Library used Natural Language Toolkit

from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize, TreebankWordTokenizer

corpus = '''Rudra is Shiva'a avatar. Tridev belongs to Shiva. Goddess Uma has three avatar Sati,Laxmi,Saraswati.
'''
# print(corpus)
tokenized = sent_tokenize(corpus, language="English")
print("Corpus to sentence -> ", tokenized)

words = []
wordsWithPunctuations = []
for sentence in tokenized:
    wordsWithPunctuations.append(wordpunct_tokenize(sentence))
    words.append(word_tokenize(sentence))

print("Sentence to words -> ", words)
print("Sentence to word punctuation -> ", wordsWithPunctuations)
tokenizer = TreebankWordTokenizer()
print(tokenizer.tokenize(corpus))

# wordpunct_tokenize(corpus)
