# Processing
import re

import pandas as p
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


def do_preprocessing():
    # read dataset
    file_content = p.read_csv("../message.csv", names=["type", "message"], delimiter="|")
    preProcessedData = []
    stammer = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    for data in file_content["message"]:
        filtered_data = re.sub("[^a-bA-z]", " ", data).strip().lower()
        # filtered_data = word_tokenize(filtered_data)
        filtered_data = [stammer.lemmatize(word) for word in filtered_data.split() if word not in stop_words]
        filtered_data = " ".join(filtered_data)
        preProcessedData.append(filtered_data)
    return preProcessedData


def do_processing(data):
    print(data)
    # Vanilla encoding everything in single word
    # cv = CountVectorizer(max_features=100, binary=True)

    # Ngram is used to make combination of words here (unigram, trigram)
    # max features represent the top max word counts you want to consider
    cv = CountVectorizer(max_features=100, binary=True, ngram_range=(1, 2))
    processed = cv.fit_transform(data).toarray()
    print(processed)
    print(f" with ngram {cv.vocabulary_}")
    # print(f" without ngram {cv_1.vocabulary_}")
    # print(cv_1.vocabulary_)
    print(processed.shape)

do_processing(do_preprocessing())
