import os 
import pickle

def save_word_occurences(path, word_occurences):
    # save word_occurences to file
    with open(path + "word_occurences.txt", "w") as f:
        for word in word_occurences:
            f.write(word + " " + str(word_occurences[word]) + "\n")

def load_word_occurences(project_path): 
    word_occurences = {}
    with open(project_path + "word_occurences.txt", "r") as f:
        for line in f:
            line = line.split()
            word_occurences[line[0]] = int(line[1])
    return word_occurences

def ensure_trailing_slash(path):
    if path[-1] != "/": 
        path += "/"
    return path

def ensure_trailing_slash_and_mkdir(path):
    path = ensure_trailing_slash(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def save_meta(path, meta): 
    # save meta to file using pickle
    with open(path + "meta.pickle", "wb") as f:
        pickle.dump(meta, f)

def load_meta(path): 
    # load meta from file using pickle
    with open(path + "meta.pickle", "rb") as f:
        return pickle.load(f)

def save_word_curves(path, x, y): 
    # use pickle
    with open(path + "word_curves.pickle", "wb") as f:
        pickle.dump((x, y), f)

def load_word_curves(path): 
    # use pickle
    with open(path + "word_curves.pickle", "rb") as f:
        return pickle.load(f)

def save_ranked_words(path, words_sorted_by_score, word_occurences, word_max_frequencies, word_variances): 
    # write selected words to file
    with open(path + 'ranked_words.csv', 'w') as f:
        f.writelines('word;occurences;max_frequency;local_frequency_variance;score\n')
        for word in words_sorted_by_score:
            f.writelines(
                word + ';' + 
                str(word_occurences[word]) + ';' + 
                str(word_max_frequencies[word]) + ';' + 
                str(word_variances[word]) + '\n'
            )

def load_ranked_words(path): 
    words_sorted_by_score = []
    word_occurences = {}
    word_max_frequencies = {}
    word_variances = {}
    with open(path + 'ranked_words.csv', 'r') as f: 
        f.readline()
        for line in f:
            print(line) 
            values = line.split(';')
            word = values[0]
            words_sorted_by_score.append(word)
            word_occurences[word] = int(values[1])
            word_max_frequencies[word] = float(values[2])
            word_variances[word] = float(values[3])

    return (words_sorted_by_score, word_occurences, word_max_frequencies, word_variances)

