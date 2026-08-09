// Comprueba que las páginas en inglés no contengan texto en español.
// Existe porque el panel de compartir de la portada inglesa se publicó en español.
const fs=require('fs'), path=require('path');
const dir=path.join(__dirname,'..','web');

const ES=[ "Compartir","Copiar","Cerrar","Cambiar","Tema","enlace","código","teléfono",
  "biblioteca","Enséñele","envíe","sitio","claro","oscuro","Saltar","contenido",
  "Página","leído","Índice","Ajustes","Continuar","aquí","letra","voz","página",
  "Copiado","anterior","siguiente","lectura","Marcadores","Borrar" ];

const PROPIOS=/Bancolombia|Colombia|Dawin Salazar|Tomás|Alcázar|Elena|Irene|Sabino|Nadia|Vidal|Guecho|Murano|Ur\b|español|Español/;

let fallos=0;
for(const f of ["index-en.html","thirst-makers.html"]){
  const h=fs.readFileSync(path.join(dir,f),'utf8');
  // interfaz: atributos accesibles, botones, títulos y etiquetas
  const zonas=[
    ...[...h.matchAll(/aria-label="([^"]+)"/g)].map(m=>["aria-label",m[1]]),
    ...[...h.matchAll(/title="([^"]+)"/g)].map(m=>["title",m[1]]),
    ...[...h.matchAll(/<button[^>]*>([^<]{2,})</g)].map(m=>["button",m[1]]),
    ...[...h.matchAll(/<h[34][^>]*>([^<]{2,})</g)].map(m=>["heading",m[1]]),
    ...[...h.matchAll(/class="etxt">([^<]+)</g)].map(m=>["etxt",m[1]]),
    ...[...h.matchAll(/class="notaComp">([^<]+)</g)].map(m=>["nota",m[1]]),
    ...[...h.matchAll(/textContent="([^"]+)"/g)].map(m=>["js",m[1]]),
  ];
  const malos=[];
  for(const [donde,txt] of zonas){
    if(PROPIOS.test(txt))continue;
    for(const w of ES){
      if(new RegExp("\\b"+w+"\\b","i").test(txt)){malos.push(`${donde}: "${txt.trim()}"`);break}
    }
  }
  const unicos=[...new Set(malos)];
  console.log((unicos.length?"  FALLA ":"  OK    ")+f+
    (unicos.length?` — ${unicos.length} textos en español`:" — interfaz íntegramente en inglés"));
  unicos.slice(0,8).forEach(m=>console.log("      "+m));
  if(unicos.length)fallos++;
}
process.exit(fallos?1:0);
