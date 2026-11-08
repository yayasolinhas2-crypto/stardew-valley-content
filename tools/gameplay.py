# Edita gravações de gameplay (16:9) em vídeo vertical 1080x1920 no estilo @segredosdovalley.
# Uso: python3 tools/gameplay.py posts/013-todo-dia
# Lê <post>/gameplay.json:
# {"titulo":"3 coisas pra fazer TODO DIA","voz":"Sulafat","velocidade":1.5,
#  "cenas":[{"src":"gravacoes/bruto/x.mp4","ini":20.0,"selo":"Nº 1 · Ver a TV","fala":"[animada] ...","cx":960,"cy":540,"zoom":1.0,"cta":"comenta DIÁRIO"}]}
# Fundo = a própria gameplay desfocada; no meio a gameplay recortada com moldura de madeira; selo e título no topo;
# legenda sincronizada; narração Sulafat em lote (tools/narrar.py), som do jogo baixinho, whoosh nas trocas.
import json, os, sys, subprocess, importlib.util, shutil
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('narrar', os.path.join(RAIZ, 'tools/narrar.py')); N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
TMP = '/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/gameplay'
LEAD, TAIL, FPS = 0.25, 0.4, 30
GX, GY, GW, GH = 40, 650, 1000, 800          # janela da gameplay (título em cima, legenda dentro, assinatura embaixo; tudo até y=1500)

def run(*a): subprocess.run(list(a), check=True)

