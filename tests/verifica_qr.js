const mine=require('./qr.js');
const QRCode=require('qrcode');
const casos=[
 "https://libros.example.com/fabricantes-de-sed.html",
 "https://dawin.netlify.app/",
 "Fabricantes de sed — Dawin Salazar",
 "https://libros-para-pensar.netlify.app/thirst-makers.html#s12",
 "a",
 "https://ejemplo.co/"+"x".repeat(120),
 "Ñandú, ácido, corazón — prueba UTF-8 ✓"
];
let fallos=0;
(async()=>{
 for(const t of casos){
  const ref=QRCode.create(t,{errorCorrectionLevel:'M'});
  const n=ref.modules.size, refData=ref.modules.data;
  const m=mine.build(t);
  let ok = (m.length===n);
  if(ok){
   for(let r=0;r<n&&ok;r++)for(let c=0;c<n;c++){
    const a=m[r][c]?1:0, b=refData[r*n+c]?1:0;
    if(a!==b){ok=false;console.log(`  discrepancia en (${r},${c})`);break}}
  } else console.log(`  tamaño: mío ${m.length} vs ref ${n}`);
  console.log((ok?"OK  ":"FALLA")+"  ["+n+"x"+n+"] "+t.slice(0,52));
  if(!ok)fallos++;
 }
 console.log(fallos===0?"\n=== TODOS LOS QR COINCIDEN CON LA REFERENCIA ===":`\n=== ${fallos} FALLOS ===`);
 process.exit(fallos?1:0);
})();
