// Uso: node tools/render.js posts/001-segredos [posts/002-...]
// Gera slides/01.png... (1080x1920) e confere: texto vazando do quadro, frase-ponte cortada e área segura.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const arg of process.argv.slice(2)){const dir=path.resolve(arg);fs.mkdirSync(dir+'/slides',{recursive:true});
 const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+dir+'/slides.html');await p.evaluate(()=>document.fonts.ready);
 const ids=await p.$$eval('section.slide',s=>s.map(x=>x.id));
 for(const [i,id] of ids.entries()) await (await p.$('#'+id)).screenshot({path:`${dir}/slides/${String(i+1).padStart(2,'0')}.png`});
 const probs=await p.$$eval('section.slide',ss=>ss.flatMap(s=>{const o=s.getBoundingClientRect();const out=[];
  s.querySelectorAll('.card').forEach(c=>{if(c.scrollHeight>c.clientHeight+1)out.push(s.id+': texto vazando do quadro')});
  s.querySelectorAll('.bridge').forEach(e=>{if(e.scrollWidth>e.clientWidth+1)out.push(s.id+': frase-ponte cortada')});
  s.querySelectorAll('.card *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.right-o.left>942||r.left-o.left<78))out.push(s.id+': saiu pela lateral: '+e.textContent.slice(0,30))});
  return out}));
 console.log(path.basename(dir)+': '+ids.length+' slides · '+(probs.length?'PROBLEMAS: '+[...new Set(probs)].join(' | '):'tudo ok'));await p.close()}
await b.close()})();
