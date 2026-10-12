from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[1];out=root/'dist/author';out.mkdir(exist_ok=True)
source=Path('/Users/bluefairy/Documents/研一/课程/HCI/pre');names=[('9103','排水口','Drain'),('9101','瓷砖与缝隙','Tiles and seams'),('9102','墙角与天花板','Wall and ceiling corner'),('9105','空调、电线与窗帘','Air conditioner, cable and curtain'),('9104','厨房水槽','Kitchen sink')];records=[]
for n,zh,en in names:
 f=source/f'IMG_{n}.JPG';im=ImageOps.exif_transpose(Image.open(f)).convert('RGB');size=im.size;im.thumbnail((768,768));p=out/f'{n}.jpg';im.save(p,quality=90)
 records.append({'id':f'author-{n}','title':[zh,en],'url':f'author/{n}.jpg','originalFilename':f.name,'originalSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'originalDimensions':size,'dimensions':im.size,'photographer':['作品作者（用户提供）','Project author (user supplied)'],'rights':['作者提供并授权用于本课程项目','Supplied and authorized by the author for this course project'],'licenseCode':'author-project-permission','permissionEvidence':'User supplied these five photos on 2026-10-12 for use in the presentation website. No general public reuse license asserted.','role':'dream-and-demonstration-only','groupId':'author-session-9101-9105','split':'display-only','usedForTraining':False,'label':'no visible cockroach at review resolution','reviewNote':'Visual review of submitted photos; not proof of insect absence outside the visible scene. Small mark on 9102 is ambiguous, not labeled ground-truth insect-free test.'})
(out/'manifest.json').write_text(json.dumps({'version':'author-inputs-2026-10-12','records':records},ensure_ascii=False,indent=2))
m=json.loads((root/'data/cockroach-candidates/manifest.json').read_text());sheet=Image.new('RGB',(1000,8*150),'white');d=ImageDraw.Draw(sheet)
for i,r in enumerate(m['records']):
 im=Image.open(root/'data/cockroach-candidates'/r['path']).convert('RGB');im.thumbnail((158,120));x=(i%6)*166;y=(i//6)*150;sheet.paste(im,(x,y));d.text((x,y+121),f"{i} {r['id'][11:]}",fill='black')
sheet.save('/tmp/insect-review.jpg')
print('Author images imported; all excluded from training')
