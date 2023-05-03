# read all files from original-texts

import os
import argparse

from scanner import Scanner
from file_utils import save_word_occurences, ensure_trailing_slash_and_mkdir, ensure_trailing_slash, save_meta

parser = argparse.ArgumentParser()
parser.add_argument("input_path", help="input to original texts")
parser.add_argument("project_path", help="directory to write files to", default="")

args = parser.parse_args()

args.project_path = ensure_trailing_slash_and_mkdir(args.project_path)
args.input_path = ensure_trailing_slash(args.input_path)

file_list = sorted(os.listdir(args.input_path))

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
    with open(args.input_path + file_name, "r") as f:
        for char in f.read():
            counter.handleChar(char)
            total_chars += 1

save_word_occurences(args.project_path, word_occurences)

save_meta(args.project_path, {
    "total_chars": total_chars,
    "input_path": args.input_path,
})
