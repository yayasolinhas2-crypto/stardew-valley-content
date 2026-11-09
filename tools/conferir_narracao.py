# Confere a narração final: o Gemini transcreve o áudio do vídeo e compara com o roteiro.
# Uso: python3 tools/conferir_narracao.py posts/005-tela-fim-do-dia
import json,base64,subprocess,sys
post=sys.argv[1].rstrip('/');T='/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/'
import re
import os
falas=json.load(open(f'{post}/narracao.json'))['falas'] if os.path.exists(f'{post}/narracao.json') else [c['fala'] for c in json.load(open(f'{post}/gameplay.json'))['cenas']]
roteiro=re.sub(r'\[[^\]]*\]\s*','',' '.join(falas))
ARQ=sys.argv[2] if len(sys.argv)>2 else 'video-narrado.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{post}/{ARQ}','-vn','-ac','1','-ar','16000',T+'conf.wav'],check=True)
b64=base64.b64encode(open(T+'conf.wav','rb').read()).decode()
q=('Transcreva o áudio e compare com o roteiro abaixo. Responda em JSON: {"transcricao":"...", "diferencas":["palavras trocadas, faltando ou a mais"], '
   '"stardew_valley_soa_ingles": true/false, "trechos_estranhos":["pronúncia esquisita, corte, ruído, chiado"], "leu_marcacao_entre_colchetes": true/false, "nota_naturalidade":0-10, "nota_emocao":0-10 (0=monótona, 10=narradora empolgada de TikTok), "chiado":0-10 (0=limpo)}. Roteiro: '+roteiro)
open(T+'conf.json','w').write(json.dumps({"contents":[{"parts":[{"inlineData":{"mimeType":"audio/wav","data":b64}},{"text":q}]}],"generationConfig":{"responseMimeType":"application/json"}}))
r=subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@'+T+'conf.json',
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent'],capture_output=True,text=True)
d=json.loads(r.stdout);a=json.loads(d['candidates'][0]['content']['parts'][0]['text'])
print(json.dumps({k:v for k,v in a.items() if k!='transcricao'},ensure_ascii=False,indent=1))
