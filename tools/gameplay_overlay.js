// Camada transparente dos vídeos de gameplay: título, selo de cada cena, moldura de madeira, legenda sincronizada, CTA, assinatura.
// Uso: node tools/gameplay_overlay.js dados.json pasta_saida fps
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
 const [dj,out,fpsS]=process.argv.slice(2);const D=JSON.parse(fs.readFileSync(dj));const fps=+fpsS;
 const raiz=path.resolve(__dirname,'..');
 const html=`<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../assets/base.css">
 <style>html,body{background:transparent!important;margin:0}
 #st{width:1080px;height:1920px;position:relative;overflow:hidden}
 .moldura{position:absolute;left:${D.gx-14}px;top:${D.gy-14}px;width:${D.gw+28}px;height:${D.gh+28}px;box-sizing:border-box;border:8px solid var(--wood);box-shadow:0 0 0 6px var(--orange),0 0 0 12px var(--wood),10px 14px 0 12px rgba(0,0,0,.35)}
 .topo{position:absolute;left:60px;right:150px;top:300px;display:flex;flex-direction:column;align-items:flex-start;gap:12px}
 .selo{font-family:Pix;font-size:58px;color:var(--gold);background:var(--wood);padding:6px 22px 10px;box-shadow:0 0 0 5px var(--orange);text-shadow:3px 3px 0 #000;text-transform:uppercase}
 .tit{font-family:Pix;font-size:84px;line-height:.95;color:#fff3cf;background:var(--wood);padding:12px 26px 16px;text-transform:uppercase;box-shadow:0 0 0 8px var(--orange),0 0 0 14px var(--wood)}
 .tit em{font-style:normal;color:var(--gold)}
 #leg{position:absolute;left:40px;right:130px;top:${D.gy+D.gh+30}px;display:flex;justify-content:center}
 #leg span{background:rgba(20,10,4,.88);color:#fff;font-family:Nun;font-weight:900;font-size:50px;line-height:1.12;padding:8px 20px 12px;box-shadow:0 0 0 5px var(--gold);text-align:center}
 #leg b{color:var(--gold)}#leg em{font-style:normal;color:#ff8a65}
 .cta{position:absolute;right:150px;top:${D.gy+30}px;background:var(--red);color:#fff;font-family:Nun;font-weight:900;font-size:40px;padding:10px 18px;box-shadow:0 0 0 5px var(--wood);transform-origin:right top}
 .cta b{color:var(--gold)}
 .capa{position:absolute;left:60px;right:60px;top:760px;display:flex;flex-direction:column;align-items:center;gap:22px}
 .capa .ct{font-family:Pix;font-size:132px;line-height:.92;text-align:center;color:#fff3cf;background:var(--wood);padding:26px 34px 34px;text-transform:uppercase;box-shadow:0 0 0 10px var(--orange),0 0 0 18px var(--wood),14px 20px 0 18px rgba(0,0,0,.4)}
 .capa .ct em{font-style:normal;color:var(--gold)}
 .capa .cs{font-family:Pix;font-size:56px;color:var(--gold);background:var(--red);padding:8px 24px 12px;box-shadow:0 0 0 6px var(--wood);text-shadow:3px 3px 0 #000;transform:rotate(-3deg)}
 .imgs{position:absolute;right:${1080-D.gx-D.gw+24}px;top:${D.gy+D.gh-330}px;display:flex;gap:18px;align-items:flex-end}
 .imgs img{height:300px;image-rendering:pixelated;filter:drop-shadow(6px 8px 0 rgba(0,0,0,.45));transform-origin:center bottom}
 .sig{position:absolute;left:${D.gx+14}px;top:${D.gy+10}px;font-family:Nun;font-weight:900;font-size:26px;opacity:.9;color:#fff;text-shadow:2px 2px 0 #000}
 .nativo .moldura,.nativo .topo{display:none!important}
 .nativo #leg{left:40px;right:130px;top:1170px}
 .nativo #leg span{background:none;box-shadow:none;padding:0;font-size:96px;line-height:1.02;color:#fff;letter-spacing:.5px;
   -webkit-text-stroke:14px #111;paint-order:stroke fill;text-shadow:0 8px 0 rgba(0,0,0,.45);text-transform:uppercase}
 .nativo #leg b{color:#ffd84a}.nativo #leg em{color:#ffd84a}
 .nativo .imgs{right:auto;left:50%;transform:translateX(-50%);top:430px}.nativo .imgs img{height:380px}
 .nativo .cta{right:auto;left:50%;transform-origin:center top;top:300px;margin-left:-180px}
 .nativo .sig{left:40px;top:1450px;font-size:30px}
 .nativo .capa{top:330px;left:40px;right:130px}
 .nativo .capa .ct{background:none;box-shadow:none;padding:0;font-family:Nun;font-weight:900;font-size:118px;line-height:1.0;color:#fff;-webkit-text-stroke:18px #111;paint-order:stroke fill;text-shadow:0 10px 0 rgba(0,0,0,.45)}
 .nativo .capa .ct em{color:#ffd84a}
 .nativo .capa .cs{display:none}
 .nativo .cta{font-size:46px;padding:12px 24px;margin-left:-230px}
 </style></head><body><div id="st" class="${D.estilo||''}"><div class="moldura"></div><div class="topo"><span class="selo" id="selo"></span><span class="tit" id="tit"></span></div>
 <div class="capa" id="capa"><span class="ct" id="ct"></span><span class="cs">Stardew Valley</span></div><div id="leg"></div><div class="cta" id="cta" style="display:none"></div><div class="imgs" id="imgs"></div><div class="sig">@segredosdovalley</div></div></body></html>`;
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 const arq=path.join(raiz,'tools','_overlay.html');fs.writeFileSync(arq,html);await p.goto('file://'+arq);await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(D=>{window.D=D;const esc=w=>w.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const ease=x=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
  document.getElementById('tit').innerHTML=esc(D.titulo).replace(/\*([^*]+)\*/g,'<em>$1</em>');document.getElementById('ct').innerHTML=document.getElementById('tit').innerHTML;
  window.desenha=t=>{const naCapa=t<(D.capa||0);document.getElementById('capa').style.display=naCapa?'flex':'none';document.querySelector('.topo').style.display=naCapa?'none':'flex';document.getElementById('leg').style.visibility=naCapa?'hidden':'visible';
   const c=D.cenas.find(x=>t>=x.S&&t<x.S+x.L)||D.cenas[D.cenas.length-1];
   const s=document.getElementById('selo');s.textContent=c.selo||'Stardew Valley';const k=ease((t-c.S)/0.3);s.style.transform=`scale(${0.6+0.4*k})`;s.style.opacity=k;
   const ct=document.getElementById('cta');if(c.cta&&t>c.fala+c.dur*0.5){ct.style.display='block';ct.innerHTML=esc(c.cta).replace(/([A-ZÀ-Ú]{4,})/g,'<b>$1</b>');ct.style.transform=`scale(${ease((t-c.fala-c.dur*0.5)/0.25)})`}else ct.style.display='none';
   const im=document.getElementById('imgs');const key=(c.img||[]).join('|');if(im.dataset.k!==key){im.dataset.k=key;im.innerHTML=(c.img||[]).map(u=>'<img src="file://'+u+'">').join('')}
   [...im.children].forEach((x,i)=>{const kk=ease((t-c.S-0.15-i*0.25)/0.3);x.style.transform=`scale(${kk})`;});
   const L=[...D.leg].reverse().find(x=>t>=x.ini&&t<x.fim);document.getElementById('leg').innerHTML=L?'<span>'+L.p.map(x=>(t>=x.t0&&t<x.t1)?'<b>'+esc(x.w)+'</b>':(/^[A-ZÀ-Ú]{4,}[!?.,]*$/.test(x.w)?'<em>'+esc(x.w)+'</em>':esc(x.w))).join(' ')+'</span>':'';}},D);
 const n=Math.ceil(D.total*fps);
 for(let f=0;f<n;f++){await p.evaluate(async t=>{desenha(t);await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r})))},f/fps);await p.screenshot({path:`${out}/${String(f).padStart(5,'0')}.png`,omitBackground:true})}
 await b.close();console.log('camada',n,'quadros');
})();
