# Gera metricool/fila.json (os posts que a Yasmin APROVOU no painel e ainda não saíram) a partir de um dump do banco do painel.
# Uso: python3 tools/exportar_fila.py <pasta_dump>/posts
import json,glob,os,sys,datetime as dt
DIR={'001':'001-segredos','002':'002-presentes','003':'003-barril-ou-jarra','004':'004-peixes-lendarios','005':'005-tela-fim-do-dia','006':'006-criaturas',
     '007':'007-recados-ep1','008':'008-recados-ep2','009':'009-erros-iniciante','010':'010-construcoes','011':'011-vila-real','012':'012-festivais-real',
     '013':'013-todo-dia','014':'014-mochila','015':'015-carrinho','016':'016-presente-do-pet','017':'017-maquina-de-costura','018':'018-torneirinha'}
agora=dt.datetime.now(dt.timezone.utc)
fila=[];SUBST={}
for f in sorted(glob.glob(sys.argv[1]+'/*.json')):
  p=json.load(open(f));pid=os.path.basename(f)[:-5]
  if p.get('status')!='aprovado':continue
  # versão ALTERNATIVA aprovada (ex.: p020n no lugar da p020v): substitui a original no mesmo horário, nunca sai duplicada
  if p.get('alternativa_de'):
    orig_f=os.path.join(os.path.dirname(f),p['alternativa_de']+'.json')
    orig=json.load(open(orig_f)) if os.path.exists(orig_f) else {}
    if orig.get('status')=='agendado' and orig.get('metricool'): p['substitui_metricool']=orig['metricool']
    elif orig.get('status')=='aprovado': SUBST[p['alternativa_de']]=pid
    else: continue
    pid=p['alternativa_de']+'→'+pid
  quando=dt.datetime.fromisoformat(f"{p['data']}T{p['hora']}:00-03:00")
  if quando<agora:continue
  base=DIR.get(p['num'][:3]) or os.path.basename(sorted(glob.glob(f"posts/{p['num'][:3]}-*"))[0]);video=bool(p.get('video'))
  midia=[p['video_repo']] if p.get('video_repo') else [f'posts/{base}/video-15x.mp4'] if video else [f'posts/{base}/slides/{os.path.basename(s)}' for s in p['slides']]
  for m in midia: assert os.path.exists(m),m
  ia='IA' in p.get('titulo','') or 'IA' in p.get('categoria','')
  fila.append({'id':pid,'titulo':p['titulo'].replace(' (marcar como IA)','').replace(' · marcar como IA',''),'quando_brasilia':f"{p['data']} {p['hora']}",'fuso':'America/Sao_Paulo',
    'formato':'video' if video else 'carrossel_fotos','redes':['tiktok','instagram'] if video else ['tiktok'],
    'midia_no_repositorio':midia,'legenda':p['legenda'],'comentario_fixado':p['fixado'],'conteudo_gerado_por_ia':ia,'status':'pronto_para_agendar',
    **({'capa':{'segundo_do_video':0.0,'imagem':(p['video_repo'].replace('.mp4','-capa.jpg') if p.get('video_repo') and os.path.exists(p['video_repo'].replace('.mp4','-capa.jpg')) else f'posts/{base}/video-capa.jpg')}} if video else {}),
    **({'substituir_metricool_post_id':p['substitui_metricool'],'acao':'EDITAR o post agendado com esse id no Metricool (mesmo horário): trocar mídia, legenda, redes e título por esta versão nova'} if p.get('substitui_metricool') else {})})
# original ainda não agendada e com alternativa aprovada: sai só a alternativa
fila=[x for x in fila if x['id'] not in SUBST]
fila.sort(key=lambda x:x['quando_brasilia'])
anterior=json.load(open('metricool/fila.json')) if os.path.exists('metricool/fila.json') else {}
saida={'atualizado_em':agora.isoformat(timespec='seconds'),'gerado_por':'Claude da Yasmin (a partir das aprovações dela no painel)','posts':fila}
if anterior.get('recado_para_claude_do_vitor'):saida={'recado_para_claude_do_vitor':anterior['recado_para_claude_do_vitor'],**saida}
json.dump(saida,open('metricool/fila.json','w'),ensure_ascii=False,indent=1)
print(len(fila),'posts na fila');[print(' ',x['quando_brasilia'],x['id'],x['formato'],x['redes']) for x in fila]
