# Narra um vídeo com a voz escolhida (Gemini TTS) e junta ao vídeo.
# Uso: python3 tools/narrar.py posts/005-tela-fim-do-dia
# Lê <post>/narracao.json  → {"voz":"Sulafat","falas":["[emoção] fala da cena 1", ...]}  (uma fala por <section class="scene">)
# A marcação [emoção] no começo da fala guia a interpretação e não é lida em voz alta (conferido por transcrição).
# Gera <post>/narracao/NN.mp3, chama tools/video.js --narr (estica cenas pra caber a fala) e cria <post>/video-narrado.mp4.
# A chave do Gemini NÃO fica aqui: o proxy do ambiente injeta o header x-goog-api-key.
import json, base64, subprocess, sys, os, hashlib, re, unicodedata

MODELO = os.environ.get('NARR_MODELO', 'gemini-2.5-flash-preview-tts')  # voz aprovada pela Yasmin em 08/11 ("o sotaque dela tá bem bom")
# 2.5 Pro: aceita instrução de interpretação sem ler em voz alta e pronuncia "Stardew Valley" em inglês (testado 07/11).
# 3.8 Flash: pronuncia bem, mas sem emoção, e quando recebe [emoção] às vezes LÊ a marcação. Cota grátis: 100 áudios/dia por modelo.
def montar(texto):
    m = re.match(r'^\[([^\]]*)\]\s*(.*)$', texto)
    emocao, fala = (m.group(1), m.group(2)) if m else ('animada', texto)
    if 'pro' in MODELO or '2.5' in MODELO:
        return (f'Diga como uma narradora brasileira de TikTok, {emocao}, com um sorriso na voz. '
                f'Pronuncie "Stardew Valley" em inglês americano, sem "i" no começo: {fala}')
    return fala
MAX_PPS = 2.95                     # regra: no máximo 3,0 palavras por segundo
API = 'https://generativelanguage.googleapis.com/v1beta/models/'

def curl_json(url, body, tmp):
    """Pede ao Gemini; se a resposta vier vazia ou quebrada (falha de rede), tenta de novo até 4 vezes."""
    import time
    open(tmp, 'w').write(json.dumps(body))
    for k in range(4):
        r = subprocess.run(['curl', '-sS', '--max-time', '300', '-H', 'x-goog-api-key: DUMMY', '-H', 'Content-Type: application/json',
                            '-d', '@' + tmp, url], capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError:
            print('  resposta vazia/quebrada da rede, tentando de novo'); time.sleep(5 * (k + 1))
    return {'error': {'message': 'sem resposta da rede'}}

def dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                capture_output=True, text=True).stdout)

def palavras(t):
    t = re.sub(r'\[[^\]]*\]', '', t).lower()
    t = ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')  # sem acento: "óvni" = "ovni"
    return re.findall(r"[a-z0-9]+", t)

# Voz da ElevenLabs (clone da Yasmin): voz = "el:<voice_id>". Chave no ambiente (o proxy injeta o cabeçalho xi-api-key).
EL_VOZES = {'yaya': 'y3CZa15ewsdFzr1xrpt2'}
def gerar_el(texto, voz, destino, tmpdir):
    vid = EL_VOZES.get(voz[3:], voz[3:])
    if 'no começo: ' in texto: texto = texto.split('no começo: ', 1)[1]   # tira a instrução que o montar() põe pro Gemini
    tx = re.sub(r'\[[^\]]*\]\s*', '', re.sub(r'^\([^)]*\)\s*', '', texto)).strip()
    tx = re.sub(r'Stardew Valley', 'Stardiu Véli', tx)  # testado 09/11: assim sai em inglês (nota 10); escrito normal vira "Valêi"
    body = {"text": tx, "model_id": "eleven_multilingual_v2", "language_code": "pt",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.85, "style": 0.35}}
    open(tmpdir + '/el.json', 'w').write(json.dumps(body))
    for t in range(4):
        r = subprocess.run(['curl', '-sS', '-o', tmpdir + '/el.mp3', '-w', '%{http_code}', '-H', 'xi-api-key: proxy-injected', '-H', 'Content-Type: application/json',
                            '-X', 'POST', f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128', '--data-binary', '@' + tmpdir + '/el.json'], capture_output=True, text=True).stdout
        if r == '200': break
        print('  elevenlabs falhou:', r); import time; time.sleep(10)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmpdir + '/el.mp3',
                    '-af', 'volume=-2dB,highpass=f=80,lowpass=f=12000,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', destino], check=True)

