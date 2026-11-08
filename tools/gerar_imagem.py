# Gera imagens realistas com o Gemini (modelo de imagem). Uso: python3 tools/gerar_imagem.py <pasta_saida> <arquivo_prompts.json>
# prompts.json = {"nome": "prompt", ...}. A chave do Gemini vem do proxy (Network secrets), nunca fica aqui.
import json,subprocess,base64,sys,os,time
out,pf=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True)
BASE=("Photorealistic vertical photograph, shot on a phone, real life, natural light, highly detailed, no cartoon, no pixel art. "
      "Any visible signs or text must be in Brazilian Portuguese. Do not include logos. Scene: ")
for nome,p in json.load(open(pf)).items():
  dst=f'{out}/{nome}.jpg'
  if os.path.exists(dst): print(nome,'já existe');continue
  body={"contents":[{"parts":[{"text":BASE+p}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"9:16"}}}
  for t in range(4):
    open('/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/img_r.json','w').write(json.dumps(body))
    d=json.loads(subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@/tmp/claude-0/-home-user-stardew-valley-content/390e979c-f63f-5f31-9eff-bd01428cedcb/scratchpad/img_r.json',
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent'],capture_output=True,text=True).stdout)
    parts=[p for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]) if 'inlineData' in p] if 'candidates' in d else []
    if parts:
      open(dst,'wb').write(base64.b64decode(parts[0]['inlineData']['data']));print(nome,'OK');break
    print(nome,'falhou:',json.dumps(d)[:200]);time.sleep(30)
