# Capas dos Destaques do Instagram (1080x1920; o Instagram mostra só o círculo do meio).
# Mesmo fundo e moldura da foto de perfil (lupa, pôr do sol). Ícones: arte do jogo (wiki) ampliada sem borrar.
from PIL import Image, ImageDraw
import random
S_W,S_H=1080,1920
def fundo(top=(90,58,140),bot=(243,154,123)):
  im=Image.new('RGB',(S_W,S_H));d=ImageDraw.Draw(im)
  for y in range(S_H):
    t=y/S_H;d.line([(0,y),(S_W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
  random.seed(5)
  for _ in range(60):
    x=random.randrange(0,S_W//12)*12;y=random.randrange(0,S_H//12)*12;s=random.choice([12,12,18])
    d.rectangle([x,y,x+s-1,y+s-1],fill=(255,233,138) if s>12 else (255,248,208))
  return im
def capa(icone,saida,escala):
  im=fundo();d=ImageDraw.Draw(im);cx,cy=S_W//2,S_H//2
  for r,c in [(470,(91,42,12)),(456,(201,106,27)),(442,(91,42,12))]:
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=c,width=14)
  ic=Image.open(icone).convert('RGBA');ic=ic.resize((ic.width*escala,ic.height*escala),Image.NEAREST)
  im.paste(ic,(cx-ic.width//2,cy-ic.height//2),ic);im.save(saida)
import os;os.makedirs('branding/destaques',exist_ok=True)
capa('assets/anim/Secret_Note.png','branding/destaques/recados.png',8)      # 64px → 512
capa('assets/icons/Junimo_Plush.png','branding/destaques/segredos.png',5)   # 96px → 480
capa('assets/icons/Pearl.png','branding/destaques/guias.png',10)           # 48px → 480
capa('assets/icons/Keg.png','branding/destaques/dinheiro.png',5)           # 48x96 → 240x480
# prévia: como aparece no perfil (círculos pequenos)
prev=Image.new('RGB',(4*230+40,300),(0,0,0));m=Image.new('L',(190,190),0);ImageDraw.Draw(m).ellipse([0,0,189,189],fill=255)
dd=ImageDraw.Draw(prev)
for i,n in enumerate(['segredos','recados','guias','dinheiro']):
  c=Image.open(f'branding/destaques/{n}.png').crop((S_W//2-470,S_H//2-470,S_W//2+470,S_H//2+470)).resize((190,190))
  prev.paste(c,(30+i*230,20),m)
prev.save('branding/destaques/previa.png')
print('ok')