def main(post):
    cfg = json.load(open(f'{post}/gameplay.json')); cenas = cfg['cenas']
    os.makedirs(f'{post}/narracao', exist_ok=True); os.makedirs(TMP, exist_ok=True)
    # 1) narração em lote (1 pedido) — mesmas regras do narrar.py
    nc = {'voz': cfg.get('voz', 'Sulafat'), 'falas': [c['fala'] for c in cenas]}
    if not N.lote(nc, post, TMP):
        print('lote falhou — fala a fala')
        for i, c in enumerate(cenas): N.fala(c['fala'], nc['voz'], f'{post}/narracao/{i+1:02d}.wav', TMP)
    durs = [N.dur(f'{post}/narracao/{i+1:02d}.wav') for i in range(len(cenas))]
    # 2) cada cena: recorte da gameplay + fundo desfocado
    partes, t0, tempos = [], 0.0, []
    for i, c in enumerate(cenas):
        L = max(c.get('min', 2.0), LEAD + durs[i] + TAIL)
        z = c.get('zoom', 1.0); cw = int(GW / GH * 1080 / z) // 2 * 2; ch = int(1080 / z) // 2 * 2
        cx = min(max(c.get('cx', 960) - cw // 2, 0), 1920 - cw); cy = min(max(c.get('cy', 540) - ch // 2, 0), 1080 - ch)
        out = f'{TMP}/cena{i}.mp4'
        fc = (f'[0:v]tpad=stop_mode=clone:stop_duration=60,split[a][b];'
              f'[a]scale=-2:1920,crop=1080:1920,boxblur=22:3,eq=brightness=-0.18:saturation=1.1[bg];'
              f'[b]crop={cw}:{ch}:{cx}:{cy},scale={GW}:{GH}:flags=neighbor,setsar=1[g];'
              f'[bg][g]overlay={GX}:{GY},fps={FPS},format=yuv420p[v];'
              f'[0:a]volume=0.12,aresample=48000,apad[ga]')
        run('ffmpeg', '-y', '-loglevel', 'error', '-ss', str(c['ini']), '-i', os.path.join(RAIZ, c['src']),
            '-filter_complex', fc, '-map', '[v]', '-map', '[ga]', '-t', f'{L:.3f}', '-c:v', 'libx264', '-crf', '18', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', out)
        real = N.dur(out)
        if abs(real - L) > 0.08: raise SystemExit(f'cena {i}: duração {real:.2f}s ≠ {L:.2f}s (dessincronizaria a legenda)')
        partes.append(out); tempos.append({'S': t0, 'L': L, 'fala': t0 + LEAD, 'dur': durs[i]}); t0 += L
    total = t0
    lst = f'{TMP}/lista.txt'; open(lst, 'w').write(''.join(f"file '{p}'\n" for p in partes))
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'copy', '-c:a', 'pcm_s16le', f'{TMP}/base.mkv')
    # 3) camada de texto (título, selos, legenda, moldura) desenhada no navegador, quadro a quadro, com fundo transparente
    leg = []
    for i, c in enumerate(cenas):
        ws = N.re.sub(r'\[[^\]]*\]', '', c['fala']).split(); pesos = [len(N.re.sub(r'[^\wÀ-ú]', '', w)) + 2 for w in ws]; tot = sum(pesos); acc = 0; bloco = []
        for k, w in enumerate(ws):
            a = tempos[i]['fala'] + durs[i] * acc / tot; acc += pesos[k]; b = tempos[i]['fala'] + durs[i] * acc / tot
            bloco.append({'w': w, 't0': a, 't1': b})
            if len(' '.join(x['w'] for x in bloco)) >= 18 or w[-1] in '.!?…:' or k == len(ws) - 1:
                leg.append({'ini': bloco[0]['t0'], 'fim': bloco[-1]['t1'] + 0.15, 'p': bloco}); bloco = []
    dados = {'titulo': cfg['titulo'], 'cenas': [{**tempos[i], 'selo': c.get('selo', ''), 'cta': c.get('cta', '')} for i, c in enumerate(cenas)], 'leg': leg, 'total': total,
             'gx': GX, 'gy': GY, 'gw': GW, 'gh': GH}
    json.dump(dados, open(f'{TMP}/dados.json', 'w'), ensure_ascii=False)
    shutil.rmtree(f'{TMP}/ov', ignore_errors=True); os.makedirs(f'{TMP}/ov')
    run('node', os.path.join(RAIZ, 'tools/gameplay_overlay.js'), f'{TMP}/dados.json', f'{TMP}/ov', str(FPS))
    # 4) junta: base + camada + voz + whoosh; volume uniforme; velocidade final
    ins = ['-i', f'{TMP}/base.mkv', '-framerate', str(FPS), '-i', f'{TMP}/ov/%05d.png']
    filt = ['[0:v][1:v]overlay=0:0:shortest=1[v]']; rot = ['[0:a]']; n = 2
    for i, t in enumerate(tempos):
        ins += ['-i', f'{post}/narracao/{i+1:02d}.wav']; ms = int(t['fala'] * 1000); filt.append(f'[{n}]adelay={ms}|{ms}[n{i}]'); rot.append(f'[n{i}]'); n += 1
        if i > 0:
            ins += ['-i', os.path.join(RAIZ, 'assets/sfx/whoosh.wav')]; ms = int(t['S'] * 1000); filt.append(f'[{n}]volume=0.8,adelay={ms}|{ms}[w{i}]'); rot.append(f'[w{i}]'); n += 1
    filt.append(''.join(rot) + f'amix=inputs={len(rot)}:normalize=0:dropout_transition=0,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.89[a]')
    run('ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(filt), '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}',
        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', f'{post}/video-narrado.mp4')
    vel = float(cfg.get('velocidade', 1.5))
    run('ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-narrado.mp4', '-filter_complex', f'[0:v]setpts=PTS/{vel},fps={FPS}[v];[0:a]atempo={vel}[a]',
        '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', f'{post}/video-15x.mp4')
    json.dump({'falas': [c['fala'] for c in cenas]}, open(f'{post}/narracao.json', 'w'), ensure_ascii=False, indent=1)
    print(f'OK {post}/video-15x.mp4 · {total/vel:.1f}s')

if __name__ == '__main__':
    main(sys.argv[1].rstrip('/'))
