#!/bin/bash

nohup python train.py -c ./configs/dex.json -m ./result-dex > train_dex.log &