def gerar(texto, voz, destino, tmpdir):
    if voz.startswith('el:'): return gerar_el(texto, voz, destino, tmpdir)
    for tentativa in range(5):
        d = curl_json(API + MODELO + ':generateContent', {
            "contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}, tmpdir + '/r.json')
        if 'candidates' in d: break
        print('  tentativa', tentativa + 1, 'falhou:', str(d)[:160])
        import time; time.sleep(35)  # limite por minuto do plano gratuito (erro 429): espera e tenta de novo
    pcm = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
    open(tmpdir + '/a.pcm', 'wb').write(pcm)
    # áudio do Gemini chega no limite (pico ~0 dB) e com ruído em -57 dB: folga de 4 dB, corta grave/agudo inútil, tira ruído leve, sem compressão com perda
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', tmpdir + '/a.pcm',
                    '-af', 'volume=-4dB,highpass=f=80,lowpass=f=11000,afftdn=nf=-32:tn=1,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ar', '48000', '-c:a', 'pcm_s16le', destino], check=True)

def transcrever(wav, tmpdir):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-ar', '16000', tmpdir + '/t.wav'], check=True)
    b64 = base64.b64encode(open(tmpdir + '/t.wav', 'rb').read()).decode()
    for tentativa in range(5):
        d = curl_json(API + 'gemini-3.8-flash:generateContent', {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": b64}},
              {"text": "Transcreva exatamente o que foi falado, palavra por palavra, incluindo hesitações (ahn, hum) e qualquer palavra extra. Escreva números por extenso (vinte e quatro, não 24). Só o texto."}]}]}, tmpdir + '/t.json')
        if 'candidates' in d: return d['candidates'][0]['content']['parts'][0]['text']
        import time; time.sleep(35)
    return ''

def fala(texto, voz, out, tmpdir):
    """Gera a fala e confere por transcrição: palavra a mais/a menos (ex.: leu a marcação [emoção]) → gera de novo; no fim, tenta sem a marcação."""
    chave = hashlib.sha1(f'{MODELO}|{voz}|{texto}|v3'.encode()).hexdigest()[:12]
    cache = f'{tmpdir}/{chave}.wav'
    if not os.path.exists(cache):
        alvo = palavras(texto)
        sem_tag = re.sub(r'^\[[^\]]*\]\s*', '', texto)
        pedido = montar(texto)
        melhor = None
        for k, tx in enumerate([pedido, pedido, pedido, montar('[animada] ' + sem_tag) if 'pro' in MODELO else sem_tag]):
            tmpw = f'{tmpdir}/{chave}-{k}.wav'
            gerar(tx, voz, tmpw, tmpdir)
            ouvido = palavras(transcrever(tmpw, tmpdir))
            erro = sum(1 for w in ouvido if w not in alvo) + sum(1 for w in alvo if w not in ouvido)
            if melhor is None or erro < melhor[0]: melhor = (erro, tmpw, ' '.join(ouvido))
            if erro == 0: break
            print(f'    ✗ tentativa {k+1}: ouvi "{" ".join(ouvido)}" — gerando de novo')
        if melhor[0] > 0: print(f'    ⚠ ficou com {melhor[0]} diferença(s): "{melhor[2]}"')
        os.replace(melhor[1], cache)
    falado = palavras(texto)
    pps = len(falado) / dur(cache)
    f = min(1.0, MAX_PPS / pps)  # só desacelera, nunca acelera
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', cache, '-af', f'atempo={f:.3f}', '-c:a', 'pcm_s16le', out], check=True)
    return dur(out), len(falado)


