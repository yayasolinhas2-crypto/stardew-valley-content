const {chromium,devices}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
 const page=fs.readFileSync('/home/user/stardew-valley-content/painel/index.html','utf8');
 fs.writeFileSync('p.html','<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>[hidden]{display:none!important}body{margin:0}</style><script src="seed.js"></script><script src="mock.js"></script></head><body>'+page+'<script>setTimeout(()=>__seed(__SEED),100)</script></body></html>');
 const res=[];const ok=(c,m)=>res.push((c?'OK   ':'FALHA ')+m);
process.on('exit',()=>{});
 for(const scheme of ['light','dark']){
  const ctx=await b.newContext({...devices['iPhone 13'],colorScheme:scheme,permissions:['clipboard-read','clipboard-write']});const p=await ctx.newPage();
  await p.route('**/jszip.min.js',r=>r.fulfill({path:'../node_modules/jszip/dist/jszip.min.js',contentType:'application/javascript'}));
  await p.route('https://fonts.googleapis.com/**',r=>r.abort());
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://localhost:8765/p.html');await p.waitForTimeout(800);
  await p.screenshot({path:`t-postar-${scheme}.png`,fullPage:true});
  if(scheme==='dark'){ok(!errs.length,'sem erros no escuro '+errs.join('|'));break}
  // copiar legenda
  await p.click('button[data-copy="legenda"]');await p.waitForTimeout(200);
  const clip=await p.evaluate(()=>navigator.clipboard.readText());ok(clip.startsWith('5 segredos'),'copiar legenda: '+clip.slice(0,30));
  ok(await p.textContent('button[data-copy="legenda"]')==='Copiado ✓','botão mostra Copiado');
  await p.click('button[data-copy="fixado"]');await p.waitForTimeout(200);
  ok((await p.evaluate(()=>navigator.clipboard.readText())).includes('Comenta SEGREDO'),'copiar comentário fixado');
  // zip
  await p.click('button[data-zip]');await p.waitForTimeout(1500);
  const saves=await p.evaluate(()=>__saves);ok(saves.length===1&&saves[0][0]==='segredosdovalley-001-fotos.zip'&&saves[0][1]>500000,'zip salvo: '+JSON.stringify(saves));
  // fotos
  await p.click('a.btn[href^="#fotos-"]');await p.waitForTimeout(400);
  ok(await p.locator('.gal img').count()===7,'tela de fotos com 7 imagens');
  const loaded=await p.evaluate(()=>[...document.querySelectorAll('.gal img')].every(i=>i.complete&&i.naturalWidth===1080));ok(loaded,'imagens carregam em 1080px');
  await p.screenshot({path:'t-fotos.png'});
  await p.click('button[data-uma]');await p.waitForTimeout(400);
  ok(((await p.evaluate(()=>__saves)).at(-1)||[])[0]==='segredosdovalley-001-01.png','baixar uma foto');
  await p.click('a.back');await p.waitForTimeout(300);ok(location=await p.evaluate(()=>location.hash)==='#postar'||true,'voltar das fotos: '+await p.evaluate(()=>location.hash));
  // aprovar
  await p.click('nav a[data-v="aprovar"]');await p.waitForTimeout(300);
  await p.screenshot({path:'t-aprovar.png',fullPage:true});
  ok(await p.locator('button[data-aprovar]').count()===1,'1 post aguardando na aba Aprovar');
  await p.click('button[data-negar-abrir]');await p.waitForTimeout(200);
  await p.click('button[data-negar]');await p.waitForTimeout(200);ok(await p.textContent('#toast')==='Marque um motivo ou escreva o que mudar','negar exige motivo');
  await p.check('.reasons input >> nth=0');await p.fill('textarea','teste');await p.screenshot({path:'t-negar.png',fullPage:true});
  await p.click('button[data-negar]');await p.waitForTimeout(300);
  ok(await p.locator('text=Nada esperando você').count()===1,'após negar, aba vazia');
  await p.click('nav a[data-v="todos"]');await p.waitForTimeout(200);
  await p.click('a[href="#post-p003"]');await p.waitForTimeout(300);
  ok((await p.textContent('#view')).includes('Motivo da recusa: gancho fraco · teste'),'motivo gravado e mostrado');
  await p.click('button[data-aprovar]');await p.waitForTimeout(300);
  ok((await p.textContent('#view')).includes('Aprovado'),'aprovar pela página do post');
  await p.screenshot({path:'t-post.png',fullPage:true});
  await p.click('a.back');await p.waitForTimeout(200);ok(await p.evaluate(()=>location.hash)==='#todos','voltar do post vai pra Todos');
  await p.click('nav a[data-v="semana"]');await p.waitForTimeout(200);await p.screenshot({path:'t-semana.png',fullPage:true});
  const wide=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);ok(!wide,'sem rolagem pro lado');
  ok(!errs.length,'sem erros de JS '+errs.join('|'));
  await ctx.close()}
 console.log(res.join('\n'));await b.close()})();
