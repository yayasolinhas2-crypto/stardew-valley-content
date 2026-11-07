# Gera amostras de voz com o TTS do Gemini. Uso: python3 tools/vozes_gemini.py <modelo> Voz1,Voz2,...
# A chave NÃO fica aqui: o proxy do ambiente injeta o header x-goog-api-key (Network secrets).
import json,base64,subprocess,sys,os
OUT='/home/user/stardew-valley-content/vozes'
FRASE='Você pula a tela do fim do dia em Stardew Valley? Então você perdeu isso.'
ESTILO='Diga com energia de criadora de conteúdo do TikTok, sorrindo, sotaque do Brasil: '
VOZES=sys.argv[2].split(',');MODEL=sys.argv[1]
res={}
for v in VOZES:
  body={"contents":[{"parts":[{"text":ESTILO+FRASE}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":v}}}}}
  open('r.json','w').write(json.dumps(body))
  r=subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@r.json',f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'],capture_output=True,text=True)
  d=json.loads(r.stdout)
  if 'candidates' not in d: print(v,'ERRO',str(d)[:300]);continue
  pcm=base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
  open('a.pcm','wb').write(pcm)
  dst=f'{OUT}/voz-{v.lower()}.m4a'
  subprocess.run(['ffmpeg','-y','-loglevel','error','-f','s16le','-ar','24000','-ac','1','-i','a.pcm','-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-14:TP=-1.5','-ar','44100','-c:a','aac','-b:a','128k',dst],check=True)
  dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',dst],capture_output=True,text=True).stdout)
  res[v]=dict(dur=round(dur,2),wps=round(len(FRASE.split())/dur,2),tokens=d.get('usageMetadata',{}).get('totalTokenCount'))
  print(v,res[v],flush=True)
json.dump(res,open(f'{OUT}/medidas.json','w'),indent=1)
