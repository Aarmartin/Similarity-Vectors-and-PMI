# Similarity-Vectors-and-PMI
Python Program that creates a co-occurence matrix of words with a given corpus, and computes Pointwise Mutual Information between two words.

The goal of this program is to calculate the Pointwise Mutual Information value between two words. It first creates a co-occurrence matrix based on a training corpus of news articles that contains the counts of each word pair within a span of words. Once this inforamtion is found, the information is run through equations to calculate each word pair's cosign value and PMI.

This method takes in a window size to evaluate the counts of words pairs that occur within this window. A size of two will only increment the count for direct word pairs, whereas a window size of 5 will add a count to each pair of words within 5 words in its context.

# Running the Program
This program only has one file to run, in the format
```
python3 similar-pmi.py <WINDOW> ./PA4-News-2011 ./word-pairs.txt
```
Where \<WINDOW\> is the window size of words to be used
