#!/bin/bash

nohup python train_ms.py -c configs/elevenlabs_ko.json -m elevenlabs_ko > train_elevenlabs_ko.log &
