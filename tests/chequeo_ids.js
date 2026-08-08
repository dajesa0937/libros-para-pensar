const fs=require('fs');
let fallos=0;
for(const ruta of process.argv.slice(2)){
 const html=fs.readFileSync(ruta,'utf8');
 const nombre=ruta.split('/').pop();
 const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join("\n");
 const idsHtml=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
 const pedidos=[...scripts.matchAll(/getElementById\(\s*"([^"]+)"\s*\)/g)].map(m=>m[1]);
 const sel=[...scripts.matchAll(/querySelector\(\s*"#([^"'\s\)]+)"/g)].map(m=>m[1]);
 const faltan=[...new Set([...pedidos,...sel])].filter(id=>!idsHtml.has(id));
 // selectores por atributo usados con querySelectorAll
 const attrs=[...new Set([...scripts.matchAll(/querySelectorAll?\(\s*"\[([a-z-]+)[=\]]/g)].map(m=>m[1]))];
 const attrsFaltan=attrs.filter(a=>!new RegExp("\\b"+a+"=").test(html));
 console.log(nombre.padEnd(25),
   faltan.length===0&&attrsFaltan.length===0 ? "OK  todos los elementos existen"
   : "FALLA faltan: "+[...faltan,...attrsFaltan].join(", "));
 if(faltan.length||attrsFaltan.length)fallos++;
}
process.exit(fallos?1:0);
