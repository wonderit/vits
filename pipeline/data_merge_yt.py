# Basic python system utility
import argparse
import sys
import os

# Basic collections
from collections import defaultdict
from collections import Counter

# Audio handling
from pydub import AudioSegment

# Parser
parser = argparse.ArgumentParser(description='State the code of dataset. Default is set to some.')
parser.add_argument('--inputpath',type=str, default='filelists/yt_filelist.txt', help="input formatting")
parser.add_argument('--outputpath',type=str, required=True, help="output formatting")

args = parser.parse_args()
script_path = args.inputpath
output_path = args.outputpath

total_duration = 0.0

error = './segmented_character_voice/dahye'
fix = 'assets/dmil'

fixed = []

with open(script_path,'r') as f:
    content = f.read().split('\n')

for line in content:
    path, name, text = line.replace('[KR]','').split('|')
    fixed_path = path.replace(error,fix)
    audio_file = AudioSegment.from_wav(fixed_path)
    total_duration += audio_file.duration_seconds
    fixed.append('|'.join([fixed_path, 'dmil_'+name, text.strip()]))

with open(output_path,'w') as f:
    f.write('\n'.join(fixed))

print("Number of files {}".format(len(fixed)))
print("Total duration {} seconds".format(total_duration))