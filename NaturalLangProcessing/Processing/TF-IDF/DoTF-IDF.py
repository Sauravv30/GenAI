from nltk.stem import WordNetLemmatizer
import pandas as p
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer


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


def do_tf_idf_vectorization(data):
    tf_idf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    output = tf_idf.fit_transform(data).toarray()
    print(output.shape)
    print(output)


do_tf_idf_vectorization(do_preprocessing())
