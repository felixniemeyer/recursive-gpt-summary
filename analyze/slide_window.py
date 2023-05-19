import argparse
import os

from scanner import Scanner 
from file_utils import load_word_occurences, ensure_trailing_slash, load_meta, save_word_curves, save_meta

parser = argparse.ArgumentParser()

parser.add_argument("project_path", help="read and write files from this directory", default="")
parser.add_argument("-moc", "--min_occurences", help="minimum occurences of a word", default=10, type=int)
parser.add_argument("-kr", "--kernel_radius", help="kernel radius in characters", default=20000, type=int)

args = parser.parse_args()

# append slash to output if it does not exist
args.project_path = ensure_trailing_slash(args.project_path)

if args.min_occurences < 2:
    print("min_occurences must be at least 2")
    exit()

# load meta
meta = load_meta(args.project_path)
input_path = meta['input_path']
total_chars = meta['total_chars']

# load word occurences from file
word_occurences = load_word_occurences(args.project_path)

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

file_list = sorted(os.listdir(input_path))

window = Window()
for file_name in file_list:
    with open(input_path + file_name, "r") as f:
        for char in f.read():
            window.handleChar(char)

# make a closing entry for every word
for word in word_curve_x: 
    word_curve_x[word].append(meta['total_chars'] + 1)
    word_curve_y[word].append(0)

# save word curves
save_word_curves(args.project_path, word_curve_x, word_curve_y)

# save meta 
meta["kernel_radius"] = args.kernel_radius
save_meta(args.project_path, meta)
