import os
import json
import argparse
from collections import defaultdict
import random

# Parser
parser = argparse.ArgumentParser(description='State the code of dataset. Default is set to some.')
parser.add_argument('--info',type=list, default=["pej"], help='dataset names')
parser.add_argument('--validation',type=int, default=50, help='validation holdout')
parser.add_argument('--holdout',type=int, default=50, help='testholdout')
parser.add_argument('--merged_name',type=str, required=True)

args = parser.parse_args()
datasets = args.info
val_total = args.validation
hold_total = args.holdout
output_name = args.merged_name

actor_file_buffer = defaultdict(lambda:defaultdict(list))
training_buffer = []
validation_buffer = []
holdout_buffer = []

total_actors = 1
MAGIC_NUMBER = 57
CHECK = 0
train_name = "filelists/{}_train_filelist.txt".format(output_name)
val_name = "filelists/{}_val_filelist.txt".format(output_name)
hold_name = "filelists/{}_hold_filelist.txt".format(output_name)

actors = set()

for dataset in datasets:
    filename = 'filelists/{}_filelist.txt'.format(dataset)
    with open(filename,'r') as f:
        try:
            content = f.read().split('\n')
            CHECK += len(content)
            for line in content:
                path, text = line.split('|')
                actor_file_buffer[dataset][0].append(line)
                actors.add(0)
        except:
            print("Failed to read {}. If it's just a few lines that crashing gracefully".format(filename))
print(len(actors))
val_per_actor = val_total // len(actors)
hold_per_actor = hold_total // len(actors)

if val_per_actor == 0:
    raise Exception("Not enough")
else:
    print("Proceeding to produce {} validation samples per speaker".format(val_per_actor))
    print("Proceeding to produce {} holdout samples per speaker".format(hold_per_actor))

for data_name in actor_file_buffer:
    for actor_name in actor_file_buffer[data_name]:
        actor_data = actor_file_buffer[data_name][actor_name]
        if len(actor_data) < 7*(val_per_actor + hold_per_actor):
            print(val_per_actor + hold_per_actor)
            print(len(actor_data))
            raise Exception("Insufficient data per actor. Actor name {}".format(actor_name))
        else:
            random.Random(MAGIC_NUMBER).shuffle(actor_data)
            validation_buffer.extend(actor_data[:val_per_actor])
            holdout_buffer.extend(actor_data[val_per_actor:val_per_actor+hold_per_actor])
            training_buffer.extend(actor_data[val_per_actor+hold_per_actor:])

print("TOTAL:")
print("Training data: {}".format(len(training_buffer)))
print("Vaidation data: {}".format(len(validation_buffer)))
print("Holdout data: {}".format(len(holdout_buffer)))
print("{} {}".format(CHECK, len(training_buffer) + len(validation_buffer) + len(holdout_buffer)))

with open(train_name, 'w') as f:
    random.Random(MAGIC_NUMBER).shuffle(training_buffer)
    f.write('\n'.join(training_buffer))

with open(val_name, 'w') as f:
    random.Random(MAGIC_NUMBER).shuffle(validation_buffer)
    f.write('\n'.join(validation_buffer))

with open(hold_name, 'w') as f:
    f.write('\n'.join(holdout_buffer))