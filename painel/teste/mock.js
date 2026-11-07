// Simula window.claude (db + downloads) para testar o painel fora do claude.ai
window.__saves=[];
(function(){
  const docs={};let subs=[];
  const emit=()=>subs.forEach(cb=>cb({metadata:{fromCache:false},docs:Object.keys(docs).sort().map(id=>({id,exists:true,data:()=>docs[id]}))}));
  window.__seed=(arr)=>{arr.forEach(([id,d])=>docs[id]=d);emit()};
  const db={collection:()=>({onSnapshot:(cb)=>{subs.push(cb);setTimeout(emit,50);return()=>{}},doc:(id)=>({update:async(p)=>{docs[id]={...docs[id],...p};setTimeout(emit,10)}})})};
  const downloads={save:async({filename,data})=>{window.__saves.push([filename,data.size||data.length]);return{status:"saved"}}};
  window.claude={use:async(n)=>n==="db"?db:n==="downloads"?downloads:null};
})();
