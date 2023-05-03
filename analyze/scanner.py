whitespace = [' ', '\n', '\t', '\r', '\f', '\v']

# class that takes a character and outputs 
class Scanner: 
    word = ""

    def __init__(self, on_word):
        self.on_word = on_word

    def handleChar(self, char): 
        if char in whitespace and self.word != "": 
            if self.word[0:4] != "http":
                self.word = self.word.lower()
                self.on_word(self.word)
            self.word = ""
        else: 
            if char.isalpha() or char.isnumeric():
                self.word += char
