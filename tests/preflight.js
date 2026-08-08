const fs=require('fs'),path=require('path');
const dir = require("path").join(__dirname,"..","web");
const archivos=fs.readdirSync(dir);
let fallos=0;
const chk=(n,ok,extra)=>{console.log((ok?"  OK    ":"  FALLA ")+n+(extra&&!ok?" → "+extra:""));if(!ok)fallos++};

console.log("\nArchivos en la carpeta:", archivos.length);
const necesarios=["index.html","index-en.html","fabricantes-de-sed.html","thirst-makers.html",
 "og-es.png","og-en.png","favicon.svg","robots.txt","sitemap.xml","404.html","_headers","_redirects"];
chk("están los 12 archivos necesarios", necesarios.every(f=>archivos.includes(f)),
    necesarios.filter(f=>!archivos.includes(f)).join(", "));
chk("no quedan notas internas publicables", !archivos.some(f=>/\.md$/i.test(f)),
    archivos.filter(f=>/\.md$/i.test(f)).join(", "));

for(const f of archivos.filter(f=>f.endsWith(".html"))){
 const h=fs.readFileSync(path.join(dir,f),'utf8');
 const enlaces=[...h.matchAll(/(?:href|src)="([^"#:]+\.(?:html|png|svg|xml|txt))"/g)].map(m=>m[1]);
 const rotos=[...new Set(enlaces)].filter(e=>!archivos.includes(e.replace(/^\//,'')));
 chk(f+": enlaces internos válidos", rotos.length===0, rotos.join(", "));
 chk(f+": sin marcadores sin sustituir", !/__[A-Z_]+__/.test(h), (h.match(/__[A-Z_]+__/g)||[])[0]);
 chk(f+": tiene og:image", /og:image/.test(h) || f==="404.html");
}
const sm=fs.readFileSync(path.join(dir,"sitemap.xml"),'utf8');
const urls=[...sm.matchAll(/<loc>[^<]*\/([^<\/]+)<\/loc>/g)].map(m=>m[1]);
chk("sitemap sólo apunta a páginas existentes", urls.every(u=>archivos.includes(u)),
    urls.filter(u=>!archivos.includes(u)).join(", "));

const total=archivos.reduce((s,f)=>s+fs.statSync(path.join(dir,f)).size,0);
console.log("\n  Peso total del sitio:",(total/1024/1024).toFixed(2),"MB");
console.log(fallos===0?"\n=== LISTO PARA SUBIR ===\n":`\n=== ${fallos} PROBLEMAS ===\n`);
process.exit(fallos?1:0);
