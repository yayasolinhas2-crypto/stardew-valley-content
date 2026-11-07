// Enfeites de fundo em pixel, sempre na mesma posição (semente fixa).
// Nunca dentro da faixa do quadro e da frase-ponte (y 250–1580).
(function(){
  let seed=7;const r=()=>(seed=(seed*9301+49297)%233280)/233280;
  const yOk=y=>y<250||(y>1580&&y<1640);
  document.querySelectorAll('.slide').forEach(s=>{
    const t=s.className;
    const layer=document.createElement('div');s.prepend(layer);
    if(t.includes('tema-noite')||t.includes('tema-por-do-sol')||t.includes('tema-inverno')){layer.className='stars';
      for(let i=0;i<60;i++){const y=Math.floor(r()*205)*8;if(!yOk(y))continue;const e=document.createElement('i');if(r()<.25)e.className='b';e.style.left=Math.floor(r()*135)*8+'px';e.style.top=y+'px';layer.appendChild(e)}}
    if(t.includes('tema-dia')){layer.className='clouds';
      [[60,120,140],[520,60,180],[820,170,120],[300,200,100]].forEach(([x,y,w])=>{const b=document.createElement('b');b.style.left=x+'px';b.style.top=y+'px';b.style.width=w+'px';layer.appendChild(b)})}
    if(t.includes('tema-mar')){layer.className='waves';
      for(let i=0;i<40;i++){const y=1600+Math.floor(r()*38)*8;const e=document.createElement('i');e.style.left=Math.floor(r()*130)*8+'px';e.style.top=y+'px';layer.appendChild(e)}}
    const card=s.querySelector('.card');if(card){const g=document.createElement('div');g.className='sig';g.textContent='@segredosdovalley';card.appendChild(g)}
    if(!t.includes('tema-mar')){['hills','hills2'].forEach(c=>{const h=document.createElement('div');h.className=c;s.appendChild(h)})}
  });
})();
