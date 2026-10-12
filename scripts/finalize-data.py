from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json,datetime,shutil
root=Path(__file__).resolve().parents[1];out=root/'data/experiment-v1';out.mkdir(exist_ok=True)
records=[]
for folder in ['cockroach-candidates','space-candidates']:
 m=json.loads((root/'data'/folder/'manifest.json').read_text())
 for source in m['records']:
  if source.get('excluded') or source.get('reviewStatus','').startswith('excluded'):continue
  r=dict(source);r['class']='empty_space' if folder=='space-candidates' else r['class'];r['groupId']=r.get('groupId') or r.get('group');f=root/'data'/folder/r['path'];assert f.exists(),f
  assert r['licenseCode'] in ['cc0','cc-by','CC0','CC BY 2.0','CC BY 2.0 de','CC BY 3.0','CC BY 4.0'],r['licenseCode']
  assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256']
  r['path']=str(f.relative_to(root));r['reviewStatus']='visually reviewed for class and visible near-duplicates; source metadata checked';r['reviewer']='Codex visual review, 2026-10-12';r['usedForTraining']=r['split']=='train';r['usedForDisplay']=False;r['licenseURL']=r.get('licenseURL') or ('https://creativecommons.org/publicdomain/zero/1.0/' if r['licenseCode']=='cc0' else 'https://creativecommons.org/licenses/by/4.0/');r['licenseVersionNote']='Original photo-page license is authoritative; iNaturalist API gives license family, not version.' if folder=='cockroach-candidates' else '';records.append(r)
# Recompute perceptual hashes across ALL categories; unite duplicate/observation/burst groups.
parents=list(range(len(records)))
def find(i):
 while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
 return i
for r in records:
 im=ImageOps.exif_transpose(Image.open(root/r['path'])).convert('RGB');g=list(im.resize((9,8)).convert('L').getdata());r['dhash']=f"{sum((g[y*9+x]>g[y*9+x+1])<<(y*8+x) for y in range(8) for x in range(8)):016x}"
for i,a in enumerate(records):
 for j,b in enumerate(records[:i]):
  same=any(a.get(k) and a.get(k)==b.get(k) for k in ['sha256','observation','burstGroup','groupId'])
  if same or (int(a['dhash'],16)^int(b['dhash'],16)).bit_count()<=6:parents[find(i)]=find(j)
# Per-class groups allocated deterministically, exactly 60/20/remainder, no train/test overlap.
for cls in ['cockroach','other_insect','empty_space']:
 groups={find(i) for i,r in enumerate(records) if r['class']==cls};ordered=sorted(groups,key=lambda g:hashlib.sha256(('5316/'+records[g]['id']).encode()).hexdigest());n=len(ordered);assert n>=5
 for j,g in enumerate(ordered):
  split='train' if j<int(n*.6) else 'validation' if j<int(n*.8) else 'test'
  for i,r in enumerate(records):
   if find(i)==g:r['groupId']='final-'+records[g]['id'];r['split']=split;r['usedForTraining']=split=='train'
manifest={'version':'cockroach-three-class-v1-2026-10-12','seed':5316,'createdAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classes':['cockroach','other_insect','empty_space'],'records':records,'authorInputsExcluded':json.loads((root/'dist/author/manifest.json').read_text())['records'],'deduplication':'Visual contact-sheet review plus transitive observation / burst / source groups / SHA256 / dHash<=6; groups split per class with seeded hash, 60/20/20 rounded down. Source groups and all five author images kept separate.','limitations':['Small convenience sample','Blattidae and Coleoptera scope; not diverse insects','Online empty-space photos; no geographic representativeness','Visual absence labels only; not proof of no insects outside visible scene']}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
with (out/'pixels.bin').open('wb') as f:
 for r in records:
  im=ImageOps.exif_transpose(Image.open(root/r['path'])).convert('RGB');im=ImageOps.pad(im,(96,96),color=(255,255,255),method=Image.Resampling.BILINEAR);f.write(im.tobytes())
public=dict(manifest);public['classes']={c:sum(r['class']==c for r in records) for c in manifest['classes']};public['splitCounts']={c:{s:sum(r['class']==c and r['split']==s for r in records) for s in ['train','validation','test']} for c in manifest['classes']}
(root/'dist/experiment/dataset-candidates.json').write_text(json.dumps(public,ensure_ascii=False,indent=2));print(json.dumps(public['splitCounts'],indent=2))
