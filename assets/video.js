// Motor dos vídeos (1080x1920). Cada <section class="scene" data-in data-out data-tr> é uma cena;
// cada elemento com data-in (s) e data-fx anima. seek(t) desenha o quadro t (determinístico).
// Transições (data-tr na cena): chicote · flash · iris · zoom · cortina  (a cena anterior continua visível embaixo durante a troca)
// fx: pop · up · left · fade · drop · stamp · light · type · count · wave · wobble · move (data-from="x,y" data-to="x,y" data-d=s [data-wob=graus])
// Troca de imagem: data-swap="t" data-swapsrc="nova.png". Animação por quadros: data-anim="pasta/Nome" data-n data-ms → Nome_00.png...
// Efeitos sonoros: o renderizador lê window.SFX() → [{t, som}] (whoosh nas transições, pop em stamp/pop de destaque, brilho no nº 1).
(function(){
  const TR=0.32;
  const clamp=x=>Math.max(0,Math.min(1,x));
  const easeOut=x=>1-Math.pow(1-x,3);
  const back=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const scenes=[...document.querySelectorAll('.scene')];
  scenes.forEach((s,i)=>{s.style.zIndex=10+i;if(!s.dataset.tr)s.dataset.tr=['chicote','flash','iris','zoom','cortina'][i%5];
    const f=document.createElement('div');f.className='flashov';f.style.cssText='position:absolute;inset:0;background:#fff8e0;opacity:0;pointer-events:none;z-index:99';s.appendChild(f)});
  const els=[...document.querySelectorAll('[data-fx]')];
  els.forEach(e=>{if(e.dataset.fx==='type'){e.dataset.text=e.dataset.text||e.textContent;e.textContent=''}});
  const anims=[...document.querySelectorAll('[data-anim]')];
  anims.forEach(e=>{for(let i=0;i<+e.dataset.n;i++){const im=new Image();im.src=`${e.dataset.anim}_${String(i).padStart(2,'0')}.png`}});
  const swaps=[...document.querySelectorAll('[data-swap]')];
  swaps.forEach(e=>{e.dataset.orig=e.getAttribute('src');const im=new Image();im.src=e.dataset.swapsrc});
  window.seek=function(t){
    scenes.forEach((s,i)=>{
      const a=+s.dataset.in,b=+s.dataset.out;
      const prox=scenes[i+1];const fimTroca=prox?+prox.dataset.in+TR:b;
      s.style.visibility=(t>=a&&t<Math.max(b,fimTroca))?'visible':'hidden';
      const p=a>0?clamp((t-a)/TR):1,q=easeOut(p),tr=s.dataset.tr;
      let tf='none',fl=0,cp='none',op=1,fx='none';
      if(p<1){
        if(tr==='chicote'){tf=`translateX(${(1-q)*1080}px)`;fx=`blur(${(1-q)*14}px)`}
        else if(tr==='flash'){fl=1-p}
        else if(tr==='iris'){cp=`circle(${q*120}% at 50% 45%)`}
        else if(tr==='zoom'){tf=`scale(${1.35-0.35*q})`;op=q}
        else if(tr==='cortina'){cp=`inset(0 0 ${(1-q)*100}% 0)`}
      }
      s.style.transform=tf;s.style.clipPath=cp;s.style.opacity=op;s.style.filter=fx;
      s.querySelector('.flashov').style.opacity=fl;
    });
    for(const e of els){
      const a=+e.dataset.in,fx=e.dataset.fx,p=clamp((t-a)/.35),q=easeOut(p);let o=1,tr='';
      if(fx==='pop'){o=p>0?1:0;tr=`scale(${p>0?back(p):0})`}
      else if(fx==='up'){o=q;tr=`translateY(${(1-q)*60}px)`}
      else if(fx==='left'){o=q;tr=`translateX(${(1-q)*-120}px)`}
      else if(fx==='fade'){o=q}
      else if(fx==='drop'){o=p>0?1:0;tr=`translateY(${(1-q)*-260}px)`}
      else if(fx==='stamp'){o=p>0?1:0;tr=`scale(${p>0?1+(1-q)*.9:0}) rotate(${e.dataset.rot||(e.classList.contains('tag')?-3:0)}deg)`}
      else if(fx==='light'){e.classList.toggle('lit',t>=a);continue}
      else if(fx==='type'){const s=e.dataset.text;e.textContent=s.slice(0,Math.round(clamp((t-a)/.45)*s.length));continue}
      else if(fx==='move'){const [x0,y0]=e.dataset.from.split(',').map(Number),[x1,y1]=e.dataset.to.split(',').map(Number);const k=clamp((t-a)/(+e.dataset.d||2));
        o=t>=a?1:0;e.style.left=(x0+(x1-x0)*k)+'px';e.style.top=(y0+(y1-y0)*k)+'px';if(e.dataset.wob)tr=`rotate(${Math.sin((t-a)*12)*(+e.dataset.wob)}deg)`}
      else if(fx==='count'){const to=+e.dataset.to;e.textContent=Math.round(clamp((t-a)/1.0)*to).toLocaleString('pt-BR')+(e.dataset.suf??'g');e.style.opacity=t>=a?1:0;continue}
      else if(fx==='wave'){o=t>=a?1:0;[...e.children].forEach((c,i)=>c.style.transform=`translateY(${Math.sin(t*6+i*.8)*22}px)`)}
      else if(fx==='wobble'){o=q;tr=`rotate(${Math.sin((t-a)*10)*6}deg)`}
      e.style.opacity=o;e.style.transform=tr;
    }
    for(const e of anims){const n=+e.dataset.n,ms=+e.dataset.ms;const i=Math.floor(t*1000/ms)%n;
      const src=`${e.dataset.anim}_${String(i).padStart(2,'0')}.png`;if(e.getAttribute('src')!==src)e.setAttribute('src',src)}
    for(const e of swaps){const src=t>=+e.dataset.swap?e.dataset.swapsrc:e.dataset.orig;if(e.getAttribute('src')!==src)e.setAttribute('src',src)}
    if(window.onSeek)window.onSeek(t);
  };
  // lista de efeitos sonoros em tempo de vídeo original
  window.SFX=function(){
    const out=[];
    scenes.forEach((s,i)=>{if(i>0)out.push({t:+s.dataset.in,som:'whoosh'})});
    els.forEach(e=>{const a=+e.dataset.in,fx=e.dataset.fx;
      if(fx==='stamp')out.push({t:a,som:'pop'});
      else if(fx==='drop')out.push({t:a+0.3,som:'tum'});
      else if(fx==='light')out.push({t:a,som:'tic'});
      else if(fx==='count')out.push({t:a,som:'moedas'});
    });
    const ult=scenes[scenes.length-2];if(ult)out.push({t:+ult.dataset.in+0.1,som:'brilho'});
    return out.sort((x,y)=>x.t-y.t);
  };
  window.addEventListener('load',()=>seek(0));
})();
