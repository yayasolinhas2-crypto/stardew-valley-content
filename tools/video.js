// Uso: node tools/video.js posts/001-segredos [fps] [--quadros 1.0,5.5,...]
// Renderiza video.html quadro a quadro (seek(t)) e monta video.mp4 1080x1920 com ffmpeg.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
(async()=>{const dir=path.resolve(process.argv[2]);const fps=+(process.argv[3]||30);
 const qi=process.argv.indexOf('--quadros');const so=qi>0?process.argv[qi+1].split(',').map(Number):null;
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('file://'+dir+'/video.html');await p.evaluate(()=>document.fonts.ready);
 const stage=await p.$('#stage');
 if(so){for(const t of so){await p.evaluate(t=>seek(t),t);await stage.screenshot({path:`${dir}/quadro-${t}.png`})}await b.close();return}
 const tmp=fs.mkdtempSync('/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/frames-');
 const dur=await p.evaluate(()=>DUR);const n=Math.ceil(dur*fps);
 for(let f=0;f<n;f++){await p.evaluate(t=>seek(t),f/fps);await stage.screenshot({path:`${tmp}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92})}
 await b.close();
 execFileSync('ffmpeg',['-y','-loglevel','error','-framerate',String(fps),'-i',`${tmp}/%05d.jpg`,'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',`${dir}/video.mp4`]);
 fs.rmSync(tmp,{recursive:true});console.log('ok',n,'quadros →',dir+'/video.mp4');
})();
