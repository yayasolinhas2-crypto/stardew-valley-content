# Vídeo "jogo × vida real" (pedido da Yasmin, 09/11): a imagem em pixel do jogo "vira" foto realista com brilho + whoosh.
# Uso: python3 tools/vida_real.py posts/025-pelican-real
# Lê <post>/vida_real.json:
#  {"titulo":"SE PELICAN TOWN FOSSE *REAL*…","trilha":"primavera","velocidade":1.5,
#   "cenas":[{"jogo":"jogo/pierre.png","real":"real/pierre.jpg","nome":"Armazém do Pierre","fala":"[empolgada] ...","cta":"♥ curte se ..."}]}
import json, os, sys, subprocess, importlib.util, shutil
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('narrar', os.path.join(RAIZ, 'tools/narrar.py')); N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
TMP = '/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/vidareal'
FPS, LEAD, TAIL, CAPA = 30, 0.2, 0.35, 1.0
def run(*a): subprocess.run(list(a), check=True)

def textos(cfg, post):
    """Desenha no navegador (fonte Nunito Black, contorno grosso) a capa e um rótulo por cena, em PNG transparente."""
    import html
    css = f"file://{RAIZ}/assets/fonts/nunito-latin-900-normal.woff2"
    def pag(corpo):
        return f'''<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:N;src:url({css})}}
        html,body{{margin:0;background:transparent}}#s{{width:1080px;height:1920px;position:relative}}
        .t{{position:absolute;left:50px;right:130px;text-align:center;font-family:N;font-weight:900;color:#fff;-webkit-text-stroke:16px #111;paint-order:stroke fill;
           text-shadow:0 10px 0 rgba(0,0,0,.45);text-transform:uppercase;line-height:1.02}}
        .t em{{font-style:normal;color:#ffd84a}}
        .ia{{position:absolute;left:40px;top:1440px;font-family:N;font-weight:900;font-size:26px;color:#fff;text-shadow:2px 2px 0 #000;opacity:.9}}
        .cta{{position:absolute;left:50%;transform:translateX(-50%);top:300px;background:#b8300f;color:#fff;font-family:N;font-weight:900;font-size:44px;padding:12px 26px;box-shadow:0 0 0 6px #5b2a0c;white-space:nowrap}}
        .rot{{position:absolute;left:50%;transform:translateX(-50%) rotate(-3deg);font-family:N;font-weight:900;font-size:40px;color:#2a1204;background:#ffd84a;padding:8px 22px;box-shadow:0 0 0 5px #111}}
        </style></head><body><div id="s">{corpo}</div></body></html>'''
    def em(t): return html.escape(t).replace('*', '\x00').split('\x00')
    def fmt(t):
        p = em(t); return ''.join(f'<em>{x}</em>' if i % 2 else x for i, x in enumerate(p))
    _fila = []
    if True:
        def shot(corpo, out):
            _fila.append({'html': pag(corpo), 'out': out})
        shot(f'<div class="t" style="top:820px;font-size:112px">{fmt(cfg["titulo"])}</div><div class="rot" style="top:1150px">jogo × vida real</div><div class="ia">imagem gerada por IA · @segredosdovalley</div>', f'{TMP}/capa.png')
        for i, c in enumerate(cfg['cenas']):
            corpo = f'<div class="t" style="top:1180px;font-size:92px">{fmt(c["nome"])}</div><div class="ia">imagem gerada por IA · @segredosdovalley</div>'
            shot(corpo, f'{TMP}/rot{i}.png')
            if c.get('cta'): shot(corpo + f'<div class="cta">{html.escape(c["cta"])}</div>', f'{TMP}/rotcta{i}.png')
        open(f'{TMP}/textos.json', 'w').write(json.dumps(_fila)); run('node', os.path.join(RAIZ, 'tools/texto_png.js'), f'{TMP}/textos.json')

