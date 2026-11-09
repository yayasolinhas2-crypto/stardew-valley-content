// Desenha páginas HTML 1080x1920 em PNG transparente. Uso: node tools/texto_png.js lista.json  ([{"html":"...","out":"x.png"}])
// Cada página é gravada como arquivo e aberta por file:// (assim a fonte local carrega; setContent não carrega file://).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const L=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const tmp=path.join(path.dirname(path.resolve(process.argv[2])),'_pg.html');
for(const x of L){fs.writeFileSync(tmp,x.html);await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);
 const ok=await p.evaluate(()=>[...document.fonts].some(f=>f.status==='loaded'));if(!ok)throw new Error('fonte não carregou: '+x.out);
 await p.screenshot({path:x.out,omitBackground:true})}
await b.close()})();
