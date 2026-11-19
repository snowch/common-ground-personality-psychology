/* Original concept figures, shared rendering rules and per-course semantic plans. */
function wrapFigureText(text,limit=24){const words=String(text).split(/\s+/),lines=[];let line='';for(const word of words){if(line&&line.length+word.length+1>limit){lines.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)lines.push(line);return lines;}
function figureText(x,y,text,size=20,color='#19394D',limit=24,anchor='middle'){
 const lines=wrapFigureText(text,limit);return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-family="CourseSans,Arial,sans-serif" fill="${color}">${lines.map((line,i)=>`<tspan x="${x}" dy="${i?size*1.32:0}">${esc(line)}</tspan>`).join('')}</text>`;
}
function figurePanel(x,y,w,h,lines,color='#216B88'){
 return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#FFF" stroke="${color}" stroke-width="1.8"/>`+lines.map((line,i)=>figureText(x+w/2,y+38+i*54,line,i?18:21,i?'#4B6172':color,w<230?20:34)).join('');
}
function figureArrow(x,y,length=32){return `<path d="M${x} ${y}v${length-8}" stroke="#7058A3" stroke-width="2"/><path d="m${x-5} ${y+length-13} 5 8 5-8" fill="none" stroke="#7058A3" stroke-width="2"/>`;}
function renderLessonFigure(model,key){
 let body=figureText(260,36,model.title,23,'#19394D',38);
 if(model.type==='compare')body+=figurePanel(30,115,220,216,model.left,'#7058A3')+figurePanel(270,115,220,216,model.right,'#216B88');
 if(['rows','flow'].includes(model.type)){
  model.items.forEach((item,i)=>{const y=93+i*103;body+=`<rect x="42" y="${y}" width="436" height="80" rx="12" fill="#FFF" stroke="${i===0?'#216B88':'#A6BCCB'}" stroke-width="1.7"/>`+figureText(62,y+29,item[0],19,'#216B88',38,'start')+figureText(62,y+58,item[1],18,'#19394D',39,'start');if(model.type==='flow'&&i<model.items.length-1)body+=figureArrow(260,y+81,21);});
 }
 if(model.type==='branch'){
  body+=figurePanel(105,101,310,78,[model.start]);
  body+=`<path d="M260 181v25M140 207H380M140 207v25M380 207v25" fill="none" stroke="#A6BCCB" stroke-width="2" stroke-dasharray="6 5"/>`;
  body+=figurePanel(30,238,220,113,[model.left],'#7058A3')+figurePanel(270,238,220,113,[model.right],'#216B88');
  body+=figureText(260,394,'Possible accounts to investigate',16,'#4B6172',40);
 }
 if(model.type==='frequencies'){
  body+=figurePanel(30,98,220,151,['10 faulty','8 test positive'],'#7058A3')+figurePanel(270,98,220,151,['90 without fault','9 test positive'],'#216B88');
  body+=`<path d="M140 252v20H380v-20M260 272v24" fill="none" stroke="#A6BCCB" stroke-width="2"/>`+figurePanel(70,301,380,105,['17 positive results','8 are real faults']);
  body+=figureText(260,438,'Invented teaching counts · 100 devices',15,'#4B6172',50);
 }
 if(model.type==='dimensions'){
  ['Extraversion','Agreeableness','Conscientiousness','Negative emotionality','Open-mindedness'].forEach((term,i)=>{const y=106+i*61;body+=figureText(36,y,term,19,'#19394D',40,'start')+`<path d="M38 ${y+22}H482" stroke="#A6BCCB" stroke-width="4" stroke-linecap="round"/><circle cx="38" cy="${y+22}" r="4" fill="#216B88"/><circle cx="482" cy="${y+22}" r="4" fill="#7058A3"/>`;});
  body+=figureText(260,443,'Unscored dimensions, not a person’s results',15,'#4B6172',50);
 }
 if(model.type==='distribution'){
  body+=`<path d="M50 337H478" stroke="#A6BCCB" stroke-width="2"/><path d="M58 336C128 336 120 311 163 240S219 126 260 125S318 180 351 245S399 334 472 336" fill="#D9E8ED" stroke="#216B88" stroke-width="3"/>`;
  body+=figureText(260,385,'State expression across occasions',19)+figureText(260,421,'Conceptual sketch · not measured data',15,'#4B6172',50);
 }
 if(model.type==='overlap'){
  body+=`<path d="M34 338H486" stroke="#A6BCCB" stroke-width="2"/><path d="M45 337C90 337 101 145 207 145S310 336 420 337" fill="#DDD6EA" fill-opacity=".65" stroke="#7058A3" stroke-width="3"/><path d="M103 337C157 337 172 163 286 163S399 336 480 337" fill="#D9E8ED" fill-opacity=".6" stroke="#216B88" stroke-width="3"/>`;
  body+=figureText(260,385,'Variation exists within both groups',19)+figureText(260,423,'Conceptual sketch · not population data',15,'#4B6172',50);
 }
 return `<svg viewBox="0 0 520 460" role="img" data-diagram="${esc(key)}" aria-label="${esc(model.caption)}">${body}</svg>`;
}
const visualCatalog=Object.fromEntries(Object.entries(VISUAL_MODELS).map(([key,model])=>[key,{key,title:model.title,caption:model.caption,terms:[],render:()=>renderLessonFigure(model,key)}]));
const visualLessons=Object.fromEntries(COURSE.flatMap(c=>c.slides.filter(s=>s.visual).map(s=>[s.id,[visualCatalog[s.visual]]])));
function diagramCaption(chapter,slide){return visualLessons[slide.id]?.[0].caption||'A fictional scene at the Common Ground repair café.';}
function scene(mode='room',stage='story',slideId=''){return visualLessons[slideId]?.[0].render()||workshopScene();}