def main(post):
    cfg = json.load(open(f'{post}/vida_real.json')); cenas = cfg['cenas']; vel = cfg.get('velocidade', 1.5)
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP); os.makedirs(f'{post}/narracao', exist_ok=True)
    nc = {'voz': cfg.get('voz', 'Sulafat'), 'falas': [c['fala'] for c in cenas]}
    marca = f'{post}/narracao/falas.json'
    if os.path.exists(marca) and json.load(open(marca)) == nc and all(os.path.exists(f'{post}/narracao/{i+1:02d}.wav') for i in range(len(cenas))):
        print('narração reaproveitada')
    elif not N.lote(nc, post, TMP):
        for i, c in enumerate(cenas): N.fala(c['fala'], nc['voz'], f'{post}/narracao/{i+1:02d}.wav', TMP)
    json.dump(nc, open(marca, 'w'), ensure_ascii=False)
    durs = [N.dur(f'{post}/narracao/{i+1:02d}.wav') for i in range(len(cenas))]
    textos(cfg, post)
    # cena com "icone" (item/retrato pequeno do jogo): monta o quadro do jogo com o ícone em pixel GRANDE no centro,
    # em cima da própria foto real desfocada e escurecida (a revelação fica natural)
    from PIL import Image, ImageFilter, ImageEnhance
    for i, c in enumerate(cenas):
        if c.get('icone') or c.get('jogo'):
            bg = Image.open(f'{post}/{c["real"]}').convert('RGB'); bw, bh = bg.size; esc = max(1080 / bw, 1920 / bh)
            bg = bg.resize((int(bw * esc) + 1, int(bh * esc) + 1)).crop((0, 0, 1080, 1920)).filter(ImageFilter.GaussianBlur(28))
            bg = ImageEnhance.Brightness(bg).enhance(0.55)
            ic = Image.open(os.path.join(RAIZ, c['icone']) if c.get('icone') else f'{post}/{c["jogo"]}').convert('RGBA')
            if c.get('icone'): k = max(1, 760 // max(ic.size)); ic = ic.resize((ic.width * k, ic.height * k), Image.NEAREST)
            else:   # construção do jogo: cabe inteira (sem cortar), pixel nítido
                k = min(1000 / ic.width, 1150 / ic.height); ic = ic.resize((int(ic.width * k), int(ic.height * k)), Image.NEAREST)
            bg.paste(ic, ((1080 - ic.width) // 2, 960 - ic.height // 2 - 120), ic)
            bg.save(f'{TMP}/jogo{i}.png'); c['jogo'] = os.path.relpath(f'{TMP}/jogo{i}.png', post)
    cover = 'scale=1080:1920:force_original_aspect_ratio=increase:flags=neighbor,crop=1080:1920,setsar=1'
    coverR = 'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1'
    partes, t0, trocas = [], 0.0, []
    # capa: metade de cima o jogo, metade de baixo a foto, título no meio (vira o 1º quadro e a capa do post)
    c0 = cenas[0]
    run('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', str(CAPA), '-i', f'{post}/{c0["jogo"]}', '-loop', '1', '-t', str(CAPA), '-i', f'{post}/{c0["real"]}', '-loop', '1', '-t', str(CAPA), '-i', f'{TMP}/capa.png',
        '-filter_complex', '[0:v]scale=1080:960:force_original_aspect_ratio=increase:flags=neighbor,crop=1080:960[a];[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[b];[a][b]vstack,setsar=1[ab];[ab][2:v]overlay=0:0,fps=30,format=yuv420p[v]',
        '-map', '[v]', '-t', str(CAPA), '-c:v', 'libx264', '-crf', '18', f'{TMP}/p_capa.mp4')
    partes.append(f'{TMP}/p_capa.mp4'); t0 = CAPA
    tempos = []
    for i, c in enumerate(cenas):
        L = max(2.4, LEAD + durs[i] + TAIL); g = round(min(1.0, L * 0.38), 3); tr = 0.3
        rot = f'{TMP}/rotcta{i}.png' if c.get('cta') else f'{TMP}/rot{i}.png'
        fc = (f'[0:v]{cover},zoompan=z=\'1+0.0006*on\':d=1:s=1080x1920:fps=30[g];'
              f'[1:v]{coverR},zoompan=z=\'1.08-0.0012*on\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s=1080x1920:fps=30[r];'
              f'[g][r]xfade=transition=fadewhite:duration={tr}:offset={g},format=yuv420p[x];[x][2:v]overlay=0:0:enable=\'gte(t,{g+tr*0.5})\'[v]')
        run('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', '30', '-t', f'{g+tr+0.05:.3f}', '-i', f'{post}/{c["jogo"]}',
            '-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', f'{post}/{c["real"]}', '-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', rot,
            '-filter_complex', fc, '-map', '[v]', '-t', f'{L:.3f}', '-r', '30', '-c:v', 'libx264', '-crf', '18', f'{TMP}/p{i}.mp4')
        partes.append(f'{TMP}/p{i}.mp4'); tempos.append((t0, L)); trocas.append(t0 + g); t0 += L
    total = t0
    open(f'{TMP}/lista.txt', 'w').write(''.join(f"file '{p}'\n" for p in partes))
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/lista.txt', '-c', 'copy', f'{TMP}/base.mp4')
    # áudio: voz (cada fala no início da cena) + whoosh em cada revelação + trilha baixinha com sidechain
    ins = ['-i', f'{TMP}/base.mp4']; filt = []; mix = []; k = 1
    for i, (s, L) in enumerate(tempos):
        ins += ['-i', f'{post}/narracao/{i+1:02d}.wav']; ms = int((s + LEAD) * 1000); filt.append(f'[{k}:a]aresample=48000,adelay={ms}|{ms}[v{i}]'); mix.append(f'[v{i}]'); k += 1
    voz = ''.join(mix) + f'amix=inputs={len(mix)}:normalize=0,apad=whole_dur={total:.3f}[voz]'; filt.append(voz)
    sfx = []
    for j, t in enumerate(trocas):
        ins += ['-i', os.path.join(RAIZ, 'assets/sfx/whoosh.wav')]; ms = int((t - 0.08) * 1000); filt.append(f'[{k}:a]aresample=48000,volume=0.55,adelay={ms}|{ms}[w{j}]'); sfx.append(f'[w{j}]'); k += 1
    ins += ['-i', os.path.join(RAIZ, 'assets/trilhas', cfg.get('trilha', 'primavera') + '.wav')]
    filt.append(f'[{k}:a]aresample=48000,aloop=loop=-1:size=2e9,atrim=0:{total:.3f},volume=0.22,afade=t=out:st={total-1:.3f}:d=1[mus]')
    filt.append('[voz]asplit=2[vz][sc];[mus][sc]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[musd]')
    filt.append('[vz][musd]' + ''.join(sfx) + f'amix=inputs={2+len(sfx)}:normalize=0,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.89[a]')
    run('ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(filt), '-map', '0:v', '-map', '[a]', '-t', f'{total:.3f}',
        '-c:v', 'copy', '-c:a', 'pcm_s16le', '-ar', '48000', f'{TMP}/normal.mkv')
    run('ffmpeg', '-y', '-loglevel', 'error', '-i', f'{TMP}/normal.mkv', '-filter_complex', f'[0:v]setpts=PTS/{vel},fps=30[v];[0:a]atempo={vel}[a]',
        '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', f'{post}/video-15x.mp4')
    run('ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-15x.mp4', '-frames:v', '1', '-q:v', '2', f'{post}/video-capa.jpg')
    print(f'OK {post}/video-15x.mp4 · {total/vel:.1f}s')

if __name__ == '__main__':
    main(sys.argv[1].rstrip('/'))
