"""PathMNIST CC BY 4.0. Deterministic stratified subset; official splits stay separate."""
import numpy as np,json,hashlib
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]; raw=root/'training-data'; out=root/'dist/training';out.mkdir(exist_ok=True)
f=raw/'pathmnist.npz'; md5=hashlib.md5(f.read_bytes()).hexdigest()
assert md5=='a8b06965200029087d5bd730944a56c1',md5
z=np.load(f);rng=np.random.default_rng(5316);splits={};labels=['adipose','background','debris','lymphocytes','mucus','smooth muscle','normal colon mucosa','cancer-associated stroma','colorectal adenocarcinoma epithelium']
for split,count in [('train',100),('val',25),('test',25)]:
 y=z[split+'_labels'].reshape(-1);indices=np.concatenate([rng.choice(np.flatnonzero(y==c),count,replace=False) for c in range(9)]);rng.shuffle(indices)
 x=z[split+'_images'][indices];x.tofile(raw/(split+'.bin'));(raw/(split+'-labels.json')).write_text(json.dumps(y[indices].tolist()))
 splits[split]={'count':len(indices),'indices':indices.tolist(),'perClass':count,'officialCount':len(y),'sha256':hashlib.sha256(x.tobytes()).hexdigest()}
 if split=='train':
  mosaic=Image.new('RGB',(9*56,56))
  for c in range(9):mosaic.paste(Image.fromarray(x[np.flatnonzero(y[indices]==c)[0]]).resize((56,56)),(c*56,0))
  mosaic.save(out/'samples.png')
card={'id':'pathmnist-28-subset-seed5316','name':'PathMNIST','version':'MedMNIST v2 / 28px; Zenodo 10519652','license':'CC BY 4.0','url':'https://zenodo.org/records/10519652','attribution':'Jiancheng Yang et al., MedMNIST v2 (2023); source: Jakob Nikolas Kather et al., NCT-CRC-HE-100K / CRC-VAL-HE-7K (2019).','sourceCitation':'Kather et al. Predicting survival from colorectal cancer histology slides using deep learning: A retrospective multicenter study. PLOS Medicine 16(1), e1002730 (2019).','type':'H&E-stained colorectal tissue microscopy patches','seed':5316,'classes':labels,'md5':md5,'preprocessing':'28×28 RGB → bilinear 64×64; pixels normalized to [-1,1]; no augmentation; official splits retained; stratified sampling','splits':splits,'limitations':'Small stratified subset and 8-epoch partial fine-tuning experiment; no medical use; no claim of complete organ understanding. Test split held out until final epoch. Everyday-photo probes are outside the training distribution.'}
(out/'dataset.json').write_text(json.dumps(card,indent=2));print('Prepared',[(k,v['count']) for k,v in splits.items()])
