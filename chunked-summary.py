import os 
import openai
import argparse

from pathlib import Path

CHARS_PER_TOKEN = 4.5

parser = argparse.ArgumentParser(
    prog='Chunked Summary',
    description='Summarizes a long text of a long text using chatGPT', 
)

parser.add_argument('-d', '--directory', type=str, help='Directory with input files', required=True)
parser.add_argument('-s', '--startswith', type=str, help='Read only files that start like this', required=True)
parser.add_argument('-t', '--target', type=str, help='Target directory for output files', required=True)

parser.add_argument('-pp', '--prepromt', type=str, help='Prompt text before each chunk', required=False, 
                    default='Please summarize the following text fragment:\n')
parser.add_argument('-cp', '--contextpromt', type=str, help='Target directory for output files', required=False, 
                    default='Here is some context: ...')
parser.add_argument('-ol', '--overlap', type=int, help='Number of chars to overlap', required=False, 
                    default=300)
parser.add_argument('-cl', '--context', type=int, help='Number of chars from previous summary as context', 
                    required=False, default=300)
parser.add_argument('-c', '--chunksize', type=int, help='Target chunk size in tokens', required=False, 
                    default=3000)

args = parser.parse_args()

openai.api_key = "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"

startswith = "2023-03" # TODO: change to e.g. 2023-01

def summarize(context, thoughts, outfile):
    print("Making request")

    messages = []

    if(len(context) > 0):
        messages.append({
            "role": "system", "content": args.contextpromt + context
        }) 

    messages.append({
        "role": "user", "content": args.prepromt + thoughts
    }) 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    print(response) 

    summary = response["choices"][0]["message"]["content"]

    print("Summary: " + summary)

    with open(args.target + outfile, "w") as f:
        f.write(summary)

    return summary
        
thoughts = ""
start_file = None
current_file = None
context = ""
previous_outfile = None
outfile_counter = 0
for filename in sorted(os.listdir(args.directory)):
    print(filename)
    if filename.startswith(args.startswith):
        print("processing")
        if(start_file == None): 
            start_file = filename
        current_file = filename
        with open(args.directory + filename, "r") as f:
            print("reading " + filename)
            thoughts += f.read()

            char_count = len(thoughts) + len(args.prepromt) + len(context) + args.overlap
            if(len(context) > 0):
                char_count += len(args.contextpromt)

            if(char_count > args.chunksize * CHARS_PER_TOKEN):
                excess_chars = char_count - args.chunksize * CHARS_PER_TOKEN
                chars = int(len(thoughts) - excess_chars)

                outfile = args.target + start_file + "_" + current_file 
                if(outfile == previous_outfile):
                    outfile_counter += 1
                    outfile += "_" + str(outfile_counter)
                else:
                    outfile_counter = 0
                    previous_outfile = outfile

                print("Summarizing " + str(chars) + " chars")
                summary = summarize(context, thoughts[:chars], outfile)

                context = summary[-args.context:]
                thoughts = thoughts[chars - args.overlap:]

                start_file = current_file

summarize(context, thoughts, args.target + start_file + "_" + current_file)