def lote(cfg, post, tmpdir):
    """Gera TODAS as falas num pedido só (pausa longa entre elas) e corta nas pausas.
    Economiza cota: 1–2 pedidos por vídeo em vez de 8–15. Volta False se não der certo (aí usa o modo fala a fala)."""
    voz, falas = cfg.get('voz', 'Sulafat'), cfg['falas']
    n = len(falas)
    linhas = []
    for t in falas:
        m = re.match(r'^\[([^\]]*)\]\s*(.*)$', t)
        linhas.append(f'({m.group(1)}) {m.group(2)}' if m else t)
    pedido = ('Narre como uma narradora brasileira de TikTok, com um sorriso na voz. Pronuncie "Stardew Valley" em inglês americano, sem "i" no começo. '
              'Cada linha abaixo é um trecho: siga a emoção indicada entre parênteses, mas NÃO leia o que está entre parênteses. '
              'Entre um trecho e o próximo, faça uma pausa longa e silenciosa de três segundos, maior que qualquer pausa dentro de uma frase.\n\n' + '\n'.join(linhas))
    alvo = [w for t in falas for w in palavras(t)]
    for tentativa in range(2):
        bruto = f'{tmpdir}/lote-{tentativa}.wav'
        d = curl_json(API + MODELO + ':generateContent', {"contents": [{"parts": [{"text": pedido}]}],
              "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}, tmpdir + '/r.json')
        if 'candidates' not in d:
            print('  lote: pedido falhou:', str(d)[:160]); return False
        open(tmpdir + '/a.pcm', 'wb').write(base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data']))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', tmpdir + '/a.pcm',
                        '-af', 'volume=-4dB,highpass=f=80,lowpass=f=11000,afftdn=nf=-32:tn=1', '-ar', '48000', '-c:a', 'pcm_s16le', bruto], check=True)
        ouvido = palavras(transcrever(bruto, tmpdir))
        erro = sum(1 for w in ouvido if w not in alvo) + sum(1 for w in alvo if w not in ouvido)
        r = subprocess.run(['ffmpeg', '-hide_banner', '-i', bruto, '-af', 'silencedetect=noise=-38dB:d=0.22', '-f', 'null', '-'], capture_output=True, text=True).stderr
        ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]
        fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
        total = dur(bruto)
        pausas = [(b - a, (a + b) / 2) for a, b in zip(ini, fim) if a > 0.3 and b < total - 0.3]
        pausas = sorted(sorted(pausas, reverse=True)[:n - 1], key=lambda x: x[1])
        print(f'  lote tentativa {tentativa+1}: {erro} diferença(s), {len(pausas)}/{n-1} pausas')
        if erro > 2 or len(pausas) != n - 1:
            continue
        cortes = [0.0] + [m for _, m in pausas] + [total]
        # confere cada pedaço: tem que ser a fala certa (as pausas mais longas podem cair no meio de uma frase)
        ok = True
        for i in range(n):
            seg = f'{tmpdir}/chk{i}.wav'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-ss', f'{cortes[i]:.3f}', '-to', f'{cortes[i+1]:.3f}', '-c:a', 'pcm_s16le', seg], check=True)
            ouv, esp = palavras(transcrever(seg, tmpdir)), palavras(falas[i])
            e = sum(1 for w in ouv if w not in esp) + sum(1 for w in esp if w not in ouv)
            if e > 1:
                print(f'    pedaço {i+1} não bate: "{" ".join(ouv)}"'); ok = False; break
        if not ok:
            continue
        for i in range(n):
            seg = f'{tmpdir}/seg{i}.wav'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-ss', f'{cortes[i]:.3f}', '-to', f'{cortes[i+1]:.3f}',
                            '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                            '-c:a', 'pcm_s16le', seg], check=True)
            w = palavras(falas[i]); pps = len(w) / max(dur(seg), 0.1); f = min(1.0, MAX_PPS / pps)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', seg, '-af', f'atempo={f:.3f}', '-c:a', 'pcm_s16le', f'{post}/narracao/{i+1:02d}.wav'], check=True)
        return True
    return False

