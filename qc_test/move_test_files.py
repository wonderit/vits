import csv
import shutil

csv_file = open("./filelists/dex_hold_filelist_test.txt", "r")
f = csv.DictReader(csv_file, delimiter="|", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for row in f:
    print(row["path"])
    # copy the contents of the demo.py file to  a new file called demo1.py
    shutil.copyfile(row["path"], f'./assets_qc_typescript/{row["path"].split("/")[-1]}')

# file = open("./filelists/dex_hold_filelist.txt", "r")
