# read all files from original-texts

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to original-texts")
parser.add_argument("-c", "--min_occurences", help="minimum occurences of a word", default=20)
parser.add_argument("-kr", "--kernel_radius", help="kernel radius in characters", default=20000)
parser.add_argument("-s", "--step", help="step size in days", default=1)
parser.add_argument("-n", "--number", help="number of the most variant words for which the SVG gets generated", default=10)

args = parser.parse_args()

if args.min_occurences < 2:
    print("min_occurences must be at least 2")
    exit()

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

# keep a window of x chars and parse the text
# at the beginnging ( add to occurences ) and at the end ( subtract from occurences )
# we store changes along with every word by the char index
word_curve_x = {}
word_curve_y = {}
class Window: 
    chars = []
    building_window = True

    location = args.kernel_radius

    occurences = {}

    def __init__(self):
        self.windowHeadCounter = Scanner(self.windowHeadWordAdder)
        self.windowTailCounter = Scanner(self.windowTailSubtractor)

    def windowHeadWordAdder(self, word): 
        if word in self.occurences:
            self.occurences[word] += 1
        else: 
            self.occurences[word] = 1
        self.createKey(word)

    def windowTailSubtractor(self, word):
        self.occurences[word] -= 1
        self.createKey(word)

    def createKey(self, word):
        if word_occurences[word] >= args.min_occurences:
            if not word in word_curve_x:
                word_curve_x[word] = [self.location]
                word_curve_y[word] = [self.occurences[word]]
            elif(word_curve_x[word][-1] == self.location):
                #override if same X as previous entry
                word_curve_y[word][-1] = self.occurences[word]
            else: 
                word_curve_x[word].append(self.location)
                word_curve_y[word].append(self.occurences[word])

    def handleChar(self, char): 
        if self.building_window: 
            self.windowHeadCounter.handleChar(char)
            self.chars.append(char)
            if len(self.chars) == args.kernel_radius * 2: 
                self.building_window = False
        else:
            self.windowHeadCounter.handleChar(char)
            self.chars.append(char)
            self.windowTailCounter.handleChar(self.chars.pop(0))
            self.location += 1

window = Window()
for file_name in file_list:
    with open(args.path + "/" + file_name, "r") as f:
        for char in f.read():
            window.handleChar(char)

word_frequencies = {}

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
    x_values = word_curve_x[word]
    y_values = word_curve_y[word]

    woc = word_occurences[word]

    frequency = 0

    varianceSum = 0
    datapoints = len(x_values)

    for i in range(datapoints):
        if i > 0:
            deviation = frequency - 1
            length = x_values[i] - x_values[i-1]
            varianceSum += deviation * deviation * length

        frequency = y_values[i] 
        frequency *= normalize_factor

    variance = varianceSum / (datapoints - 1) 

    word_variances[word] = variance
    word_scores[word] = variance * 

# order words by variance
words_sorted_by_score = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

# print top n words
for i in range(int(args.number)):
    word = words_sorted_by_score[i][0]
    print(word, word_scores[word], word_occurences[word], word_curve_y[word])

print('es', word_scores['es'], word_occurences['es'])
print('nina', word_scores['nina'], word_occurences['nina'])
