# read all files from original-texts

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to original-texts")
parser.add_argument("-c", "--min_occurences", help="minimum occurences of a word", default=10)
parser.add_argument("-ks", "--kernel_size", help="kernel radius in characters", default=15)
parser.add_argument("-s", "--step", help="step size in days", default=1)

args = parser.parse_args()

whitespace = [' ', '\n', '\t', '\r', '\f', '\v']

# class that takes a character and outputs 
class Scanner: 
    word = ""

    def __init__(self, on_word):
        self.on_word = on_word

    def handleChar(self, char): 
        if char in whitespace: 
            self.word = self.word.lower()
            self.on_word(self.word)
            self.word = ""
        else: 
            if char.isalpha() or char.isnumeric():
                self.word += char

file_list = sorted(os.listdir(args.path))

word_occurences = {}
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

relevant_word_occurences = {}
for word in word_occurences:
    if word_occurences[word] >= args.min_occurences:
        relevant_word_occurences[word] = word_occurences[word]

print(relevant_word_occurences)


wordCurveX = []
wordCurveY = []

class Window: 
    chars = []
    buildingWindow = True

    location = args.kernel_size / 2

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

    def createKey(self, word):
        if(wordCurveX[word] == None):
            wordCurveX[word] = []
            wordCurveY[word] = []
        elif(wordCurveX[word][-1] == self.location):
            #override if same X as previous entry
            wordCurveY[word][-1] = self.occurences[word]
        else: 
            wordCurveX[word].append(self.occurences[word])
            wordCurveY[word].append(self.occurences[word])

    def handleChar(self, char): 
        if self.buildingWindow: 
            self.windowHeadCounter.handleChar(char)
            self.chars.append(char)
            if len(self.chars) == args.kernel_size:
                self.buildingWindow = False
        else:
            self.windowHeadCounter.handleChar(char)
            self.windowTailCounter.handleChar(self.chars.pop(0))
            self.location += 1

window = Window()
for file_name in file_list:
    with open(args.path + "/" + file_name, "r") as f:
        for char in f.read():
            window.handleChar(char)

# for file in file_list:
#     print(file)
#     with open('original-texts/' + file, 'r') as f:
#         for line in f:
#             # replace hyphens with spaces
#             for word in line.split(): 
#                 word = word.lower()
#                 # remove all non-word characters (german)
#                 word = ''.join([c for c in word if c.isalpha()])
#                 if word != '':
#                     if word in word_occurences:
#                         word_occurences[word] += 1
#                     else:
#                         word_occurences[word] = 1


# remove words with less than X occurences

# ok, the general idea is to keep a window of x chars and parse the text
# at the beginnging ( add to occurences ) and at the end ( subtract from occurences )

# we store changes along with every word by the char index
# we register min and max occurences within the window (is there any way to get the variance?) 

# we calculate the mean by adding up halves of the mean of two neighbouring keys
# then we calculate the variance in a similar way. 

