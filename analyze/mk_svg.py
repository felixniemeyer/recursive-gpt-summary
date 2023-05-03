import argparse

from file_utils import load_meta, load_ranked_words, ensure_trailing_slash

parser = argparse.ArgumentParser()

parser.add_argument("project_path", help="directory to write files to", default="")
parser.add_argument("-x", "--size_x", help="number of the most variant words for which the SVG gets generated", default=1000)
parser.add_argument("-y", "--size_y", help="number of the most variant words for which the SVG gets generated", default=8000)

args = parser.parse_args()

args.project_path = ensure_trailing_slash(args.project_path)

(words_sorted_by_score, word_occurences, word_max_frequencies, word_variances) = load_ranked_words(args.project_path)

print(words_sorted_by_score) 

# begin SVG image string
svg = "<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">"

# add v


  <rect x="10" y="10" width="80" height="80" />

svg += "</svg>"
