# Stemming

Stemming is the process of reducing the words to its word stem that affixes to suffixes and prefixed or the roots of words known as lemma.
- **Classification Problem** means, the comment on the product is a positive review or negative review. 
   Eg. Eat, Eaten, Eating -> Eat is Stem

**Porter Stemmer**
- eat -> stemming to eat
- eaten -> stemming to eaten
- go -> stemming to go
- going -> stemming to go
- do -> stemming to do
- doing -> stemming to do
- done -> stemming to done
- program -> stemming to program
- programming -> stemming to program
- history -> stemming to histori   - **(Drawback - it is changing the meaning here)**

**Regex Stemmer**
- Using regular expression we can easily implement Regular Expression Stemmer algo.

**Snowball Stemmer**
- Better then porter stammer, still we have words which are not performing well. 
  **like:** 
  - history -> histori
  -  historically -> histor


