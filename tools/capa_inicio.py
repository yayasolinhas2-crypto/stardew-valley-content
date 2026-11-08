# Coloca a capa (quadro com o título completo) nos primeiros 0,6 s do vídeo — o post não começa "do nada".
# Uso: python3 tools/capa_inicio.py posts/009-erros-iniciante [segundo_da_capa=2.0]
import subprocess,sys,os
post=sys.argv[1].rstrip('/');t=sys.argv[2] if len(sys.argv)>2 else '2.0'
v=f'{post}/video-15x.mp4';tmp=f'{post}/_c.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',t,'-i',v,'-frames:v','1','-q:v','2',f'{post}/video-capa.jpg'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-t','0.6','-i',f'{post}/video-capa.jpg','-f','lavfi','-t','0.6','-i','anullsrc=r=48000:cl=stereo','-i',v,
  '-filter_complex','[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[c];[2:v]fps=30,format=yuv420p,setsar=1[m];[c][1:a][m][2:a]concat=n=2:v=1:a=1[v][a]',
  '-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',tmp],check=True)
os.replace(tmp,v);print('capa ok',post)