def main(post):
    cfg = json.load(open(f'{post}/narracao.json'))
    voz = cfg.get('voz', 'Sulafat')
    os.makedirs(f'{post}/narracao', exist_ok=True)
    tmpdir = os.environ.get('NARR_TMP', '/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/narr-cache')
    os.makedirs(tmpdir, exist_ok=True)
    durs, palavras_total = [], 0
    if os.environ.get('NARR_MODO', 'lote') == 'lote' and lote(cfg, post, tmpdir):
        print('  narração gerada em lote (1 pedido)')
        for i, t in enumerate(cfg['falas']):
            d = dur(f'{post}/narracao/{i+1:02d}.wav'); w = len(palavras(t))
            durs.append(round(d, 3)); palavras_total += w
            print(f'  cena {i+1}: {d:.2f}s · {w/d:.2f} palavras/s · {t}')
    else:
        print('  modo fala a fala')
        for i, t in enumerate(cfg['falas']):
            d, w = fala(t, voz, f'{post}/narracao/{i+1:02d}.wav', tmpdir)
            durs.append(round(d, 3)); palavras_total += w
            print(f'  cena {i+1}: {d:.2f}s · {w/d:.2f} palavras/s · {t}')
    json.dump({'duracoes': durs, 'falas': cfg['falas']}, open(f'{post}/narracao/duracoes.json', 'w'), ensure_ascii=False)
    subprocess.run(['node', 'tools/video.js', post, '30', '--narr', f'{post}/narracao/duracoes.json'], check=True)
    tempos = json.load(open(f'{post}/tempos.json'))
    # trilha: voz (cada fala no início da sua cena) + efeitos sonoros
    SFX_VOL = {'whoosh': 0.9, 'pop': 0.35, 'tum': 0.4, 'tic': 0.3, 'moedas': 0.35, 'brilho': 0.4}
    ins, filt, rot = [], [], []
    n = 0
    for i, c in enumerate(tempos['cenas']):
        ins += ['-i', f'{post}/narracao/{i+1:02d}.wav']; n += 1
        ms = int(c['fala'] * 1000); filt.append(f'[{n}]adelay={ms}|{ms}[v{i}]'); rot.append(f'[v{i}]')
    for j, e in enumerate(tempos.get('sfx', [])):
        ins += ['-i', f'assets/sfx/{e["som"]}.wav']; n += 1
        ms = int(e['t'] * 1000); filt.append(f'[{n}]volume={SFX_VOL.get(e["som"], 0.3)},adelay={ms}|{ms}[s{j}]'); rot.append(f'[s{j}]')
    filt.append(''.join(rot) + f'amix=inputs={len(rot)}:normalize=0:dropout_transition=0,apad[mix]')
    mix = f'{post}/narracao/mix.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', *ins,
                    '-filter_complex', ';'.join(filt), '-map', '[mix]', '-t', str(tempos['total']), '-c:a', 'pcm_s16le', mix], check=True)
    # volume uniforme: mede e aplica (linear, sem "bombear" as pausas)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', mix, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.89")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-mudo-narr.mp4', '-i', mix, '-af', ln,
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-shortest', '-movflags', '+faststart',
                    f'{post}/video-narrado.mp4'], check=True)
    os.remove(f'{post}/video-mudo-narr.mp4')
    # ritmo final escolhido pela Yasmin (07/11): 1,5x — acelera vídeo e voz juntos, sem afinar a voz (atempo mantém o tom)
    vel = float(cfg.get('velocidade', 1.5))
    if vel != 1.0:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{post}/video-narrado.mp4', '-filter_complex',
                        f'[0:v]setpts=PTS/{vel},fps=30[v];[0:a]atempo={vel}[a]', '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', f'{post}/video-15x.mp4'], check=True)
        print(f'OK {post}/video-15x.mp4 · {dur(post + "/video-15x.mp4"):.1f}s (velocidade {vel}x)')
    total = tempos['total']
    print(f'OK {post}/video-narrado.mp4 · {total:.1f}s · {palavras_total} palavras · média {palavras_total/total:.2f} palavras/s no vídeo')

if __name__ == '__main__':
    main(sys.argv[1].rstrip('/'))
