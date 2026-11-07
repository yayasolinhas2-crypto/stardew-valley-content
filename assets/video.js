// Motor dos vídeos (1080x1920). Cada <section class="scene" data-in data-out> é uma cena;
// cada elemento com data-in (s) e data-fx anima. seek(t) desenha o quadro t (determinístico).
// fx: pop · up · left · fade · drop · stamp · light · type · move (data-from="x,y" data-to="x,y" data-d=s) · wobble
// Animação por quadros: <img data-anim="assets/anim/Nome" data-n="4" data-ms="400"> → Nome_00.png, Nome_01.png...
(function(){
  const clamp=x=>Math.max(0,Math.min(1,x));
  const easeOut=x=>1-Math.pow(1-x,3);
  const back=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const els=[...document.querySelectorAll('[data-fx]')];
  els.forEach(e=>{if(e.dataset.fx==='type'){e.dataset.text=e.dataset.text||e.textContent;e.textContent=''}});
  const anims=[...document.querySelectorAll('[data-anim]')];
  anims.forEach(e=>{for(let i=0;i<+e.dataset.n;i++){const im=new Image();im.src=`${e.dataset.anim}_${String(i).padStart(2,'0')}.png`}});
  window.seek=function(t){
    document.querySelectorAll('.scene').forEach(s=>{
      const a=+s.dataset.in,b=+s.dataset.out;s.style.visibility=(t>=a&&t<b)?'visible':'hidden';
      const p=clamp((t-a)/.22);s.style.transform=a>0?`translateX(${(1-easeOut(p))*1080}px)`:'none';
    });
    for(const e of els){
      const a=+e.dataset.in,fx=e.dataset.fx,p=clamp((t-a)/.35),q=easeOut(p);let o=1,tr='';
      if(fx==='pop'){o=p>0?1:0;tr=`scale(${p>0?back(p):0})`}
      else if(fx==='up'){o=q;tr=`translateY(${(1-q)*60}px)`}
      else if(fx==='left'){o=q;tr=`translateX(${(1-q)*-120}px)`}
      else if(fx==='fade'){o=q}
      else if(fx==='drop'){o=p>0?1:0;tr=`translateY(${(1-q)*-260}px)`}
      else if(fx==='stamp'){o=p>0?1:0;tr=`scale(${p>0?1+(1-q)*.9:0}) rotate(${e.dataset.rot||0}deg)`}
      else if(fx==='light'){e.classList.toggle('lit',t>=a);continue}
      else if(fx==='type'){const s=e.dataset.text;e.textContent=s.slice(0,Math.round(clamp((t-a)/.45)*s.length));continue}
      else if(fx==='move'){const [x0,y0]=e.dataset.from.split(',').map(Number),[x1,y1]=e.dataset.to.split(',').map(Number);const k=clamp((t-a)/(+e.dataset.d||2));
        o=t>=a?1:0;e.style.left=(x0+(x1-x0)*k)+'px';e.style.top=(y0+(y1-y0)*k)+'px'}
      else if(fx==='count'){const to=+e.dataset.to;e.textContent=Math.round(clamp((t-a)/1.0)*to).toLocaleString('pt-BR')+(e.dataset.suf??'g');e.style.opacity=t>=a?1:0;continue}
      else if(fx==='wave'){o=t>=a?1:0;[...e.children].forEach((c,i)=>c.style.transform=`translateY(${Math.sin(t*6+i*.8)*22}px)`)}
      else if(fx==='wobble'){o=q;tr=`rotate(${Math.sin((t-a)*10)*6}deg)`}
      e.style.opacity=o;e.style.transform=tr;
    }
    for(const e of anims){const n=+e.dataset.n,ms=+e.dataset.ms;const i=Math.floor(t*1000/ms)%n;
      const src=`${e.dataset.anim}_${String(i).padStart(2,'0')}.png`;if(!e.src.endsWith(src.replace(/^(\.\.\/)+/,'')))e.src=src}
  };
  window.addEventListener('load',()=>seek(0));
})();
