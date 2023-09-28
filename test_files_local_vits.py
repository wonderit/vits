import csv
import IPython.display as ipd
import torch

import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

dir_path = "./models/dex"
output_path = "./assets_qc_vits"
stepk = 147

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file(f"{dir_path}/config.json")
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model)
_ = net_g.eval()

print(f"{dir_path}/G_{stepk}000.pth")
_ = utils.load_checkpoint(f"{dir_path}/G_{stepk}000.pth", net_g, None)


csv_file = open("./filelists/dex_hold_filelist_test.txt", "r")
f = csv.DictReader(csv_file, delimiter="|", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

for row in f:
    print(row["text"])

    stn_tst = get_text(row["text"], hps)
    with torch.no_grad():
        x_tst = stn_tst.unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
        sid0 = torch.LongTensor([0])
        audio0 = net_g.infer(x_tst, x_tst_lengths, sid=sid0, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][
            0, 0].data.cpu().float().numpy()

    audio0 = ipd.Audio(audio0, rate=hps.data.sampling_rate, normalize=False)
    with open(f'{output_path}/{row["path"].split("/")[-1]}', 'wb') as f:
        f.write(audio0.data)