// Desenha páginas HTML 1080x1920 em PNG transparente. Uso: node tools/texto_png.js lista.json  ([{"html":"...","out":"x.png"}])
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const L=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const x of L){await p.setContent(x.html,{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:x.out,omitBackground:true})}
await b.close()})();
