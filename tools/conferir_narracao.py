# Confere a narração final: o Gemini transcreve o áudio do vídeo e compara com o roteiro.
# Uso: python3 tools/conferir_narracao.py posts/005-tela-fim-do-dia
import json,base64,subprocess,sys
post=sys.argv[1].rstrip('/');T='/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/'
roteiro=' '.join(json.load(open(f'{post}/narracao.json'))['falas'])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{post}/video-narrado.mp4','-vn','-ac','1','-ar','16000',T+'conf.wav'],check=True)
b64=base64.b64encode(open(T+'conf.wav','rb').read()).decode()
q=('Transcreva o áudio e compare com o roteiro abaixo. Responda em JSON: {"transcricao":"...", "diferencas":["palavras trocadas, faltando ou a mais"], '
   '"stardew_valley_soa_ingles": true/false, "trechos_estranhos":["pronúncia esquisita, corte, ruído"], "nota_naturalidade":0-10}. Roteiro: '+roteiro)
open(T+'conf.json','w').write(json.dumps({"contents":[{"parts":[{"inlineData":{"mimeType":"audio/wav","data":b64}},{"text":q}]}],"generationConfig":{"responseMimeType":"application/json"}}))
r=subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@'+T+'conf.json',
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent'],capture_output=True,text=True)
d=json.loads(r.stdout);a=json.loads(d['candidates'][0]['content']['parts'][0]['text'])
print(json.dumps({k:v for k,v in a.items() if k!='transcricao'},ensure_ascii=False,indent=1))
