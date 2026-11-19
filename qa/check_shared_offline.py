"""Validate two complete course saves on the same origin without cache collisions."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
RESULTS=Path(os.environ.get('COURSE_QA_RESULTS_DIR',R/'qa'));RESULTS.mkdir(parents=True,exist_ok=True)
PATHS={'cognitive':os.environ.get('COURSE_COGNITIVE_PATH','cognitive'),'personality':os.environ.get('COURSE_PERSONALITY_PATH','personality')}
BASE=os.environ.get('COURSE_FAMILY_BASE_URL','http://127.0.0.1:8910').rstrip('/')
async def main():
 async with async_playwright()as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);ctx=await b.new_context();tabs={}
  cognitive_size=None
  for name in ['cognitive','personality']:
   page=await ctx.new_page();tabs[name]=page;await page.goto(BASE+'/'+PATHS[name]+'/offline.html');await page.locator('#offlineSave:not([disabled])').wait_for();await page.locator('#offlineSave').click();await page.locator('#offlineContinue').wait_for(timeout=180000)
   if name=='cognitive':cognitive_size=await page.locator('#offlineSize').inner_text()
   else:assert await tabs['cognitive'].locator('#offlineSize').inner_text()==cognitive_size,'Other course progress messages changed the saved course UI'
  await ctx.set_offline(True)
  for name,page in tabs.items():
   await page.goto(BASE+'/'+PATHS[name]+'/#chapter-1-slide-1');await page.locator('#read').click();await page.wait_for_function('audioPlayer&&audioPlayer.currentTime>.1');await page.locator('#stop').click()
  await tabs['personality'].goto(BASE+'/'+PATHS['personality']+'/offline.html');await tabs['personality'].locator('#offlineContinue').wait_for()
  await tabs['cognitive'].goto(BASE+'/'+PATHS['cognitive']+'/offline.html');await tabs['cognitive'].locator('#offlineContinue').wait_for();await tabs['cognitive'].locator('#offlineRemove').click();await tabs['cognitive'].wait_for_function('document.querySelector("#offlineRemove").hidden')
  await tabs['personality'].wait_for_timeout(500);assert not await tabs['personality'].locator('#offlineContinue').is_hidden(),'Removing another course changed this course status'
  await tabs['personality'].goto(BASE+'/'+PATHS['personality']+'/offline.html');await tabs['personality'].locator('#offlineContinue').wait_for();assert 'Ready to use offline'in await tabs['personality'].locator('#offlineState').inner_text()
  result=dict(shared_origin_offline_saves='passed',both_courses_narration_offline='passed',removing_one_preserves_the_other='passed',cross_course_progress_messages_isolated='passed')
  (RESULTS/'shared-offline-results.json').write_text(json.dumps(result,indent=2)+'\n')
  print(json.dumps(result,indent=2));await b.close()
asyncio.run(main())
