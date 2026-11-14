# Carrossel de FOTOS pro TikTok no formato "dica com print da gameplay" (referência: "Things I wish I knew…", 194 mil curtidas).
# Uso: python3 tools/carrossel_dicas.py posts/041-coisas-que-eu-queria-saber
# Lê <post>/carrossel.json:
# {"serie":"COISAS QUE EU QUERIA SABER","parte":1,
#  "slides":[{"src":"gravacoes/bruto/x.mp4","t":4.0,"cx":960,"texto":"Planta *VAGEM* na primavera!","sub":"texto menor opcional","capa":false}]}
# Saída: <post>/slides/NN.jpg (1080x1920, JPEG — o TikTok recusa PNG). Fundo = quadro da gravação dela em tela cheia (recorte 9:16, pixel nítido).
# Texto: branco grande com contorno preto, palavra entre *asteriscos* em dourado; selo da série no topo; assinatura. Tudo dentro da área segura.
import json, os, sys, subprocess, html, re
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = 'file://' + os.path.join(RAIZ, 'assets/fonts/nunito-latin-900-normal.woff2')

def quadro(src, t, cx, out):
    cw = 608; x = min(max(int(cx) - cw // 2, 0), 1920 - cw)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t), '-i', os.path.join(RAIZ, src), '-frames:v', '1',
                    '-vf', f'crop={cw}:1080:{x}:0,scale=1080:1920:flags=neighbor,eq=brightness=-0.06', out], check=True)

def marca(txt):
    t = html.escape(txt)
    return re.sub(r'\*(.+?)\*', r'<span class="k">\1</span>', t)

CSS = """@font-face{font-family:N;src:url('%s') format('woff2')}
*{margin:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;font-family:N,sans-serif}
.bg{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;image-rendering:pixelated}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0,rgba(0,0,0,0) 22%%,rgba(0,0,0,0) 45%%,rgba(0,0,0,.55) 100%%)}
.top{position:absolute;top:290px;left:70px;right:150px;display:flex;gap:14px;align-items:center}
.pill{background:#f6c445;color:#2b1a05;font-size:34px;padding:10px 22px;border-radius:999px;letter-spacing:.5px;box-shadow:0 4px 0 #8a5a12}
.cnt{color:#fff;font-size:32px;-webkit-text-stroke:6px #000;paint-order:stroke fill}
.box{position:absolute;left:70px;right:150px;top:840px;display:flex;flex-direction:column;gap:26px;align-items:flex-start}
.num{width:120px;height:120px;border-radius:50%%;background:#f6c445;color:#2b1a05;font-size:76px;display:grid;place-items:center;box-shadow:0 6px 0 #8a5a12}
.tx{color:#fff;font-size:84px;line-height:1.08;-webkit-text-stroke:14px #000;paint-order:stroke fill;letter-spacing:-.5px}
.sub{color:#fff;font-size:44px;line-height:1.15;-webkit-text-stroke:9px #000;paint-order:stroke fill}
.k{color:#f6c445}
.capa .box{top:620px}.capa .tx{font-size:112px}
.sig{position:absolute;left:70px;top:1470px;color:#fff;font-size:30px;-webkit-text-stroke:6px #000;paint-order:stroke fill;opacity:.95}
""" % FONT

def main(post):
    cfg = json.load(open(f'{post}/carrossel.json')); sl = cfg['slides']
    os.makedirs(f'{post}/slides', exist_ok=True)
    pages = []; n = len([s for s in sl if not s.get('capa') and not s.get('fim')])
    i_dica = 0
    for i, s in enumerate(sl, 1):
        bg = os.path.abspath(f'{post}/slides/_bg{i:02d}.png'); quadro(s['src'], s['t'], s.get('cx', 960), bg)
        capa = s.get('capa'); fim = s.get('fim')
        if not capa and not fim: i_dica += 1
        topo = f'<div class="top"><span class="pill">{html.escape(cfg["serie"])} · PARTE {cfg["parte"]}</span>' + \
               ('' if capa or fim else f'<span class="cnt">{i_dica}/{n}</span>') + '</div>'
        num = '' if capa or fim else f'<div class="num">{i_dica}</div>'
        sub = f'<p class="sub">{marca(s["sub"])}</p>' if s.get('sub') else ''
        body = (f'<img class="bg" src="file://{bg}"><div class="sh"></div>{topo}'
                f'<div class="box">{num}<p class="tx">{marca(s["texto"])}</p>{sub}</div><div class="sig">@segredosdovalley</div>')
        pages.append({'html': f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{"capa" if capa else ""}">{body}</body></html>',
                      'out': os.path.abspath(f'{post}/slides/_{i:02d}.png')})
    lista = os.path.abspath(f'{post}/slides/_paginas.json'); json.dump(pages, open(lista, 'w'))
    subprocess.run(['node', os.path.join(RAIZ, 'tools/texto_png.js'), lista], check=True)
    for i in range(1, len(sl) + 1):
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{post}/slides/_{i:02d}.png', '-q:v', '2', f'{post}/slides/{i:02d}.jpg'], check=True)
    for f in os.listdir(f'{post}/slides'):
        if f.startswith('_'): os.remove(f'{post}/slides/{f}')
    print('OK', len(sl), 'slides em', f'{post}/slides')

if __name__ == '__main__': main(sys.argv[1].rstrip('/'))
