import IPython.display as ipd
import torch

import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

dir_path = "../drive/MyDrive/elevenlabs_en"
stepk = 100
sample_text = "We establish standards for safe monitoring and early response that can protect people and the environment. Cutting-edge AI technology rapidly detects vision data enabling early responses and providing a safer life."

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file(f"{dir_path}/config.json")
#%%
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    **hps.model)
_ = net_g.eval()

_ = utils.load_checkpoint(f"{dir_path}/G_{stepk}000.pth", net_g, None)
#%%
stn_tst = get_text(sample_text, hps)
with torch.no_grad():
    x_tst = stn_tst.unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
    sid0 = torch.LongTensor([0])
    sid1 = torch.LongTensor([1])
    audio0 = net_g.infer(x_tst, x_tst_lengths, sid=sid0, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
    audio1 = net_g.infer(x_tst, x_tst_lengths, sid=sid1, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()

audio0 = ipd.Audio(audio0, rate=hps.data.sampling_rate, normalize=False)
audio1 = ipd.Audio(audio1, rate=hps.data.sampling_rate, normalize=False)
with open(f'{dir_path}/antoni_step_{stepk}_{sample_text}.wav', 'wb') as f:
  f.write(audio0.data)
with open(f'{dir_path}/bella_step_{stepk}_{sample_text}.wav', 'wb') as f:
  f.write(audio1.data)