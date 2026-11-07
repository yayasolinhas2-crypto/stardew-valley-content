# Funções de teste de voz: tts() gera áudio no Gemini; julgar() pede ao Gemini nota de pronúncia/idade. Chave vem do proxy (Network secrets).
import json,base64,subprocess,sys
def tts(text,voice,out,model='gemini-2.5-flash-preview-tts'):
  body={"contents":[{"parts":[{"text":text}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":voice}}}}}
  open('r.json','w').write(json.dumps(body))
  d=json.loads(subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@r.json',f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'],capture_output=True,text=True).stdout)
  pcm=base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
  open('a.pcm','wb').write(pcm)
  subprocess.run(['ffmpeg','-y','-loglevel','error','-f','s16le','-ar','24000','-ac','1','-i','a.pcm','-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-14:TP=-1.5','-ar','44100','-c:a','libmp3lame','-b:a','128k',out],check=True)
def julgar(path,pergunta):
  subprocess.run(['ffmpeg','-y','-loglevel','error','-i',path,'-ac','1','-ar','16000','q.wav'],check=True)
  b64=base64.b64encode(open('q.wav','rb').read()).decode()
  body={"contents":[{"parts":[{"inlineData":{"mimeType":"audio/wav","data":b64}},{"text":pergunta}]}],"generationConfig":{"responseMimeType":"application/json"}}
  open('q.json','w').write(json.dumps(body))
  d=json.loads(subprocess.run(['curl','-sS','-H','x-goog-api-key: DUMMY','-H','Content-Type: application/json','-d','@q.json','https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent'],capture_output=True,text=True).stdout)
  return json.loads(d['candidates'][0]['content']['parts'][0]['text'])
