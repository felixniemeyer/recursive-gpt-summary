import argparse

from file_utils import load_word_occurences, load_word_curves, ensure_trailing_slash, load_meta, save_ranked_words 

parser = argparse.ArgumentParser()

parser.add_argument("project_path", help="directory to write files to", default="")

args = parser.parse_args()

args.project_path = ensure_trailing_slash(args.project_path)

# load word occurences from file
word_occurences = load_word_occurences(args.project_path)

# load meta
meta = load_meta(args.project_path)
total_chars = meta["total_chars"]
kernel_radius = meta["kernel_radius"]

# load word curves from file
(word_curve_x, word_curve_y) = load_word_curves(args.project_path)

word_max_frequencies = {}
word_variances = {}
word_scores = {}

for word in word_curve_x:
    window_start_chars = word_curve_x[word]
    words_in_window = word_curve_y[word]

    max_frequency = 0

    # local_frequency = words_in_window[i] / (2 * args.kernel_radius)
    # usual_frequency = word_occurences / total_chars
    # normalized_frequency = local_frequency / usual_frequency
    # => normalize_factor = 
    normalize_factor = total_chars / (2 * kernel_radius) / word_occurences[word]

    frequency = 0

    varianceSum = 0
    datapoints = len(window_start_chars)

    for i in range(datapoints):
        if i > 0:
            deviation = frequency - 1
            length = window_start_chars[i] - window_start_chars[i-1]
            varianceSum += deviation * deviation * length

        frequency = words_in_window[i] * normalize_factor

        if frequency > max_frequency:
            max_frequency = frequency

    variance = varianceSum / (datapoints - 1) 

    word_variances[word] = variance
    word_max_frequencies[word] = max_frequency
    word_scores[word] = variance * word_occurences[word] ** 2

# order words by variance, keep only word
words_sorted_by_score = [word for (word, _score) in sorted(word_scores.items(), key=lambda x: x[1], reverse=True)]

save_ranked_words(
    args.project_path, 
    words_sorted_by_score, 
    word_occurences,
    word_max_frequencies,
    word_variances
)

