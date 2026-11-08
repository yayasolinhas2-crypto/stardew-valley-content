// Guia de 1 página: node tools/guia.js posts/016-presente-do-pet → slides/01.png (1080x1920)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const a of process.argv.slice(2)){const d=path.resolve(a);fs.mkdirSync(d+'/slides',{recursive:true});
 const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+d+'/slides.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 const fora=await p.$$eval('.placa,.passos,.faixa,.grade2,.grade3',e=>e.filter(x=>{const r=x.getBoundingClientRect();return r.top<170||r.bottom>1500||r.right>952}).map(x=>x.className));
 await (await p.$('.pg')).screenshot({path:d+'/slides/01.png'});
 console.log(path.basename(d),fora.length?'⚠ fora da área segura: '+fora.join(', '):'área segura ok');await p.close()}
await b.close()})();
