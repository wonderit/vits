import IPython.display as ipd
import torch

import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

dir_path = "../drive/MyDrive/elevenlabs_ko"
stepk = 35
sample_text = "사람과 환경을 보호할 수 있는, 안전한 모니터링과, 조기대응을 위한 기준을 마련합니다. 최첨단 AI 기술로, 비전 데이터를 신속하게 감지해, 조기 대응이 가능하고, 보다 안전한 삶을 제공합니다."

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
with open(f'{dir_path}/antoni_step_{stepk}_{sample_text[0:5]}.wav', 'wb') as f:
  f.write(audio0.data)
with open(f'{dir_path}/bella_step_{stepk}_{sample_text[0:5]}.wav', 'wb') as f:
  f.write(audio1.data)