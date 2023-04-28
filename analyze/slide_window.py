
# save word_occurences to file
with open("word_occurences.txt", "w") as f:
    for word in word_occurences:
        f.write(word + " " + str(word_occurences[word]) + "\n")

# load word occurences from file
word_occurences = {}
with open("word_occurences.txt", "r") as f:
    for line in f:
        line = line.split()
        word_occurences[line[0]] = int(line[1])

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

# make a closing entry for every word
for word in word_curve_x: 
    word_curve_x[word].append(total_chars + 1)
    word_curve_y[word].append(0)
