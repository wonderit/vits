import argparse
import text
from utils import load_filepaths_and_text

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--text_index", default=2, type=int)
  parser.add_argument("--filelists", nargs="+", default=[
    # "filelists/elevenlabs_en_train_filelist.txt","filelists/elevenlabs_en_train_filelist2.txt",
    # "filelists/elevenlabs_en_val_filelist.txt",
    # "filelists/elevenlabs_en_hold_filelist.txt"
    "filelists/elevenlabs_ko_train_filelist.txt",
    "filelists/elevenlabs_ko_val_filelist.txt",
    "filelists/elevenlabs_ko_hold_filelist.txt"
  ])
  parser.add_argument("--text_cleaners", nargs="+", default=[
    "korean_cleaners" #"english_cleaners2"
  ])

  args = parser.parse_args()


  for filelist in args.filelists:
    print("START:", filelist)
    new_filelist = filelist + "." + args.out_extension
    with open(new_filelist, "w", encoding="utf-8") as file:

      filepaths_and_text = load_filepaths_and_text(filelist)
      for i in range(len(filepaths_and_text)):
        original_text = filepaths_and_text[i][args.text_index]
        cleaned_text = text._clean_text(original_text, args.text_cleaners)
        file.write(f"{filepaths_and_text[i][0]}|{filepaths_and_text[i][1]}|{cleaned_text}\n")
        print(f'iteration : {i}, {cleaned_text}')
    file.close()

    # with open(new_filelist, "w", encoding="utf-8") as f:
    #   f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])




