import os
import json
import argparse
import wave
from pydub.utils import mediainfo
from pydub import AudioSegment

# Parser
parser = argparse.ArgumentParser(description='State the code of dataset. Default is set to some.')
parser.add_argument('--info',type=str, required=True, help='validation filelist path')
parser.add_argument('--sourcepath',type=str, default='assets', help='source path to be replaced')
parser.add_argument('--targetpath',type=str, default='assets_cleaned', help='output path of processed audio files')
parser.add_argument('--targetsr',type=int, default=22050, help="Target sampling rate of data. Should be 22050")

args = parser.parse_args()
file_name = args.info
source_path = args.sourcepath
target_path = args.targetpath
target_sr = args.targetsr

with open(file_name,'r') as f:
    content = f.read().split('\n')

# Construct directory
path, _, _ = content[0].split('|')
target_check = "/".join(path.split('/')[:-1]).replace(source_path,target_path,1)
os.makedirs(target_check, exist_ok=True)

for line in content[:-1]:
    path, _, _ = line.split('|')
    info = mediainfo(path)
    frame_rate = info['sample_rate']
    if frame_rate != target_sr:
        output_file_name = "{}".format(path.replace(source_path,target_path,1))
        if not os.path.isfile(output_file_name):
            sound = AudioSegment.from_wav(path)
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(target_sr)
            sound.export(output_file_name, format="wav")