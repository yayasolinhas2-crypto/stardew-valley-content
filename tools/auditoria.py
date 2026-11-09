# Auditoria geral: python3 tools/auditoria.py <dump_do_painel>/posts
# Confere fila do Metricool, mídia, capa (1º quadro), duração, resolução, áudio, área segura da legenda, agenda (1 post por horário) e painel x agendados.
import json, glob, os, sys, subprocess, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
prob, ok = [], []
def P(m): prob.append(m)
def probe(f):
    j = json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate:format=duration','-of','json',f],capture_output=True,text=True).stdout)
    v = [s for s in j['streams'] if s['codec_type']=='video']; a = [s for s in j['streams'] if s['codec_type']=='audio']
    return float(j['format']['duration']), (v[0]['width'], v[0]['height']) if v else None, bool(a)
def loud(f):
    e = subprocess.run(['ffmpeg','-hide_banner','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    i = [l for l in e.split('\n') if l.strip().startswith('I:')]
    return float(i[-1].split()[1]) if i else None
def quadro0_vazio(f):
    # capa: o 1º quadro precisa ter conteúdo (variação de cor), não cartão liso
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-frames:v','1','-vf','scale=108:192','/tmp/q0.png'])
    from PIL import Image, ImageStat
    s = ImageStat.Stat(Image.open('/tmp/q0.png').convert('L'));return s.stddev[0] < 25
posts = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(sys.argv[1]+'/*.json')}
fila = json.load(open('metricool/fila.json')); ag = json.load(open('metricool/agendados.json'))
agora = dt.datetime.now(dt.timezone.utc)
# 1) fila
for x in fila['posts']:
    for m in x['midia_no_repositorio'] + [x['capa']['imagem']]:
        if not os.path.exists(m): P(f'FILA {x["id"]}: arquivo não existe {m}')
        elif subprocess.run(['git','ls-files','--error-unmatch',m],capture_output=True).returncode: P(f'FILA {x["id"]}: arquivo fora do git {m}')
    if 'ALTERNATIVA' in x['titulo']: P(f'FILA {x["id"]}: título com ALTERNATIVA')
    if 'comenta' in x['legenda'].lower(): P(f'FILA {x["id"]}: legenda com "comenta"')
    if len(x['legenda']) > 2200: P(f'FILA {x["id"]}: legenda longa demais')
# 2) vídeos que vão sair (fila + agendados futuros do painel)
saem = {}
for pid, p in posts.items():
    if p.get('status') in ('aprovado','agendado') and p.get('data'):
        q = dt.datetime.fromisoformat(f"{p['data']}T{p['hora']}:00-03:00")
        if q > agora: saem[pid] = p
slots = {}
for pid, p in saem.items(): slots.setdefault((p['data'],p['hora']),[]).append(pid)
for k, v in slots.items():
    if len(v) > 1: P(f'AGENDA {k}: {len(v)} posts no mesmo horário: {v}')
for pid, p in sorted(saem.items(), key=lambda x:(x[1]['data'],x[1]['hora'])):
    f = p.get('video_repo')
    if not f:
        num = p['num'][:3]; d = sorted(glob.glob(f'posts/{num}-*'))
        if not d: P(f'{pid}: pasta não achada'); continue
        if p.get('video'):
            cand = [c for c in ['video-15x.mp4','video-carrossel.mp4','video-guia.mp4'] if os.path.exists(f'{d[0]}/{c}')]
            if 'carrossel' in (p.get('categoria','')+p.get('video','')) and os.path.exists(f'{d[0]}/video-carrossel.mp4'): cand=['video-carrossel.mp4']
            if 'guia' in p.get('categoria','') and os.path.exists(f'{d[0]}/video-guia.mp4'): cand=['video-guia.mp4']
            f = f'{d[0]}/{cand[0]}' if cand else None
    if not f or not os.path.exists(f): P(f'{pid}: vídeo não achado ({f})'); continue
    dur, res, aud = probe(f)
    if res != (1080,1920): P(f'{pid}: resolução {res}')
    if not aud: P(f'{pid}: SEM ÁUDIO')
    if dur > 35.5: P(f'{pid}: {dur:.1f}s (passa de 35 s)')
    if quadro0_vazio(f): P(f'{pid}: 1º quadro parece vazio (capa bugada)')
    L = loud(f)
    if L is None or not (-17 <= L <= -11): P(f'{pid}: volume {L} LUFS (esperado ~-14)')
    ok.append(f'{p["data"][8:]}/{p["data"][5:7]} {p["hora"]} {pid}: {dur:.1f}s {L} LUFS ✓')
# 3) painel x Metricool
ids_ag = {}
for r in ag.get('agendados', []): ids_ag.setdefault(r['id'], r)
for pid, p in saem.items():
    if p['status']=='agendado' and pid not in ids_ag: P(f'{pid}: painel diz agendado mas não está em agendados.json')
    if p['status']=='agendado' and pid in ids_ag and ids_ag[pid]['quando_brasilia'] != f"{p['data']} {p['hora']}": P(f'{pid}: horário diferente painel {p["data"]} {p["hora"]} x Metricool {ids_ag[pid]["quando_brasilia"]}')
fila_ids = {x['id'].split('→')[-1] for x in fila['posts']}
for pid, p in saem.items():
    if p['status']=='aprovado' and pid not in fila_ids: P(f'{pid}: aprovado mas fora da fila')
for r in ag.get('agendados', []):
    pid = r['id'].split('→')[-1]
    if r.get('status')=='agendado' and r['quando_brasilia'] > (agora - dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M'):
        if posts.get(pid,{}).get('status') == 'negado': P(f'METRICOOL: {pid} está NEGADO no painel mas agendado no Metricool ({r["quando_brasilia"]})')
print('\n'.join(ok)); print('\nPROBLEMAS:' if prob else '\nNenhum problema.'); print('\n'.join(prob))
