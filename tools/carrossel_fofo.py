# Guia em FOTOS estilo "fofo" (referência TetelaJoga 22/11): fundo pastel, moldura com laço, título numerado,
# caixa de texto clara e o print da gameplay dela num quadro arredondado. Desenho 100% nosso (CSS), sem IA.
# Uso: python3 tools/carrossel_fofo.py posts/NNN  (lê <post>/carrossel.json: {"serie","parte","slides":[{src,t,cx,titulo,texto,capa,fim}]})
import json, os, sys, subprocess, html, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = 'file://' + os.path.join(RAIZ, 'assets/fonts/nunito-latin-900-normal.woff2')
def quadro(src, t, cx, out):
    w = 1100; x = min(max(int(cx) - w // 2, 0), 1920 - w)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',os.path.join(RAIZ,src),'-frames:v','1',
                    '-vf',f'crop={w}:880:{x}:100,scale=880:-1:flags=neighbor',out],check=True)
def marca(t): return re.sub(r'\*(.+?)\*', r'<b class="k">\1</b>', html.escape(t)).replace('|','<br>')
LACO = '''<svg class="laco" viewBox="0 0 200 90"><path d="M100 45 C70 5 20 5 25 45 C20 85 70 85 100 45 Z" fill="#f7a8c4" stroke="#c9577f" stroke-width="6"/>
<path d="M100 45 C130 5 180 5 175 45 C180 85 130 85 100 45 Z" fill="#f7a8c4" stroke="#c9577f" stroke-width="6"/>
<rect x="86" y="30" width="28" height="30" rx="8" fill="#e9789f" stroke="#c9577f" stroke-width="6"/></svg>'''
CSS = """@font-face{font-family:N;src:url('%s') format('woff2')}*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:N,sans-serif;background:linear-gradient(#bfe6ff 0,#e8f7ff 45%%,#d9f2c4 100%%)}
.dot{position:absolute;border-radius:50%%;background:#fff;opacity:.7}
.card{position:absolute;left:70px;right:140px;top:300px;bottom:430px;background:#fff8ec;border:10px solid #e7b36a;border-radius:46px;box-shadow:0 14px 0 #c98f45}
.laco{position:absolute;left:50%%;top:228px;width:230px;transform:translateX(-58%%)}
.col{position:absolute;left:110px;right:180px;top:350px;display:flex;flex-direction:column;gap:28px}
.tit{background:#ffe7b3;border:6px solid #e7b36a;border-radius:28px;padding:22px 26px;text-align:center;color:#6b3d17;font-size:56px;line-height:1.1}
.tx{color:#4a2c12;font-size:44px;line-height:1.25;text-align:center}
.k{color:#d2457a}
.img{position:absolute;left:115px;right:185px;bottom:470px;height:520px;border:8px solid #e7b36a;border-radius:30px;overflow:hidden;background:#000}
.img img{width:100%%;height:100%%;object-fit:cover;image-rendering:pixelated}
.pill{position:absolute;left:110px;top:1500px;background:#f7a8c4;color:#7a1f45;font-size:30px;padding:10px 24px;border-radius:999px}
.sig{position:absolute;left:110px;top:1440px;color:#6b3d17;font-size:30px}
.capa .tit{font-size:80px;padding:34px}.capa .tx{font-size:46px}
""" % FONT
def main(post):
    cfg=json.load(open(f'{post}/carrossel.json')); sl=cfg['slides']; os.makedirs(f'{post}/slides',exist_ok=True); pages=[]
    for i,s in enumerate(sl,1):
        bg=os.path.abspath(f'{post}/slides/_bg{i:02d}.png'); quadro(s['src'],s['t'],s.get('cx',960),bg)
        cls='capa' if (s.get('capa') or s.get('fim')) else ''
        body=(''.join(f'<div class="dot" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px"></div>' for x,y,r in [(80,120,60),(900,90,80),(500,160,40),(960,1700,70),(60,1760,50)])+
              f'<div class="card"></div>{LACO}<div class="col"><div class="tit">{marca(s["titulo"])}</div><div class="tx">{marca(s.get("texto",""))}</div></div>'
              f'<div class="img"><img src="file://{bg}"></div><div class="sig">@segredosdovalley</div>'
              f'<div class="pill">{html.escape(cfg["serie"])} · parte {cfg["parte"]}</div>')
        pages.append({'html':f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{body}</body></html>','out':os.path.abspath(f'{post}/slides/_{i:02d}.png')})
    lista=os.path.abspath(f'{post}/slides/_paginas.json'); json.dump(pages,open(lista,'w'))
    subprocess.run(['node',os.path.join(RAIZ,'tools/texto_png.js'),lista],check=True)
    for i in range(1,len(sl)+1): subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'{post}/slides/_{i:02d}.png','-q:v','2',f'{post}/slides/{i:02d}.jpg'],check=True)
    for f in os.listdir(f'{post}/slides'):
        if f.startswith('_'): os.remove(f'{post}/slides/{f}')
    print('OK',len(sl),'slides')
if __name__=='__main__': main(sys.argv[1].rstrip('/'))
