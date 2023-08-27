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
parser.add_argument('--name',type=str, default='kss', help='name of the dataset')
parser.add_argument('--script',type=str, default='assets/kss/transcript.v.1.4.txt', help="reference scripts")
parser.add_argument('--basepath',type=str, default='assets/kss', help="basepath")
parser.add_argument('--outputpath',type=str, default='filelists/kss_filelist.txt', help="output formatting")

args = parser.parse_args()
script_path = args.script
base_path = args.basepath
final_output_path = args.outputpath
output_buffer = []

total_duration = 0.0

with open(script_path,'r') as f:
    content = f.read().split('\n')

for line in content:
    if line != '':
        raw = line.split('|')
        path = raw[0]
        text = raw[1]
        f_type, fn = path.split('/')
        output_path = "{}/{}".format(base_path, fn)
        try:
            audio_file = AudioSegment.from_wav(output_path)
            total_duration += audio_file.duration_seconds
            output_buffer.append('|'.join([output_path, 'kss_kss', text]))
        except:
            print("Failed on {} gracefully moving on".format(output_path))

print("Total Duration: {} seconds".format(total_duration))
print("Writing to: {}".format(output_path))
with open(final_output_path, 'w') as f:
    f.write("\n".join(output_buffer))