"""Build a pre-training candidate manifest. Never train from unreviewed records."""
from pathlib import Path
import json,urllib.request,urllib.parse,time,hashlib,datetime,re
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'data/cockroach-candidates';(out/'images').mkdir(parents=True,exist_ok=True)
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'NeuralNetworkDreamsEducationalAudit/1.0'})
 with urllib.request.urlopen(req,timeout=40) as r:return r.read()
records=[]
for category,taxon in [('cockroach',82232),('other_insect',47208)]:
 query=urllib.parse.urlencode({'taxon_id':taxon,'photos':'true','photo_license':'cc0,cc-by','quality_grade':'research','per_page':60,'order_by':'id','order':'asc'})
 observations=json.loads(fetch('https://api.inaturalist.org/v1/observations?'+query))['results'];time.sleep(1.1)
 for o in observations:
  if sum(r['class']==category for r in records)>=24:break
  p=next((p for p in o['photos'] if p.get('license_code') in ['cc0','cc-by'] and not p.get('hidden') and not p.get('flags')),None)
  if not p:continue
  name=f"{category}-{o['id']}-{p['id']}.jpg";url=p['url'].replace('/square.','/medium.')
  try:
   f=out/'images'/name
   if not f.exists():f.write_bytes(fetch(url));time.sleep(.15)
   im=Image.open(f).convert('RGB');gray=im.resize((9,8)).convert('L');pixels=list(gray.getdata());bits=sum((pixels[y*9+x]>pixels[y*9+x+1])<<(y*8+x) for y in range(8) for x in range(8))
   attribution=p['attribution'];photographer=re.sub(r'^\(c\)\s*','',attribution).split(', some rights')[0]
   if 'uploaded by ' in photographer:photographer=photographer.split('uploaded by ',1)[1]
   records.append({'id':f"inat-photo-{p['id']}",'class':category,'path':'images/'+name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'dhash':f'{bits:016x}','photographer':photographer,'attribution':attribution,'licenseCode':p['license_code'],'licenseEvidenceURL':f"https://www.inaturalist.org/photos/{p['id']}",'observation':o['id'],'originalURL':f"https://www.inaturalist.org/observations/{o['id']}",'downloadURL':url,'taxon':o['taxon']['name'],'taxonId':o['taxon']['id'],'observerId':o['user']['id'],'observedOn':o.get('observed_on'),'burstGroup':f"{o['user']['id']}:{o.get('observed_on')}:{o['taxon']['id']}",'dimensions':list(im.size),'displayAllowed':True,'usedForDisplay':False,'usedForTraining':False,'reviewStatus':'pending visual and near-duplicate review','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()})
   print(category,len([r for r in records if r['class']==category]),flush=True)
  except Exception as e:print('Skipped',o['id'],str(e),flush=True)
parents=list(range(len(records)))
def find(i):
 while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
 return i
for i,a in enumerate(records):
 for j,b in enumerate(records[:i]):
  near=(int(a['dhash'],16)^int(b['dhash'],16)).bit_count()<=6
  if a['observation']==b['observation'] or a['burstGroup']==b['burstGroup'] or a['sha256']==b['sha256'] or near:parents[find(i)]=find(j)
for i,r in enumerate(records):
 group='candidate-group-'+records[find(i)]['id'];n=int(hashlib.sha256(('seed5316/'+group).encode()).hexdigest()[:8],16)%10
 r['groupId']=group;r['split']='train' if n<6 else 'validation' if n<8 else 'test'
manifest={'version':'cockroach-candidates-v0-2026-10-10','status':'incomplete; not a training dataset yet','seed':5316,'scope':'Blattidae positive candidates; Coleoptera negative candidates; globally sourced, not representative of Guangdong','deduplication':'one photo per observation; union by observation, observer-date-taxon burst group, identical SHA-256 or dHash Hamming <=6; split by connected component; manual near-burst review still required','splitPolicy':'deterministic group hash 60/20/20, provisional; final Dream inputs excluded from all training','sourceAPI':'https://api.inaturalist.org/v1/observations','missing':['author-owned no-insect spaces','author-owned Guangdong Dream inputs kept separate','manual label/license/near-duplicate review','broader other-insect coverage'],'records':records}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print('Manifest saved:',len(records),flush=True)
summary={'version':manifest['version'],'status':'candidate','classes':{c:len([r for r in records if r['class']==c]) for c in ['cockroach','other_insect','empty_space']},'splitCounts':{c:{s:sum(r['class']==c and r['split']==s for r in records) for s in ['train','validation','test']} for c in ['cockroach','other_insect','empty_space']},'records':[{k:r[k] for k in ['id','class','photographer','attribution','licenseCode','licenseEvidenceURL','observation','originalURL','sha256','groupId','split','usedForTraining','usedForDisplay','reviewStatus']} for r in records]}
(root/'dist/experiment/dataset-candidates.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
