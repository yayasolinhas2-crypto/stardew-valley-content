# Compõe trilhas ORIGINAIS no clima "fazenda aconchegante" (violão dedilhado, flauta, baixo, marimba, chocalho).
# Nada copiado do jogo: progressões comuns de música folk + melodias geradas a partir das notas do acorde (semente fixa).
# Uso: python3 tools/compor_trilha.py  → assets/trilhas/{primavera,verao,outono,inverno}.wav (≈64 s, loop limpo)
import numpy as np, wave, os, random
SR = 44100
NOTA = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)

def pluck(f, dur, bright=0.5, vol=1.0):
    """Corda dedilhada (Karplus-Strong) — violão/banjo."""
    n = int(SR * dur); p = max(2, int(SR / f))
    buf = (np.random.rand(p) * 2 - 1) * vol
    out = np.zeros(n); i = 0
    for k in range(n):
        out[k] = buf[i]
        nxt = buf[(i + 1) % p]
        buf[i] = 0.996 * (bright * buf[i] + (1 - bright) * nxt) if k > p else 0.5 * (buf[i] + nxt)
        i = (i + 1) % p
    return out

def flauta(f, dur, vol=0.25):
    t = np.arange(int(SR * dur)) / SR
    vib = np.sin(2 * np.pi * 5.2 * t) * 0.004 * np.clip(t * 3, 0, 1)
    fase = 2 * np.pi * f * np.cumsum(1 + vib) / SR
    s = np.sin(fase) + 0.18 * np.sin(2 * fase) + 0.06 * np.sin(3 * fase)
    s += np.random.randn(len(t)) * 0.015  # sopro
    env = np.clip(t / 0.06, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    return s * env * vol

def marimba(f, dur, vol=0.3):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)
    return s * np.exp(-t * 6) * vol

def baixo(f, dur, vol=0.45):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return s * np.exp(-t * 3.5) * np.clip(t / 0.01, 0, 1) * vol

def chocalho(dur, vol=0.06):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.random.randn(n); s = np.diff(np.concatenate([[0], s]))  # agudo
    return s * np.exp(-t * 40) * vol

def acorde(nome, oit=4):
    raiz = NOTA[nome.rstrip('m')]; menor = nome.endswith('m')
    base = 12 * (oit + 1) + raiz
    return [base, base + (3 if menor else 4), base + 7]

ESTILOS = {
 'primavera': dict(tom=0, bpm=104, prog=['C','G','Am','F','C','F','G','C'], lead='flauta', seed=11),
 'verao':     dict(tom=2, bpm=112, prog=['C','Am','F','G','C','Em','F','G'], lead='marimba', seed=23),
 'outono':    dict(tom=-3, bpm=92,  prog=['Am','F','C','G','Am','Dm','G','C'], lead='flauta', seed=37),
 'inverno':   dict(tom=5, bpm=84,  prog=['F','C','Dm','A#','F','Gm','C','F'], lead='marimba', seed=51),
}

def compor(nome, cfg, compassos=32):
    random.seed(cfg['seed']); np.random.seed(cfg['seed'])
    bt = 60 / cfg['bpm']; total = int(SR * bt * 4 * compassos) + SR
    mix = np.zeros(total)
    def add(sig, t0):
        i = int(t0 * SR); j = min(total, i + len(sig)); mix[i:j] += sig[:j - i]
    prog = cfg['prog']; tom = cfg['tom']
    padrao_ded = [0, 2, 1, 2, 0, 2, 1, 2]           # dedilhado em colcheias
    ritmos = [[1, 1, 2], [2, 1, 1], [1, .5, .5, 2], [3, 1], [2, 2], [1, 1, 1, 1]]
    ult = None
    for c in range(compassos):
        nome_ac = prog[c % len(prog)]
        notas = [m + tom for m in acorde(nome_ac, 3)]
        t0 = c * 4 * bt
        # violão dedilhado
        for k, idx in enumerate(padrao_ded):
            nota = notas[idx] + (12 if k in (3, 7) else 0)
            add(pluck(hz(nota), bt * 1.6, bright=0.45, vol=0.22), t0 + k * bt / 2)
        # baixo: tônica e quinta
        add(baixo(hz(notas[0] - 12), bt * 1.8), t0); add(baixo(hz(notas[2] - 12), bt * 1.8, 0.35), t0 + 2 * bt)
        # chocalho leve nos contratempos (a partir do 3º compasso)
        if c >= 2:
            for k in range(4): add(chocalho(0.08), t0 + k * bt + bt / 2)
        # melodia: entra no compasso 4, respira a cada 4 compassos
        if c >= 3 and c % 8 != 7:
            tons = [m + 12 for m in notas] + [notas[0] + 24]
            escala = sorted(set([n for n in range(notas[0] + 10, notas[0] + 27) if (n - (60 + tom)) % 12 in (0, 2, 4, 5, 7, 9, 11)]))
            r = random.choice(ritmos); tt = t0
            for k, d in enumerate(r):
                if k == 0 or random.random() < 0.6: alvo = random.choice(tons)
                else: alvo = random.choice(escala)
                if ult is not None and abs(alvo - ult) > 7: alvo = ult + (5 if alvo > ult else -5)
                alvo = min(max(alvo, notas[0] + 10), notas[0] + 26); ult = alvo
                dur = d * bt
                if cfg['lead'] == 'flauta': add(flauta(hz(alvo), dur * 0.95), tt)
                else: add(marimba(hz(alvo), dur * 1.2), tt); add(marimba(hz(alvo + 12), dur, 0.06), tt)
                tt += dur
    # leve "sala": eco curto
    eco = np.zeros_like(mix); d = int(SR * 0.11); eco[d:] = mix[:-d] * 0.18
    mix = mix + eco
    mix /= np.max(np.abs(mix)) * 1.12
    # fade in/out curtos para emendar em loop
    f = int(SR * 0.5); mix[:f] *= np.linspace(0, 1, f); mix[-SR:] *= np.linspace(1, 0, SR)
    os.makedirs('assets/trilhas', exist_ok=True)
    with wave.open(f'assets/trilhas/{nome}.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print(nome, round(len(mix) / SR, 1), 's')

if __name__ == '__main__':
    for n, c in ESTILOS.items(): compor(n, c)
