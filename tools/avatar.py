# Desenha os ícones de perfil em pixel art (arte original, sem sprites do jogo).
from PIL import Image, ImageDraw
import random
C={'O':(59,29,7),'P':(251,224,168),'S':(226,184,118),'R':(184,48,15),'r':(232,98,60),'D':(120,22,8),
   'G':(255,216,74),'g':(217,165,32),'W':(255,255,255),'B':(150,205,240),'b':(95,150,200),'K':(107,54,19),'k':(160,90,31)}
ENVELOPE=[
"OOOOOOOOOOOOOOOOOO",
"OPSPPPPPPPPPPPPSPO",
"OPPSPPPPPPPPPPSPPO",
"OPPPSPPPPPPPPSPPPO",
"OPPPPSPPPPPPSPPPPO",
"OPPPPPSPPPPSPPPPPO",
"OPPPPPPRRRRPPPPPPO",
"OPPPPPRrrRRRPPPPPO",
"OPPPPPRrRRRRPPPPPO",
"OPPPPPRRRRRDPPPPPO",
"OPPPPSPRRRDPSPPPPO",
"OPPPSPPPPPPPPSPPPO",
"OPPSPPPPPPPPPPSPPO",
"OOOOOOOOOOOOOOOOOO"]
LUPA=[
"....OOOOOO.......",
"..OOBBBBBBOO.....",
".OBWWBBBBBBbO....",
".OBWBBBBBBBbO....",
"OBBBBBBBBBBbbO...",
"OBBBBBBBBBBbbO...",
"OBBBBBBBBBbbbO...",
"OBBBBBBBBBbbbO...",
".ObBBBBBBbbbO....",
".ObbbBBbbbbbO....",
"..OObbbbbbOOkO...",
"....OOOOOO.OKkO..",
"............OKkO.",
".............OKkO",
"..............OKO",
"...............O."]
def sprite(rows,scale):
  w=len(rows[0]);h=len(rows);im=Image.new('RGBA',(w*scale,h*scale),(0,0,0,0));d=ImageDraw.Draw(im)
  for y,r in enumerate(rows):
    for x,c in enumerate(r):
      if c in C:d.rectangle([x*scale,y*scale,(x+1)*scale-1,(y+1)*scale-1],fill=C[c])
  return im
def fundo(top,bot,stars=True,seed=3):
  S=1080;im=Image.new('RGB',(S,S));d=ImageDraw.Draw(im)
  for y in range(S):
    t=y/S;d.line([(0,y),(S,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
  random.seed(seed)
  if stars:
    for _ in range(38):
      x=random.randrange(0,S//12)*12;y=random.randrange(0,S//12)*12;s=random.choice([12,12,18])
      d.rectangle([x,y,x+s-1,y+s-1],fill=(255,233,138) if s>12 else (255,248,208))
  return im
def estrela(d,cx,cy,u,cor):
  for dx,dy in [(0,-2),(0,-1),(0,0),(0,1),(0,2),(-1,0),(-2,0),(1,0),(2,0)]:
    d.rectangle([cx+dx*u,cy+dy*u,cx+dx*u+u-1,cy+dy*u+u-1],fill=cor)
def moldura(im):
  d=ImageDraw.Draw(im);S=im.size[0]
  # anel de madeira estilo menu (dentro do recorte circular)
  for r,c in [(520,(91,42,12)),(506,(201,106,27)),(492,(91,42,12))]:
    d.ellipse([S/2-r,S/2-r,S/2+r,S/2+r],outline=c,width=14)
  return im
# Opção A: recado secreto (envelope com selo) no céu noturno
a=fundo((20,22,64),(75,79,176));sp=sprite(ENVELOPE,40);a.paste(sp,((1080-sp.width)//2,(1080-sp.height)//2+30),sp)
d=ImageDraw.Draw(a);estrela(d,250,250,18,(255,216,74));estrela(d,820,300,14,(255,248,208));moldura(a);a.save('avatar-A-recado.png')
# Opção B: lupa sobre o céu (investigar segredos)
b=fundo((90,58,140),(243,154,123));sp=sprite(LUPA,40);b.paste(sp,((1080-sp.width)//2+20,(1080-sp.height)//2),sp)
d=ImageDraw.Draw(b);estrela(d,445,440,22,(255,216,74));moldura(b);b.save('avatar-B-lupa.png')
# Prévia: como aparece no TikTok (círculo pequeno)
prev=Image.new('RGB',(760,400),(18,18,18));m=Image.new('L',(300,300),0);ImageDraw.Draw(m).ellipse([0,0,299,299],fill=255)
for i,f in enumerate(['avatar-A-recado.png','avatar-B-lupa.png']):
  prev.paste(Image.open(f).resize((300,300)),(50+i*360,50),m)
prev.save('previa-avatares.png')
