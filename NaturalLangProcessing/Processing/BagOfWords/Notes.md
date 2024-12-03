# Processing

* Processing the way that how we are converting the input data or text too numerical representation so we can perform
  some calculations on that.

    - One hot encoded
    - Bag of words(BOW)
    - TF-IDF
    - Word2Vec (Allow us customization)
    - AvgWord2Vec

**One hot encoded**

Is one of the basic encoding technique with few advantages and many disadvantages
    
      S1 -> good boy, S2 -> good girl, S3 -> boy girl good
                     
      **Vocabulary  Frequency**
      good           3
      boy            2
      girl           2

      Representation
           good        boy     girl
      S1    1           1        0
      S2    1           0        1
      S3    1           1        1

**Advantages**

- Simple to implement with pandas.get_dummies() or scikit.one_hot_encoding

**Disadvantages**

- Spars matrix (multiple zeros and ones approach) overfitting
- No similarities with cosine
- Out of vocabulary (OOV) it only takes care for the word it has encoded, will not support for new words.
- Length size mismatch, it is not doable for machine learning.

**Bag of words(BOW)**

* Lowercase all the words
* Stopwords

It takes the vocabulary word or say most frequent used words and keep it's frequency

**Vocabulary Frequency**

- Good -> 2
- Bad -> 2

It does short encoding with the help vocabulary and for each sentence if word is present will increment it with one.
We have two types of encoding **Binary BOW** and **BOW**

**Advantages**
- Simple and Intuitive
- Fixed size input, for ML algorithms


**Disadvantages**
- Spars matrix or array, Overfitting
- Ordering of the word is changed, meaning of words with get impacted.
- OOV (Out of vocabulary) New test data like any new word will be ignored
- Semantic meaning is still not captured.

**N-Grams**
- N-Grams is used to make some words combination, as in previous encoding tecnhiques 'He is playing' and 'He is not playing' for these sentences only not is the difference and that's why for encoding these are nearly the same sentences.
where in actual these are opposite to each other.
- So n-grams are used to make some better combinations which help machine to find these are different.
- e.g 
  * "is not", "is"
  * "no playing", "playing"
