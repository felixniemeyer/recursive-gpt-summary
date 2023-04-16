import os 
import openai
import argparse
import json

from pathlib import Path

# support .env file
from dotenv import load_dotenv
load_dotenv()

# open ai key
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

CHARS_PER_TOKEN = 4.5

parser = argparse.ArgumentParser(
    prog='Chunked Summary',
    description='Summarizes a long text of a long text using chatGPT', 
)

parser.add_argument('-d', '--directory', type=str, help='Directory with input files', required=True)

parser.add_argument('-pp', '--prepromt', type=str, help='Prompt text before each chunk', required=False, 
                    default='Fasse diesen Text in der Ich-Perspektive zusammen.')

parser.add_argument('-cp', '--contextpromt', type=str, help='Target directory for output files', required=False, 
                    default='Hier ist das Ende der vorherigen Zusammenfassung: <context> Schließe daran an.')

parser.add_argument('-ol', '--overlap', type=int, help='Number of chars to overlap', required=False, 
                    default=300)
parser.add_argument('-cl', '--context', type=int, help='Number of chars from previous summary as context', 
                    required=False, default=300)
parser.add_argument('-c', '--chunksize', type=int, help='Target chunk size in tokens', required=False, 
                    default=2500)
# factor has to be less than 1
parser.add_argument('-f', '--factor', type=int, help='Factor by which chatGPT should reduce by summary', required=False, 
                    default=0.33)

parser.add_argument('-fk', '--fake-summary', action='store_true', help='Use fake summarization instead of chatGPT', 
                    default=False)

args = parser.parse_args()

target_char_count = args.chunksize * CHARS_PER_TOKEN * args.factor 
if(target_char_count < args.overlap):
    print("Overlap has to be smaller than target summary size")
    exit(1)

if(args.factor < 0.05 or args.factor > 0.75):
    print("Factor has to be between 0.05 and 0.5")
    exit(1)

# remove trailing slash
if(args.directory.endswith("/")):
    args.directory = args.directory[:-1]

# check that subdirectory 'original' exists
original_dir = args.directory + "/original"
if not os.path.exists(original_dir):
    print("Directory " + original_dir + " does not exist")
    exit(1)

condense_prompt = "Verwende etwa <wc> Wörter und schreibe in der Ich-Perspektive"

def summarize(context, thoughts):
    if(args.fake_summary):
        return fakeSummarize(context, thoughts)
    else:
        return chatGPTSummarize(context, thoughts)

def chatGPTSummarize(context, thoughts):
    print("Summarizing " + thoughts)

    messages = []

    messages.append({
        "role": "user", "content": thoughts
    }) 
    messages.append({
        "role": "system", "content": args.prepromt
    }) 

    if(len(context) > 0):
        messages.append({
            "role": "system", "content": args.contextpromt.replace("<context>", context)
        }) 

    target_word_count = len(thoughts) / 5 * args.factor
    target_word_count = int(target_word_count / 50) * 50

    messages.append({
        "role": "system", "content": condense_prompt.replace("<wc>", str(target_word_count))
    })

    print("Prompts: ", messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    summary = response["choices"][0]["message"]["content"]

    print("Summary: " + summary)

    return summary

def fakeSummarize(context, thoughts):
    counter = 0
    takeEach = 1 / args.factor
    summary = ""
    for c in thoughts:  
        counter += 1
        if(counter > takeEach):
            counter -= takeEach
            summary += c
    return summary


def processFolder(fromFolderName, level, origins, summaries):
    fromFolder = args.directory + '/' + fromFolderName
    toFolder = args.directory + '/' + str(level)
    Path(toFolder).mkdir(parents=True, exist_ok=True)
    thoughts = ""
    current_file = ""
    # new set 
    origin_files = []
    context = ""
    file_counter = 0

    def createFile(summary): 
        nonlocal file_counter
        nonlocal origin_files
        nonlocal origins
        nonlocal summaries

        with open(toFolder + '/' + str(file_counter), "w") as f:
            f.write(summary)

        file_id = str(level) + '/' + str(file_counter)
        origins[file_id] = origin_files
        for origin in origin_files:
            if origin not in summaries:
                summaries[origin] = []
            summaries[origin].append(file_id)

        file_counter += 1

        return summary


    for filename in sorted(os.listdir(fromFolder)):
        current_file = fromFolderName + '/' + filename
        origin_files.append(current_file)
        with open(fromFolder + '/' + filename, "r") as f:
            print("reading " + filename)
            thoughts += f.read()

            char_count = len(thoughts) + len(args.prepromt) + len(context) + len(condense_prompt) + args.overlap
            if(len(context) > 0):
                char_count += len(args.contextpromt)

            if(char_count > args.chunksize * CHARS_PER_TOKEN):
                excess_chars = char_count - args.chunksize * CHARS_PER_TOKEN
                chars = int(len(thoughts) - excess_chars)

                print("Summarizing " + str(chars) + " chars")

                summary = summarize(context, thoughts[:chars])
                createFile(summary)

                # create new set of origin files 
                origin_files = [current_file]

                context = summary[-args.context:]
                thoughts = thoughts[chars - args.overlap:]

    summary = summarize(context, thoughts)
    createFile(summary)

    return file_counter

origins = {}
summaries = {} # a file may have 2 files as a summary, when it's contents are split

level = 1
file_count = processFolder('original', level, origins, summaries)

while file_count > 1: 
    file_count = processFolder(str(level), level + 1, origins, summaries)
    level += 1

# write origins and summaries into json files
with open(args.directory + '/origins.json', 'w') as f:
    json.dump(origins, f)

with open(args.directory + '/summaries.json', 'w') as f:
    json.dump(summaries, f)

# write number of levels into file
with open(args.directory + '/levels', 'w') as f:
    f.write(str(level))

