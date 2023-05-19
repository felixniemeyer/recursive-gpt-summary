import argparse
import colorhash

from file_utils import load_word_curves, load_ranked_words, ensure_trailing_slash, load_meta

parser = argparse.ArgumentParser()

parser.add_argument("project_path", help="directory to write files to", default="")
parser.add_argument("-x", "--size_x", help="svg canvas size x", default=700, type=int)
parser.add_argument("-y", "--size_y", help="svg canvas size y", default=12000, type=int)
parser.add_argument("-s", "--stroke_width", help="svg stroke_width", default=2)
parser.add_argument("-f", "--font_size", help="font size", default=16)
parser.add_argument("-n", "--number_of_words", help="maximal number of words (ranked highest). 0 = no limit", default=160, type=int)
parser.add_argument("-t", "--threshold", help="don't show lines where normalized frequency < t", default=0.3)
parser.add_argument("-ls", "--label_space", help="how much space to leave for labels", default=0.3)

args = parser.parse_args()

args.project_path = ensure_trailing_slash(args.project_path)

(
    words_sorted_by_score, 
    word_occurences, 
    word_variances, 
    word_max_frequencies, 
    word_max_frequencies_ats, 
    word_frequencies
) = load_ranked_words(args.project_path)

(word_curves_char_index, word_curves_raw_frequency) = load_word_curves(args.project_path)

meta = load_meta(args.project_path)

total_chars = meta["total_chars"]

# begin SVG image string
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}">'.format(args.size_x, args.size_y)
svg += '<style>'
svg += '.label { font-family: sans-serif; font-size: ' + str(args.font_size) + 'px; dominant-baseline: middle; text-anchor: end; }'
svg += '.curve { fill: none; stroke-width: ' + str(args.stroke_width) + '; }'
svg += '</style>'


# for every word draw curve and label
w = 0
startline = '<polyline points="'
width = args.size_x * (1 - args.label_space) / (1 - args.threshold)

included_words = []

for word in words_sorted_by_score:
    char_indices = word_curves_char_index[word]
    frequencies = word_frequencies[word]

    colorHasher = colorhash.ColorHash(word)
    endline = '" class="curve" data-word="{}" stroke="{}" />'.format(
        word,
        colorHasher.hex
    )

    max_frequency = word_max_frequencies[word]

    previous_normalized = 0
    y = 0
    x = 0

    skipping = False

    curve = startline

    datapoints = len(char_indices)
    for i in range(datapoints - 1):
        normalized = frequencies[i] / max_frequency

        skip = False
        if normalized < args.threshold: 
            if previous_normalized < args.threshold: 
                skip = True

        if (not skipping) and skip: 
            curve += endline

        if skipping and (not skip): 
            curve += startline
            # add previous point
            curve += '{},{} '.format(
                x, 
                y
            )

        y = char_indices[i] / total_chars * args.size_y 
        x = args.size_x - (normalized - args.threshold) * width
        if skip: 
            skipping = True
        else: 
            skipping = False
            curve += '{},{} '.format(x, y)

        previous_normalized = normalized
    
    if not skipping: 
        curve += endline

    svg += curve

    included_words.append((
        word, 
        word_max_frequencies_ats[word] / total_chars * args.size_y,
        colorHasher.hex
    ))

    w += 1
    if (args.number_of_words > 0) and (w >= args.number_of_words): 
        break

# make sure word lables don't overlap
included_words.sort(key=lambda x: x[1])

line_height = args.font_size * 1.2
half_line_height = line_height / 2

label_y_positions = {}

i = 0
while i < len(included_words):
    center_y = included_words[i][1] 

    count_i = 1

    top_i = i
    bottom_i = i

    def adjustCenter(ii): 
        global count_i, center_y
        y = included_words[ii][1] 
        center_y = (center_y * count_i + y) / (count_i + 1)
        if(center_y - count_i * half_line_height - line_height < 0): 
            center_y = count_i * half_line_height + line_height
        elif(center_y + count_i * half_line_height + line_height > args.size_y): 
            center_y = args.size_y - count_i * half_line_height - line_height
        count_i += 1

    def check_forward(): 
        global center_y, top_i, bottom_i, count_i
        if bottom_i + 1 < len(included_words): 
            if center_y + (count_i * half_line_height) > included_words[bottom_i + 1][1] - half_line_height: 
                # expand bottom
                bottom_i += 1
                adjustCenter(bottom_i)
                check_forward()
                check_backward()

    def check_backward():
        global center_y, top_i, bottom_i, count_i
        if top_i != 0: 
            if center_y - (count_i * half_line_height) < included_words[top_i - 1][1] + half_line_height:
                # expand top
                top_i -= 1
                adjustCenter(top_i)
                check_backward()
                check_forward()

    check_forward()

    if top_i == bottom_i: 
        i += 1
    else: 
        # redistribute words
        start_y = center_y - (count_i * half_line_height) + half_line_height
        c = 0
        for j in range(top_i, bottom_i + 1):
            included_words[j] = (
                included_words[j][0],
                start_y + (c * line_height), 
                included_words[j][2]
            )
            c += 1
        i = bottom_i + 1

    
for word_info in included_words:
    word = word_info[0]
    svg += '<text x="{}" y="{}" class="label" data-word="{}" fill="{}">{}</text>'.format(
        args.size_x * args.label_space * 0.9,
        word_info[1], 
        word, 
        word_info[2],
        word
    )

# create time axis (y) 
svg += '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#333" stroke-width="3" />'.format(
    args.size_x, args.font_size, args.size_x, args.size_y - args.font_size * 2
)

svg += '</svg>'

# write to file
with open(args.project_path + 'word_curves.svg', 'w') as f:
    f.write(svg)

