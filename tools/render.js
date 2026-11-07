// Uso: node tools/render.js posts/001-segredos
// Gera um PNG 1080x1920 por <section class="slide"> e uma folha de contato.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const dir=path.resolve(process.argv[2]);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+dir+'/slides.html');await p.evaluate(()=>document.fonts.ready);
const ids=await p.$$eval('section.slide',s=>s.map(x=>x.id));
for(const [i,id] of ids.entries()){await (await p.$('#'+id)).screenshot({path:`${dir}/slides/${String(i+1).padStart(2,'0')}.png`});}
// checagem de área segura: nada importante fora de y 260–1500 e x > 950
const bad=await p.$$eval('section.slide',ss=>ss.flatMap(s=>{const o=s.getBoundingClientRect();return [...s.querySelectorAll('.card,.bridge')].map(e=>{const r=e.getBoundingClientRect();return {id:s.id,c:e.className,top:r.top-o.top,bottom:r.bottom-o.top,right:r.right-o.left}}).filter(r=>r.top<260||r.bottom>1540||r.right>950)}));
const over=await p.$$eval('.card',cs=>cs.filter(c=>c.scrollHeight>c.clientHeight+1).map(c=>c.parentElement.id));
console.log('vazando do quadro:',over.length?over:'nenhum');
console.log(ids.length+' slides', bad.length?bad:'área segura ok');await b.close()})();
