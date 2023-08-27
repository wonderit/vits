# Basic python system utility
import argparse
import sys
import os

# Parser
parser = argparse.ArgumentParser(description='Name the train val hold set.')
parser.add_argument('--path',type=list, default=['filelists/doppel_train_filelist.txt.cleaned','filelists/doppel_val_filelist.txt.cleaned','filelists/doppel_hold_filelist.txt.cleaned'])

args = parser.parse_args()
files_to_clean = args.path
speakers = set()
speaker_map = {}

for fn in files_to_clean:
    recycle = []
    with open(fn,'r') as f:
        content = f.read().split('\n')
        for line in content:
            if not line == '':
                path, sid, text = line.split('|')
                if not sid in speaker_map:
                    speaker_map[sid] = len(speakers)
                    new_sid = speaker_map[sid]
                    speakers.add(sid)
                else:
                    new_sid = speaker_map[sid]
                if os.path.isfile(path.replace('assets','assets_cleaned',1)):
                    recycle.append("{}|{}|{}".format(path,new_sid,text))
                else:
                    print(line)
    with open(fn,'w') as f:
        f.write('\n'.join(recycle))

print("Mapping")
print(speaker_map)
for sid in speaker_map:
    print("{}: {}".format(sid, speaker_map[sid]))