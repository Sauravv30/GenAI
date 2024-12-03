# Word Embeddings

- In the Natural Language Processing, word embeddings is a term used for the representation of words for text analysis,
  typically in the form of a real-valued vector that encodes the meaning od the word such that the words that are closed
  in the vector space are expected to be similar in meaning.

**Types**
**Count or Frequency**

- One Shot Encoding
- Bag of Words
- Tf-IDF

**Deep Learning Trained Model**

- Word2Vec (Helps to overcome previous problems and efficiently convert the words to vectors)
    - CBOW (Continuous bag of words)
    - Skip-gram

# Word2Vec

- Is a technique for NLP published in 2013 by Google. The word2vec uses neural network model to learn word associations
  from the
  large corpus of text. Once trained such a model can detect synonymous words or suggest additional words for a partial
  sentence. As the name
  implies, word2vec represents each distinct words with a particular list of numbers called a vector.

**Feature Representation**

    (Dimensions)      Boy         King        Queen     Girl     
      Gender          -1          0.02         -0.03     1            
      Royal           0.03        0.98         -0.95    0.05
      Food            0.02        0.04          0.06    0.08

**Notes:** With these values the cosine works for similarities.

We have two types of Word2Vec models:

- Pretrained Model
- Train from scratch

# CBOW (Continous Bag of Words)

- This is bit difficult to understand as ANN, neural network is involved in it.
- We have a window size defined and we move to next words of sentence with same window size everytime.
- This window is there help creation relationships.
- Then we have a loss function applied on it, if loss is more the less accurate the result is. We have backward propagation to fix it.

# Skipgram (Similar to CBOW but in opposite direction)

**Usage**

- CBOW : Used to small dataset
- Skipgram : Used in huge datasets

**Improve the Output**

- Increase the training data
- Increase window size, leads to increase in vector dimension.

### Advantages of Word2Vec
1. Sparce Matrix -> Dense Matrix
2. Semantic information is captured (Similar words)
3. Fixed set of dimensions (No vocabulary problems)

# Average Word2Vec