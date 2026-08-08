const fs=require('fs');
const vm=require('vm');
const {crearEntorno}=require('./mini_dom.js');
const ruta=process.argv[2];
const html=fs.readFileSync(ruta,'utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const {win,doc,nodos,almacen}=crearEntorno(html);
const ctx=vm.createContext(win);
let err=null;
try{
 for(const s of scripts) vm.runInContext(s,ctx,{timeout:10000});
}catch(e){err=e}
setTimeout(()=>{
 const R=[];const ok=(n,c)=>R.push([n,!!c]);
 ok("el script se ejecuta entero sin excepción", !err);
 if(err)console.log("   → "+err.message);
 ok("indicador de página con contenido", nodos.pag && /\d/.test(nodos.pag.textContent));
 const a=nodos.pag?nodos.pag.textContent:"";
 nodos.bSig.click();
 ok("avanza de página", nodos.pag.textContent!==a);
 const b=nodos.pag.textContent;
 nodos.bAnt.click();
 ok("retrocede de página", nodos.pag.textContent!==b);
 nodos.bMarca.click();
 ok("guarda marcador", /\[\{/.test(almacen["fds-es:marcas"]||almacen["fds-en:marcas"]||""));
 nodos.bComp.click();
 ok("genera el QR", /<svg/.test(nodos.qrCaja.innerHTML));
 ok("muestra la URL", /https/.test(nodos.urlTxt.textContent));
 nodos.bToc.click();
 ok("abre el índice", nodos.toc.classList.contains("on"));
 nodos.bAa.click();
 ok("abre los ajustes", nodos.panel.classList.contains("on"));
 nodos.bMas.click();
 ok("aumenta el tamaño de letra", parseFloat(almacen[Object.keys(almacen).find(k=>/:tam$/.test(k))]||0)>1.07);
 ok("guarda el registro de lectura", Object.keys(almacen).some(k=>/:(pct|sec|cap)$/.test(k)));
 console.log("\n"+ruta.split('/').pop());
 let f=0;R.forEach(([n,o])=>{if(!o)f++;console.log((o?"  OK    ":"  FALLA ")+n)});
 process.exit(f?1:0);
},60);
