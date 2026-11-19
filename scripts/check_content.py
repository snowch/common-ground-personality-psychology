"""Validate the curriculum, assessment alignment and narration before publishing."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
course=json.loads((R/'course.json').read_text());teaching=json.loads((R/'teaching-pages.json').read_text());transfers=json.loads((R/'transfer-exercises.json').read_text());glossary=json.loads((R/'glossary.json').read_text());evidence=json.loads((R/'course-evidence.json').read_text());case=json.loads((R/'learning-check.json').read_text());models=json.loads((R/'visual-models.json').read_text());scenes=json.loads((R/'production/af-heart/scenes.json').read_text())
assert len(course)==10 and [c['number']for c in course]==list(range(1,11))
assert len({c['title']for c in course})==10 and len({c['objective']for c in course})==10
expected={};steps=0;research=0;decisions=0
for c in course:
 n=c['number'];assert len(c['slides'])==9 and len(c['quizzes'])==2 and len(c['recall'])==len(c['answers'])==2
 assert len(glossary[str(n)])>=3 and len(evidence[str(n)]['sources'])>=2
 for s in c['slides']:
  steps+=1;assert re.fullmatch(fr'c{n:02d}s(?:0[1-8]|03b)',s['id'])
  assert s['id']not in expected;expected[s['id']]=s['text'];assert len(s['text'].split())<210
  if s['kind']in ['concept','evidence']:
   research+=1;assert s['research']['sources']
   assert all(section['heading'] and section['text'] and section['text'] not in s['text'] for section in s['research']['sections']),s['id']
   assert s['visual']in models and models[s['visual']]['caption']
  if 'quiz'in s:
   decisions+=1;q=s['quiz'];
   assert q['prompt']in s['text'] and all(option in s['text']for option in q['options']),'Spoken choices must match the displayed choices.'
   assert len(q['options'])==len(q['feedback'])==3 and q['correct']in [0,1,2]
   assert len(set(q['options']))==3 and len(set(q['feedback']))==3
   if s['kind']=='transfer':assert q['reasoningPrompt']and q['revision']and q==transfers[str(n)]
   for i,text in enumerate(q['feedback']):expected[s['id']+f'-feedback-{i}']=text
  if s['kind']=='recall':expected[s['id']+'-answers']='\n\n'.join(s['answers'])
 assert teaching[str(n)]==[s for s in c['slides']if s.get('research')]
assert steps==90 and research==40 and decisions==20 and len(models)==40 and len(expected)==160
core=next(s for c in course for s in c['slides']if s['id']=='c02s03')
for term in ['Extraversion','Agreeableness','Conscientiousness','Negative emotionality','Open-mindedness']:assert term.lower()in core['text'].lower() and any(term.lower()in point.lower()for point in core['points'])
assert {s['id']:s['text']for s in scenes}==expected
for scene in scenes:
 say=re.sub(r'\[pause(?:\s+[\d.]+)?\]',' ',scene['say']);say=re.sub(r'\[([^\]]+)\]\(/[^)]*/\)',r'\1',say)
 assert ' '.join(say.split())==' '.join(scene['text'].split()),scene['id']
assert set(range(1,11))=={n for task in case['tasks']for n in task['chapters']}
assert len(case['tasks'])>=5 and len(case['rubric'])>=3
assert 'common-ground-v1'not in (R/'template.html').read_text(),'Must not overwrite the social course progress.'
if (R/'audio/manifest.json').exists():
 manifest=json.loads((R/'audio/manifest.json').read_text());assert {x['id']for x in manifest['clips']}==set(expected)
 for clip in manifest['clips']:
  path=R/clip['file'];assert path.stat().st_size==clip['bytes']and hashlib.sha256(path.read_bytes()).hexdigest()==clip['sha256']
 report=R/'qa/narration-asr.json'
 assert report.exists(),'Complete independent speech screening before publishing.'
 screened={x['id']:x for x in json.loads(report.read_text())['clips']}
 assert set(screened)==set(expected),'Every clip needs an independent transcript screen.'
 assert all(screened[id]['expected']==text for id,text in expected.items()),'Speech review must match the current scripts.'
 review=json.loads((R/'qa/narration-review.json').read_text())
 assert not review['unresolved']
 assert {id for id,row in screened.items()if row['flags']}<=set(review['resolved'])
 assert all(review['encoded_hashes'][x['id']]==x['sha256'] for x in manifest['clips']),'Review hashes must match final audio.'
print(json.dumps(dict(chapters=10,pages=steps,independent_teaching_pages=research,concept_figures=len(models),decisions=decisions,recording_scripts=len(expected),written_transfer_cases=10,final_case_tasks=len(case['tasks']),aligned_source_checks='passed'),indent=2))
