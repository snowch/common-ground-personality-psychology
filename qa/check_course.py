"""Check all lesson states, evidence disclosures, figures and written decisions."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];C=json.loads((R/'course.json').read_text());BASE=os.environ.get('COURSE_BASE_URL','http://127.0.0.1:8877').rstrip('/');AXE=Path(os.environ.get('AXE_SCRIPT','/tmp/common-ground-axe.min.js'))
async def main():
 errors=[];audited=0;figures=0;feedbacks=0
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await browser.new_page(viewport={'width':390,'height':1000},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/');await page.add_script_tag(path=str(AXE))
  for c in C:
   for s in c['slides']:
    await page.evaluate('(h)=>location.hash=h','chapter-'+str(c['number'])+'-slide-'+s['id'].split('s')[1].lstrip('0'))
    await page.wait_for_function('(x)=>document.querySelector("#slideTitle")?.textContent===x',arg=s['title'])
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),s['id']
    if s.get('research'):
     d=page.locator('.lesson-research');assert await d.get_attribute('open')is None
     assert await page.locator('.chapter-reading').get_attribute('open')is None
     await d.locator('summary').focus();await page.keyboard.press('Enter');assert await page.locator('.research-content').is_visible()
     assert await page.locator('.research-content a').count()==len(s['research']['sources'])
     bad=await page.locator('.slide-art>svg').evaluate('''svg=>{const box=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<-.5||b.y<-.5||b.x+b.width>box.width+.5||b.y+b.height>box.height+.5}).map(t=>t.textContent)}''')
     assert not bad,(s['id'],bad);figures+=1
    if 'quiz'in s:
     q=s['quiz']
     for i,text in enumerate(q['feedback']):
      await page.locator('[data-answer="'+str(i)+'"]').click()
      if q.get('reasoningPrompt'):await page.locator('#decisionReasoning').fill('Compare relevant evidence; retain uncertainty. <script>unsafe</script>')
      await page.locator('#checkChoice').click();assert text in await page.locator('.feedback').inner_text();feedbacks+=1
     if q.get('reasoningPrompt'):
      await page.reload();assert '<script>unsafe</script>'in await page.locator('#decisionReasoning').input_value()
      assert await page.locator('script').filter(has_text='unsafe').count()==0
      await page.add_script_tag(path=str(AXE))
    if s['kind']=='recall':
     assert not await page.locator('.answers').count();await page.locator('#reveal').click();answer_text=await page.locator('.answers').inner_text();assert all(x in answer_text for x in s['answers'])
    if s.get('research')or s.get('quiz'):
     issues=await page.evaluate('''async()=>{const r=await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))}''')
     assert not issues,(s['id'],issues);audited+=1
  await page.goto(BASE+'/#case');assert await page.locator('#case-story').inner_text()==json.loads((R/'learning-check.json').read_text())['caseTitle']
  await page.goto(BASE+'/visual-guide.html');assert await page.locator('.visual-card').count()==40
  await page.goto(BASE+'/study-guide.html');assert await page.locator('.research-topic').count()==40
  assert not errors,errors;await browser.close()
 result=dict(chapters=10,pages=90,expanded_research=figures,svg_text_bounds='passed',feedback_variants=feedbacks,axe_states=audited,writing_restore_and_escaping='passed',case_and_companions='passed',js_errors=errors)
 (R/'qa/course-browser-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':asyncio.run(main())
