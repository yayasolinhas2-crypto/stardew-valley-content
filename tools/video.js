// Uso:
//   node tools/video.js posts/001-segredos [fps]                      → video.mp4 (tempo original)
//   node tools/video.js posts/001-segredos 30 --quadros 1.0,5.5       → PNGs de conferência
//   node tools/video.js posts/001-segredos 30 --narr duracoes.json     → video-mudo-narr.mp4 + tempos.json
// --narr: {"duracoes":[s por cena]} — cada cena dura no mínimo LEAD+fala+TAIL; a animação congela no fim da cena até a fala acabar.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const LEAD=0.2,TAIL=0.35;
(async()=>{const dir=path.resolve(process.argv[2]);const fps=+(process.argv[3]||30);
 const arg=k=>{const i=process.argv.indexOf(k);return i>0?process.argv[i+1]:null};
 const so=arg('--quadros')?arg('--quadros').split(',').map(Number):null;const narr=arg('--narr');
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+dir+'/video.html');await p.evaluate(()=>document.fonts.ready);
 const stage=await p.$('#stage');
 const espera=()=>p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
 if(so){for(const t of so){await p.evaluate(t=>seek(t),t);await espera();await stage.screenshot({path:`${dir}/quadro-${t}.png`})}await b.close();return}
 const dur=await p.evaluate(()=>DUR);
 // mapa de tempo: saída → tempo original
 let mapa=t=>t,total=dur,nome='video.mp4',tempos=null;
 if(narr){
  const cenas=await p.$$eval('.scene',ss=>ss.map(s=>[+s.dataset.in,+s.dataset.out]));
  cenas[cenas.length-1][1]=dur;
  const ds=JSON.parse(fs.readFileSync(narr)).duracoes;
  if(ds.length!==cenas.length)throw new Error(`narração tem ${ds.length} falas e o vídeo ${cenas.length} cenas`);
  let S=0;const seg=cenas.map(([a,bb],k)=>{const L=Math.max(bb-a,LEAD+ds[k]+TAIL);const o={a,len:bb-a,S,L,fala:S+LEAD};S+=L;return o});
  total=S;tempos={total,cenas:seg};nome='video-mudo-narr.mp4';
  mapa=T=>{const s=seg.find(x=>T<x.S+x.L)||seg[seg.length-1];return s.a+Math.min(T-s.S,s.len-0.001)};
  fs.writeFileSync(dir+'/tempos.json',JSON.stringify(tempos,null,1));
 }
 const tmp=fs.mkdtempSync('/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/frames-');
 const n=Math.ceil(total*fps);
 for(let f=0;f<n;f++){await p.evaluate(t=>seek(t),mapa(f/fps));await espera();await stage.screenshot({path:`${tmp}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92})}
 await b.close();
 execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(fps),'-i',`${tmp}/%05d.jpg`,'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',`${dir}/${nome}`]);
 fs.rmSync(tmp,{recursive:true});console.log('ok',n,'quadros →',dir+'/'+nome,tempos?`(${total.toFixed(1)} s)`:'');
})();
