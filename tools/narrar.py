# Narra um vídeo com a voz escolhida (Gemini TTS) e junta ao vídeo.
# Uso: python3 tools/narrar.py posts/005-tela-fim-do-dia
# Lê <post>/narracao.json  → {"voz":"Sulafat","falas":["fala da cena 1", ...]}  (uma fala por <section class="scene">)
# Gera <post>/narracao/NN.mp3, chama tools/video.js --narr (estica cenas pra caber a fala) e cria <post>/video-narrado.mp4.
# A chave do Gemini NÃO fica aqui: o proxy do ambiente injeta o header x-goog-api-key.
import json, base64, subprocess, sys, os, hashlib

MODELO = 'gemini-3.8-flash-tts'   # texto puro: pronuncia "Stardew Valley" em inglês (o 2.5 punha "Istárdiu")
MAX_PPS = 2.95                     # regra: no máximo 3,0 palavras por segundo
API = 'https://generativelanguage.googleapis.com/v1beta/models/'

def curl_json(url, body, tmp):
    open(tmp, 'w').write(json.dumps(body))
    r = subprocess.run(['curl', '-sS', '-H', 'x-goog-api-key: DUMMY', '-H', 'Content-Type: application/json',
                        '-d', '@' + tmp, url], capture_output=True, text=True)
    return json.loads(r.stdout)

def dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                capture_output=True, text=True).stdout)

def fala(texto, voz, out, tmpdir):
    chave = hashlib.sha1(f'{MODELO}|{voz}|{texto}'.encode()).hexdigest()[:12]
    cache = f'{tmpdir}/{chave}.mp3'
    if not os.path.exists(cache):
        for tentativa in range(3):
            d = curl_json(API + MODELO + ':generateContent', {
                "contents": [{"parts": [{"text": texto}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}, tmpdir + '/r.json')
            if 'candidates' in d: break
            print('  tentativa', tentativa + 1, 'falhou:', str(d)[:200])
        pcm = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
        open(tmpdir + '/a.pcm', 'wb').write(pcm)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', tmpdir + '/a.pcm',
                        '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                        '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '160k', cache], check=True)
    pps = len(texto.split()) / dur(cache)
    f = min(1.0, MAX_PPS / pps)  # só desacelera, nunca acelera
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', cache, '-af', f'atempo={f:.3f}', '-c:a', 'libmp3lame', '-b:a', '160k', out], check=True)
    return dur(out), len(texto.split())

def main(post):
    cfg = json.load(open(f'{post}/narracao.json'))
    voz = cfg.get('voz', 'Sulafat')
    os.makedirs(f'{post}/narracao', exist_ok=True)
    tmpdir = os.environ.get('NARR_TMP', '/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/narr-cache')
    os.makedirs(tmpdir, exist_ok=True)
    durs, palavras = [], 0
    for i, t in enumerate(cfg['falas']):
        d, w = fala(t, voz, f'{post}/narracao/{i+1:02d}.mp3', tmpdir)
        durs.append(round(d, 3)); palavras += w
        print(f'  cena {i+1}: {d:.2f}s · {w/d:.2f} palavras/s · {t}')
    json.dump({'duracoes': durs}, open(f'{post}/narracao/duracoes.json', 'w'))
    subprocess.run(['node', 'tools/video.js', post, '30', '--narr', f'{post}/narracao/duracoes.json'], check=True)
    tempos = json.load(open(f'{post}/tempos.json'))
    # trilha de voz: cada fala começa no início da sua cena (+LEAD)
    ins, filt = [], []
    for i, c in enumerate(tempos['cenas']):
        ins += ['-i', f'{post}/narracao/{i+1:02d}.mp3']
        ms = int(c['fala'] * 1000)
        filt.append(f'[{i+1}]adelay={ms}|{ms}[a{i}]')
    filt.append(''.join(f'[a{i}]' for i in range(len(tempos['cenas']))) + f'amix=inputs={len(tempos["cenas"])}:normalize=0,loudnorm=I=-14:TP=-1.5,apad[voz]')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-mudo-narr.mp4', *ins, '-filter_complex', ';'.join(filt),
                    '-map', '0:v', '-map', '[voz]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart',
                    f'{post}/video-narrado.mp4'], check=True)
    os.remove(f'{post}/video-mudo-narr.mp4')
    total = tempos['total']
    print(f'OK {post}/video-narrado.mp4 · {total:.1f}s · {palavras} palavras · média {palavras/total:.2f} palavras/s no vídeo')

if __name__ == '__main__':
    main(sys.argv[1].rstrip('/'))
