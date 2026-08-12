const fs=require('fs'),path=require('path');
const dir = require("path").join(__dirname,"..","web");
const archivos=fs.readdirSync(dir);
let fallos=0;
const chk=(n,ok,extra)=>{console.log((ok?"  OK    ":"  FALLA ")+n+(extra&&!ok?" → "+extra:""));if(!ok)fallos++};

console.log("\nArchivos en la carpeta:", archivos.length);
const necesarios=["index.html","index-en.html","fabricantes-de-sed.html","thirst-makers.html","cartel.html","poster.html",
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
 chk(f+": tiene og:image", /og:image/.test(h) || ["404.html","cartel.html","poster.html"].includes(f));
}
const sm=fs.readFileSync(path.join(dir,"sitemap.xml"),'utf8');
const urls=[...sm.matchAll(/<loc>[^<]*\/([^<\/]+)<\/loc>/g)].map(m=>m[1]);
chk("sitemap sólo apunta a páginas existentes", urls.every(u=>archivos.includes(u)),
    urls.filter(u=>!archivos.includes(u)).join(", "));


// Las URLs absolutas que apuntan al propio sitio deben corresponder a un archivo real.
// Existe porque el kit de difusión pasó a usar rutas absolutas: un BASEURL mal
// puesto rompería el cartel y las descargas sin que nada más fallara.
const BASE = (fs.readFileSync(path.join(dir,"robots.txt"),'utf8')
  .match(/Sitemap: (https?:\/\/[^\/]+)/)||[])[1];
if(BASE){
  console.log("\n  base declarada en robots.txt: "+BASE);
  for(const f of archivos.filter(f=>f.endsWith(".html"))){
    const h=fs.readFileSync(path.join(dir,f),'utf8');
    const abs=[...new Set([...h.matchAll(new RegExp(BASE.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+"\\/([A-Za-z0-9._-]+\\.(?:html|png|svg|xml|txt))","g"))].map(m=>m[1]))];
    const rotos=abs.filter(a=>!archivos.includes(a));
    if(abs.length) chk(f+": URLs absolutas apuntan a archivos reales", rotos.length===0, rotos.join(", "));
  }
} else chk("robots.txt declara el sitemap con la URL base", false);

const total=archivos.reduce((s,f)=>s+fs.statSync(path.join(dir,f)).size,0);
console.log("\n  Peso total del sitio:",(total/1024/1024).toFixed(2),"MB");
console.log(fallos===0?"\n=== LISTO PARA SUBIR ===\n":`\n=== ${fallos} PROBLEMAS ===\n`);
process.exit(fallos?1:0);
