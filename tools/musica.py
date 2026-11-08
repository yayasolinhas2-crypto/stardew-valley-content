# Música de fundo (trilhas originais em assets/trilhas/) nos vídeos e carrosséis.
# Vídeo narrado:  python3 tools/musica.py video posts/001-segredos inverno
#   → guarda o original em video-15x-sem-musica.mp4 (só na 1ª vez) e regrava video-15x.mp4 com a trilha baixinha,
#     abaixando ainda mais quando a voz fala (sidechain). Rodar de novo não duplica a música.
# Carrossel → vídeo:  python3 tools/musica.py carrossel posts/011-vila-real verao
#   → video-carrossel.mp4: cada foto ~3 s, transições, whoosh, trilha em primeiro plano.
import subprocess, sys, os, glob, json
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(*a): subprocess.run(list(a), check=True)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def trilha(nome): return os.path.join(RAIZ, 'assets/trilhas', nome + '.wav')

def video(post, nome):
    v = f'{post}/video-15x.mp4'; orig = f'{post}/video-15x-sem-musica.mp4'
    if not os.path.exists(orig): os.replace(v, orig)
    d = dur(orig)
    fc = ('[1:a]aloop=loop=-1:size=2e9,atrim=0:{d},volume=0.20,afade=t=out:st={fo}:d=1.2,asplit=1[mus];'
          '[0:a]asplit=2[voz][sc];'
          '[mus][sc]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[musd];'
          '[voz][musd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.89[a]').format(d=d, fo=max(0, d - 1.2))
    run('ffmpeg','-y','-loglevel','error','-i',orig,'-i',trilha(nome),'-filter_complex',fc,'-map','0:v','-map','[a]',
        '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',f'{d:.3f}',v)
    print('música ok', post, nome)

def carrossel(post, nome, por=3.0, capa=2.6, tr=0.35):
    fotos = sorted(glob.glob(f'{post}/slides-video/*.png')) or sorted(glob.glob(f'{post}/slides/*.png'))
    n = len(fotos); durs = [capa] + [por] * (n - 1); durs[-1] += 0.8
    ins = []
    for f, dd in zip(fotos, durs): ins += ['-loop', '1', '-t', f'{dd + tr:.3f}', '-i', f]
    efeitos = ['slideleft', 'fade', 'circleopen', 'slideup', 'smoothleft', 'fadewhite', 'wiperight']
    fc = [f'[{i}:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[s{i}]' for i in range(n)]
    acc, t = 's0', 0.0
    for i in range(1, n):
        t += durs[i - 1]
        fc.append(f'[{acc}][s{i}]xfade=transition={efeitos[(i-1) % len(efeitos)]}:duration={tr}:offset={t:.3f}[x{i}]'); acc = f'x{i}'
    total = sum(durs) + tr
    # áudio: trilha + whoosh em cada troca
    ins += ['-i', trilha(nome)]; m = n
    aud = [f'[{m}:a]aloop=loop=-1:size=2e9,atrim=0:{total:.3f},volume=0.9,afade=t=in:d=0.3,afade=t=out:st={total-1.5:.3f}:d=1.5[mu]']; rot = ['[mu]']
    t = 0.0
    for i in range(1, n):
        t += durs[i - 1]; ins += ['-i', os.path.join(RAIZ, 'assets/sfx/whoosh.wav')]; k = m + i
        ms = int((t - 0.05) * 1000); aud.append(f'[{k}:a]volume=0.5,adelay={ms}|{ms}[w{i}]'); rot.append(f'[w{i}]')
    aud.append(''.join(rot) + f'amix=inputs={len(rot)}:normalize=0,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.89[a]')
    run('ffmpeg','-y','-loglevel','error',*ins,'-filter_complex',';'.join(fc + aud),'-map',f'[{acc}]','-map','[a]','-t',f'{total:.3f}',
        '-c:v','libx264','-crf','23','-maxrate','4M','-bufsize','8M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'{post}/video-carrossel.mp4')
    run('ffmpeg','-y','-loglevel','error','-ss','0.2','-i',f'{post}/video-carrossel.mp4','-frames:v','1','-q:v','2',f'{post}/video-carrossel-capa.jpg')
    print('carrossel em vídeo ok', post, f'{total:.1f}s')

if __name__ == '__main__':
    modo, post, nome = sys.argv[1], sys.argv[2].rstrip('/'), sys.argv[3]
    (video if modo == 'video' else carrossel)(post, nome)
