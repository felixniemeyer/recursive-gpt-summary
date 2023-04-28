# read all files from original-texts

import os
import argparse

import math

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to original-texts")
parser.add_argument("-c", "--min_occurences", help="minimum occurences of a word", default=20)
parser.add_argument("-kr", "--kernel_radius", help="kernel radius in characters", default=20000)
parser.add_argument("-s", "--step", help="step size in days", default=1)
parser.add_argument("-n", "--number", help="number of the most variant words for which the SVG gets generated", default=500)
parser.add_argument("-o", "--output", help="output directory", default="")

args = parser.parse_args()

if args.min_occurences < 2:
    print("min_occurences must be at least 2")
    exit()

# append slash to output if it does not exist
if args.output[-1] != "/": 
    args.output[-1] += "/"

# make output dir if it does not exist
os.mkdir(args.output) 

whitespace = [' ', '\n', '\t', '\r', '\f', '\v']

# class that takes a character and outputs 
class Scanner: 
    word = ""

    def __init__(self, on_word):
        self.on_word = on_word

    def handleChar(self, char): 
        if char in whitespace and self.word != "":
            self.word = self.word.lower()
            self.on_word(self.word)
            self.word = ""
        else: 
            if char.isalpha() or char.isnumeric():
                self.word += char

file_list = sorted(os.listdir(args.path))

# count occurences of all words
word_occurences = {}
total_chars = 0
def countWord(word):
    if word in word_occurences:
        word_occurences[word] += 1
    else: 
        word_occurences[word] = 1
counter = Scanner(countWord)

for file_name in file_list:
    with open(args.path + "/" + file_name, "r") as f:
        for char in f.read():
            counter.handleChar(char)
            total_chars += 1


# word_max_frequency = {}
# 
# for word in word_curve_x:
#     x_values = word_curve_x[word]
#     y_values = word_curve_y[word]
#     max_frequency = 0
#     word_frequencies[word] = []
#     for i in range(len(x_values)):
#         frequency = y_values[i] / word_occurences[word]
#         frequency *= normalize_factor
#         word_frequencies[word].append(frequency)
#         if frequency > max_frequency:
#             max_frequency = frequency
# 
#     word_max_frequency[word] = max_frequency
# 
# # sort words by frequency
# sorted_words = sorted(word_max_frequency.items(), key=lambda x: x[1], reverse=True)
# 
# # print top n words
# for i in range(args.number):
#     word = sorted_words[i][0]
#     print(word, word_max_frequency[word], word_occurences[word])
# 
# print('es', word_max_frequency['es'], word_occurences['es'])
# print('nina', word_max_frequency['nina'], word_occurences['nina'])

normalize_factor = total_chars / (2 * args.kernel_radius)

word_variances = {}
word_scores = {}

for word in word_curve_x:
    window_start_chars = word_curve_x[word]
    words_in_window = word_curve_y[word]

    woc = word_occurences[word]

    frequency = 0

    varianceSum = 0
    datapoints = len(window_start_chars)

    for i in range(datapoints):
        if i > 0:
            deviation = frequency - 1
            length = window_start_chars[i] - window_start_chars[i-1]
            varianceSum += deviation * deviation * length

        frequency = words_in_window[i] / woc
        frequency *= normalize_factor

    variance = varianceSum / (datapoints - 1) 

    word_variances[word] = variance
    # score words with more occurences slightly higher

    word_scores[word] = variance * math.pow(woc, 2)

# order words by variance
words_sorted_by_score = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

# print top n words
for i in range(int(args.number)):
    word = words_sorted_by_score[i][0]
    print(word, word_scores[word], word_occurences[word])

print('es', word_scores['es'], word_occurences['es'])
print('nina', word_scores['nina'], word_occurences['nina'])
