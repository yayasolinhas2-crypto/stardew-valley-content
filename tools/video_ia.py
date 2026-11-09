# Finaliza um vídeo gerado por IA (Gemini Omni): narração Sulafat, título/capa, rótulos por trecho, marca "imagem gerada por IA", trilha com sidechain.
# Uso: python3 tools/video_ia.py posts/026-pelican-ia   (lê video_ia.json: bruto, titulo, trilha, trechos:[{ini,fim,nome,fala,cta?}])
import json, os, sys, subprocess, importlib.util, shutil, html
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('narrar', os.path.join(RAIZ, 'tools/narrar.py')); N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
TMP = '/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/videoia'
def run(*a): subprocess.run(list(a), check=True)
def main(post):
    cfg = json.load(open(f'{post}/video_ia.json')); tr = cfg['trechos']
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP); os.makedirs(f'{post}/narracao', exist_ok=True)
    nc = {'voz': cfg.get('voz', 'Sulafat'), 'falas': [t['fala'] for t in tr]}; marca = f'{post}/narracao/falas.json'
    if not (os.path.exists(marca) and json.load(open(marca)) == nc):
        if not N.lote(nc, post, TMP):
            for i, t in enumerate(tr): N.fala(t['fala'], nc['voz'], f'{post}/narracao/{i+1:02d}.wav', TMP)
        json.dump(nc, open(marca, 'w'), ensure_ascii=False)
    fonte = f"file://{RAIZ}/assets/fonts/nunito-latin-900-normal.woff2"
    def fmt(t):
        p = html.escape(t).split('*'); return ''.join(f'<em>{x}</em>' if i % 2 else x for i, x in enumerate(p))
    css = f'''@font-face{{font-family:N;src:url({fonte})}}html,body{{margin:0;background:transparent}}#s{{width:1080px;height:1920px;position:relative}}
      .t{{position:absolute;left:50px;right:130px;text-align:center;font-family:N;font-weight:900;color:#fff;-webkit-text-stroke:16px #111;paint-order:stroke fill;text-shadow:0 10px 0 rgba(0,0,0,.45);text-transform:uppercase;line-height:1.02}}
      .t em{{font-style:normal;color:#ffd84a}}.ia{{position:absolute;left:40px;top:1440px;font-family:N;font-weight:900;font-size:26px;color:#fff;text-shadow:2px 2px 0 #000}}
      .cta{{position:absolute;left:50%;transform:translateX(-50%);top:300px;background:#b8300f;color:#fff;font-family:N;font-weight:900;font-size:44px;padding:12px 26px;box-shadow:0 0 0 6px #5b2a0c;white-space:nowrap}}'''
    _fila = []
    if True:
        def shot(corpo, out):
            _fila.append({'html': f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div id="s">{corpo}</div></body></html>', 'out': out})
        ia = '<div class="ia">vídeo gerado por IA · @segredosdovalley</div>'
        shot(f'<div class="t" style="top:700px;font-size:118px">{fmt(cfg["titulo"])}</div>' + ia, f'{TMP}/capa.png')
        for i, t in enumerate(tr):
            shot(f'<div class="t" style="top:1180px;font-size:88px">{fmt(t["nome"])}</div>' + (f'<div class="cta">{html.escape(t["cta"])}</div>' if t.get('cta') else '') + ia, f'{TMP}/r{i}.png')
        open(f'{TMP}/textos.json', 'w').write(json.dumps(_fila)); run('node', os.path.join(RAIZ, 'tools/texto_png.js'), f'{TMP}/textos.json')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{post}/{cfg["bruto"]}'], capture_output=True, text=True).stdout)
    CAPA = 1.6
    ins = ['-i', f'{post}/{cfg["bruto"]}', '-loop', '1', '-i', f'{TMP}/capa.png'] ; f = ['[0:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30[b]', f'[b][1:v]overlay=0:0:enable=\'lt(t,{CAPA})\'[v0]']; last = 'v0'
    for i, t in enumerate(tr):
        ins += ['-loop', '1', '-i', f'{TMP}/r{i}.png']; ini = max(t['ini'], CAPA if i == 0 else t['ini'])
        f.append(f'[{last}][{i+2}:v]overlay=0:0:enable=\'between(t,{ini},{t["fim"]})\'[v{i+1}]'); last = f'v{i+1}'
    k = len(tr) + 2; vozes = []
    for i, t in enumerate(tr):
        ins += ['-i', f'{post}/narracao/{i+1:02d}.wav']; ms = int((t['ini'] + 0.25) * 1000); f.append(f'[{k}:a]aresample=48000,adelay={ms}|{ms}[n{i}]'); vozes.append(f'[n{i}]'); k += 1
    ins += ['-i', os.path.join(RAIZ, 'assets/trilhas', cfg.get('trilha', 'primavera') + '.wav')]
    f.append(''.join(vozes) + f'amix=inputs={len(vozes)}:normalize=0,apad=whole_dur={dur:.3f}[voz]')
    f.append(f'[{k}:a]aresample=48000,aloop=loop=-1:size=2e9,atrim=0:{dur:.3f},volume=0.25,afade=t=out:st={dur-1:.3f}:d=1[mus]')
    f.append('[voz]asplit=2[vz][sc];[mus][sc]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[musd];[vz][musd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.89[a]')
    run('ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(f), '-map', f'[{last}]', '-map', '[a]', '-t', f'{dur:.3f}',
        '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', f'{post}/video-15x.mp4')
    run('ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-15x.mp4', '-frames:v', '1', '-q:v', '2', f'{post}/video-capa.jpg')
    print('OK', post, f'{dur:.1f}s')
if __name__ == '__main__': main(sys.argv[1].rstrip('/'))
