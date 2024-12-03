# TF-IDF (Term Frequence - Inverse Document Frequency)

Example

- S1 -> good boy
- S2 -> good girl
- S3 -> good boy girl

**Formula**
**Term Frequency(TF)** = No. of repetitive words in sentence / No. of words in sentence

             Good   BOY   GIRL
       S1 -> 1/2  - 1/2 - 0
       S2 -> 1/2  - 0 - 1/2 
       S3 -> 1/3  - 1/3 - 1/3

**IDF** = log e (Number of sentence / No. of sentence containing the word)
           
             Good                    BOY               GIRL
       Words -> log e (3 / 3) or 0  log e (3 / 2)    log e (3 / 2)


**TF-IDF** = **Term Frequency(TF)**  *  **IDF**
            
            Final TF-IDF 
            good         boy                    girl
    Sent1     0     1/2 * log e (3 / 2)          0
    Sent2     0           0                  1/2 * log e (3 / 2)
    Sent3     0     1/3 * log e (3 / 2)      1/3 * log e (3 / 2)

**Notes:** - If word is present frequent then it will get less importance. You can see for good everytime we have importance as zero. 

**Pros**
- Intuitive implementation
- Fixed size, Vocab size
- Word importance is captured

**Cons**
- Sparsity still exists
- OOV (Out of vocabulary) still there as this conversion works on the present data only.