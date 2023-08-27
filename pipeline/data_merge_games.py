# Basic python system utility
import argparse
import sys
import os

# Basic collections
from collections import defaultdict
from collections import Counter

# XML API
import xml.etree.ElementTree as ET

# Audio handling
from pydub import AudioSegment

# Parser
parser = argparse.ArgumentParser(description='State the code of dataset.')
parser.add_argument('--name',type=str, required=True, help='name of the dataset.')
parser.add_argument('--hashsid',type=bool, default=False, help="'anonymize' the speaker.")

args = parser.parse_args()

# Game title and book-keeping
dataset_name = args.name
anon = args.hashsid
stats = defaultdict(float)
total_duration = 0.0

# Base directories
base_script_directory = 'assets/{}_assets/TextAsset/script'.format(dataset_name)
base_audio_directory = 'assets/{}_assets/AudioClip'.format(dataset_name)

# XML tree and its root
mytree = ET.parse(base_script_directory)
myroot = mytree.getroot()

# dfs boiler plate
def dfs(node, buffer):
    for child in list(node):
        if(child.tag == "page"):
            buffer.append(child)
        dfs(child, buffer)
    
# anonymize
def hasher(dataset, sid):
    return "{}_{}".format(dataset, sid)

# page and content buffer
pages = []
content = []
final_output = []

# Character mapping name -> id
character_mapping = defaultdict(Counter)
init_to_char = {}
char_to_init = {}

# traverse XML
dfs(myroot, pages)

for page in pages:
    if 'comment' in page.attrib and page.attrib["comment"] != "":
        page_content = page.find('content')
        if not page_content is None:
            text = page_content.find('text')
            if not text is None:
                content.append((page.attrib["comment"], text.attrib["data"]))

# Character map builder
for audio_path, text in content:
    # filename
    initial, _ = audio_path.split('=')
    # textname
    try:
        character, _ = text.split(';')
        character_mapping[initial.replace('@','')][character.replace('#t=','')] += 1
    except:
        print(text)
        print("Shouldn't be happening unless it's a special text")
        print("-------------------------------------------------")

# Create initial to name mapping
for init in character_mapping:
    init_to_char[init] = character_mapping[init].most_common(1)[0][0]

# Reverse mapping
for init in init_to_char:
    char_to_init[init_to_char[init]] = init

for audio_path, text in content:
    cleaned_path = audio_path.replace(';','').replace('@','').replace('=','_')
    init_extract = len(cleaned_path) - 1 - list(reversed(cleaned_path)).index('_')
    if anon:
        char_name = hasher(dataset_name, cleaned_path[:init_extract])
    else:
        char_name = dataset_name + '_' + init_to_char[cleaned_path[:init_extract]]
    try:
        line = text[text.index(';')+1:]
    except ValueError:
        print(text)
        print("Value error")
        print("-------------------------------------------------")
    final_file = "{}/{}.wav".format(base_audio_directory,cleaned_path)
    if os.path.isfile(final_file):
        final_output.append('|'.join([final_file, char_name, line]))
        file_duration = AudioSegment.from_wav(final_file).duration_seconds
        stats[char_name] += file_duration
        total_duration += file_duration
    else:
        pass

with open('filelists/{}_filelist.txt'.format(dataset_name),'w') as f:
    f.write('\n'.join(final_output))

print("Number of files {}".format(len(final_output)))
print("Total duration {} seconds".format(total_duration))
print("Duration stats")

for name in stats:
    print("{}: {} seconds".format(name, stats[name]))