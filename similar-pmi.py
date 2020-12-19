# Aaron Martin
# 11/10
#
# Program that takes in a training corpus of different texts and a set of word pairs, and uses that training information to calculate the cosign and pmi values for each word pair
#
# Cosign	word 1	word 2		c(1)	c(2)	c(1,2)	pmi
# 0.90664	russia	germany		4156	4607	4		3.30312
#
# 1. Parse directory of all input text files word by word
# 	a. Add every unique word to a dictionary
#	b. Keep a running count of all total words
#	c. Keep a running count of amount of times each specific word has occured
#	d. Assign each new word an index value
# 2. Parse entire text line by line
# 	a. Parse each word in text
#		i. Add co-occurence of index of word and all words within a specified window in the form matrix[indexWord1][indexWord2] by incrementing a running sum of each unique occurence
# 3. Parse each word pair
#	a. Calculate cosign value of word pair
#		i.  Parse row of word 1 and word 2 in co-occurence matrix at the same time
#			a. Multiply co-occurence values of word 1 at column i and word 2 at column i
#			b. Add value to running sum for numerator
#			c. Square co-occurence value of word 1 at column i and add to running sum (sum1)
#			d. Square co-occurence value of word 2 at column i and add to running sum (sum2)
#		ii. Calculate denominator by finding the square root of sum1 (sqrt(sum1)) and multiplying it by the square root of sum2 (sqrt(sum2))
#		iii. Find the cosign value by diving the calculated numerator value by the denominator value
#			a. If denominator is 0, return a cosign value of 0
#		iv. If a word is not found, return -9999
#	b. Calculate PMI value of word pair
#		i. Calculate probability of first word by dividing the word count by total word count
#		ii. Calculate probability of second word by dividing the word count by total word count
#		iii. Calculate probability of the word co-occurence by dividing the co-occurence value by the total word count
#		iv. Calculate the PMI value by dividing the probability of the co-occurence by the mulitplication of the probability of the first and second words and then taking the log base 2 of the result
#		v. If a word is not found or the probability of the co-occurence is zero, return a PMI value of 0
#	c. Output the cosign value, c(1), c(2), c(1,2), and PMI value for each word pair

import sys
import re
import numpy
import math
import os

# Create co-occurence matrix
def calcco(window, vocab, comatrix, text):

	# Split sentence into list of words
	words = text.split()

	# For each word in the sentence, take index of word in vocab and index of each word within a certain window in vocab and increment it (co-occurence value)
	for word, i in zip(words, range(len(words)-window + 1)):
		for j in range(window - 1):
			comatrix[ vocab[words[i] ][0] ][ vocab[words[i+j+1] ][0] ] += 1
			# print(words[i] + " " +  words[i + j + 1])

# Calculate cosign value of word pair
def cosine(vocab, comatrix, pair):

	# Split word pair into list
	words = pair.split()

	numerator = 0
	sum1 = 0
	sum2 = 0
	denominator = 0

	# If both words exist in vocabulary
	if words[0] in vocab.keys() and words[1] in vocab.keys():

		# For each column of both the target row and the context row, use co-occurence values
		for first, second in zip( comatrix[ vocab[ words[0] ][0] ] , comatrix[ vocab[ words[1] ][0]] ):

			# Add to numerator sum multiplying co-occurence of target and word in vocab by co-occurence of context and word in vocab
			numerator += first*second

			# Running sum of square of co-occurence for eventual denominator value
			sum1 += first*first
			sum2 += second*second

		# Create denominator by taking square roots of each sum and multiplying them
		denominator = math.sqrt(sum1)*math.sqrt(sum2)

		# Exception statement
		if denominator == 0:
			return 0

	# If either word is not found
	else:
		return -9999

	return numerator/denominator

# Calculate PMI value of word pair
def pmi(vocab, comatrix, pair, totalWords):

	# Split word pair into list
	words = pair.split()

	# If both words exist in vocabulary
	if words[0] in vocab.keys() and words[1] in vocab.keys():

		# Caclulate proabbility of word 1
		p1 = vocab[words[0]][1]/totalWords

		# Calculate probability of word 2
		p2 = vocab[words[1]][1]/totalWords

		# Calculate proabbility of co-occurence of both words
		p12 = comatrix[vocab[words[0]][0]][vocab[words[1]][0]]/totalWords

		# Exception statement
		if p12 == 0:
			return 0

	# If either word is not found
	else:
		return 0

	# Calculate PMI and return
	return math.log2(p12/(p1*p2))

def main(argv):

	# Input arguments
	window = int(argv[1])
	directory = argv[2]
	fpair = open(argv[3], "r")

	full = ""

	# Parse directory and open all files to append to master string
	with os.scandir(directory) as entries:
		for entry in entries:
			ftrain = open(entry, "r", encoding="ascii", errors='ignore')
			full += ftrain.read()
			full += "\n"

	# Clean text
	full = re.sub(r"[^a-zA-Z0-9 ]", "\n", full).lower()

	# Split text line by line
	lfull = full.split("\n")

	# Read in word pairs
	pairs = fpair.readlines()

	# Create Vocabulary
	index = 0
	totalWords = 0
	vocab = {}

	for word in full.split():
		if word not in vocab.keys():
			vocab.setdefault(word, [index, 1])
			index += 1
		else:
			vocab[word][1] += 1
		totalWords += 1

	# Initialize Matrix
	comatrix = numpy.zeros(( len(vocab), len(vocab) ), int)

	# Calculate co-occurence
	for sentence in lfull:
		calcco(window, vocab, comatrix, sentence)

	# Output data
	for pair in pairs:
		words = pair.split()
		word1 = words[0]
		word2 = words[1]
		print(str("{0:.5f}".format(cosine(vocab, comatrix, pair))) + "\t" + word1 + "\t\t" + word2, end="\t\t")
		try:
			print(vocab[word1][1], end="\t")
		except:
			print(0, end="\t")
		try:
			print(vocab[word2][1], end="\t")
		except:
			print(0, end="\t")
		try:
			print(str(comatrix[vocab[word1][0]][vocab[word2][0]]), end="\t")
		except:
			print(0, end="\t")
		print(str("{0:.5f}".format(pmi(vocab, comatrix, pair, totalWords))))

	# Close files
	ftrain.close()
	fpair.close()

main(sys.argv)
