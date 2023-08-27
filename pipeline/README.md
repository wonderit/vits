# Data processing pipeline

## Dependencies
```
pydub
```

## Structure
```
preprocess_audio.py <- primarily for upsampling as of now.
data_merge_{NAME}.py <- merges voice text pair for given NAME dataset.
merge_split_data.py <- merges and splits to train/val/test set.
preprocess.py <- text cleaning.
```

## Procedure
```
1. pipeline/data_merge_NAME.py
2. pipeline/preprocess_audio.py
3. pipeline/data_merge_NAME.py
5. pipeline/merge_split_data.py
6. preprocess.py
```