"""Synchronize review files and recording scripts from canonical course.json."""
from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
c=json.loads((R/'course.json').read_text());old={x['id']:x for x in json.loads((R/'production/af-heart/scenes.json').read_text())};scenes=[]
def scene(id,text,title):
 if id in old and old[id]['text']==text:return old[id]
 say=re.sub(r"Maya(?:[’']s)?",lambda m:'['+m[0]+'](/'+('mˈaɪəz'if len(m[0])>4 else 'mˈaɪə')+'/)',text)
 say=re.sub(r'\b[Rr]ank-order\b',lambda m:'['+m[0]+'](/ɹˈæŋk ˈɔːɹdɚ/)',say).replace('\n\n',' [pause 0.65] ')
 return dict(id=id,step=title,text=text,say=say)
for chapter in c:
 for s in chapter['slides']:
  title=f"Chapter {chapter['number']}: {s['title']}";scenes.append(scene(s['id'],s['text'],title))
  if s.get('quiz'):
   for i,text in enumerate(s['quiz']['feedback']):scenes.append(scene(s['id']+f'-feedback-{i}',text,title+f': feedback {i+1}'))
  if s.get('answers'):scenes.append(scene(s['id']+'-answers','\n\n'.join(s['answers']),title+': suggested answers'))
outputs={'teaching-pages.json':{str(x['number']):[s for s in x['slides']if s.get('research')]for x in c},'transfer-exercises.json':{str(x['number']):next(s['quiz']for s in x['slides']if s['kind']=='transfer')for x in c},'production/af-heart/scenes.json':scenes}
for name,data in outputs.items():
 if args.check:assert json.loads((R/name).read_text())==data,name
 else:(R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
text='\n\n'.join(s['id']+' '+s['step']+'\n'+s['text'] for s in scenes)+'\n'
if args.check:assert (R/'narration-script.txt').read_text()==text
else:(R/'narration-script.txt').write_text(text)
print('Recording and review sources are synchronized.' if args.check else 'Updated recording and review sources. Regenerate changed speech before publishing.')
