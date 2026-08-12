#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sitio 'Libros para pensar': portada + lector paginado accesible."""

import html, os, re
from cubierta import CUBIERTA, CUBIERTA_EN

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "src", "manuscritos")
OUT = os.path.join(RAIZ, "web")
os.makedirs(OUT, exist_ok=True)

PARTS = ["MANUSCRITO.md", "MANUSCRITO_P2.md", "MANUSCRITO_P3.md",
         "MANUSCRITO_P4.md", "MANUSCRITO_P5.md"]
SITIO = "Libros para pensar"
# Dirección definitiva del sitio. Cámbiela aquí y regenere, o edite los HTML.
BASEURL = os.environ.get("URL_SITIO", "https://libros-para-pensar.netlify.app").rstrip("/")
CUENTA = "333 279 352 89"
BANCO = "Bancolombia · Cuenta de ahorros"


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def parse(partes=None):
    raw = ""
    for p in (partes or PARTS):
        raw += open(os.path.join(BASE, p), encoding="utf-8").read() + "\n"
    lines, secciones, buf, cur = raw.split("\n"), [], [], None
    epi = titulo = None

    def cerrar():
        nonlocal cur, buf
        if cur:
            cur["html"] = "\n".join(buf)
            secciones.append(cur)
        buf = []

    i = 0
    while i < len(lines):
        t = lines[i].strip(); i += 1
        if t in ("", ">"):
            continue
        if t.startswith("# "):
            titulo = t[2:].strip(); continue
        if t.startswith("## "):
            cerrar()
            cab, sub = t[3:].strip(), ""
            j = i
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and lines[j].strip().startswith("### "):
                sub = lines[j].strip()[4:].strip(); i = j + 1
            if cab.startswith("INTERLUDIO"):
                kind = "interludio"
            elif cab.startswith("CAPÍTULO"):
                kind = "cap"
            elif cab in ("PRÓLOGO", "EPÍLOGO"):
                kind = "marco"
            else:
                kind = "final"
            cur = {"id": "s%d" % len(secciones), "kind": kind, "num": cab, "titulo": sub}
            continue
        if cur is None:
            if t.startswith("> "):
                epi = inline(t[2:])
            continue
        if t == "---":
            buf.append('<hr class="sep" aria-hidden="true">')
        elif t.startswith("> "):
            buf.append("<blockquote>%s</blockquote>" % inline(t[2:]))
        else:
            cls = ' class="dial"' if t.startswith("—") else ""
            buf.append("<p%s>%s</p>" % (cls, inline(t)))
    cerrar()
    return titulo, epi, secciones


# ----------------------------------------------------------------- CSS común
BASECSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{
 --papel:#faf8f4;--tinta:#201d19;--suave:#6b6459;--linea:#e3ddd2;
 --acento:#8a5424;--caja:#f2ece2;--marca:#201d19;--foco:#0a58ca;
 --fs:1.075rem;--lh:1.75;--ls:0em;--marg:1.4rem;
 --fam:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
}
html[data-tema="sepia"]{--papel:#f4e9d6;--tinta:#3b2f21;--suave:#7a6752;--linea:#ded0b6;--caja:#ecdfc7;--acento:#8a5424;--marca:#3b2f21}
html[data-tema="noche"]{--papel:#14120f;--tinta:#dcd5c9;--suave:#8f877b;--linea:#2d2922;--acento:#cf9a56;--caja:#1d1a15;--marca:#dcd5c9;--foco:#8ab4f8}
html[data-tema="contraste"]{--papel:#000;--tinta:#fff;--suave:#ffe14d;--linea:#fff;--acento:#ffe14d;--caja:#000;--marca:#fff;--foco:#ffe14d}
html[data-tema="contraste"] body{font-weight:500}
html{-webkit-text-size-adjust:100%}
body{background:var(--papel);color:var(--tinta);font-family:var(--fam);
 font-size:var(--fs);line-height:var(--lh);letter-spacing:var(--ls);
 -webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:3px solid var(--foco);outline-offset:2px;border-radius:3px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
 clip:rect(0 0 0 0);white-space:nowrap;border:0}
.saltar{position:absolute;left:-9999px;top:0;background:var(--tinta);color:var(--papel);
 padding:.8rem 1.2rem;z-index:200;font-family:system-ui,sans-serif}
.saltar:focus{left:0}
button{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
 background:none;border:1px solid var(--linea);color:var(--tinta);cursor:pointer;
 border-radius:.5rem;min-height:44px;min-width:44px;font-size:.9rem;
 display:inline-flex;align-items:center;justify-content:center;gap:.4rem;padding:0 .7rem}
button:hover{background:var(--caja)}
button[aria-pressed="true"]{background:var(--tinta);color:var(--papel);border-color:var(--tinta)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

# ----------------------------------------------------------------- lector
READER = r"""<!DOCTYPE html>
<html lang="__LANG__" data-tema="dia">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=5">
<title>__TIT__ — __SITIO__</title>
<meta name="description" content="Novela sobre la persuasión, la verdad y el precio de las palabras. Lectura libre.">
<meta name="theme-color" content="#faf8f4">
<meta property="og:title" content="__TIT__">
<meta property="og:description" content="__OGDESC__">
<meta property="og:image" content="__BASEURL__/__OGIMG__">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="__BASEURL__/__ESTE__">
<meta property="og:locale" content="__LOCALE__">
<meta property="og:site_name" content="__SITIO__">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="__BASEURL__/__ESTE__">
<link rel="alternate" hreflang="es" href="__BASEURL__/fabricantes-de-sed.html">
<link rel="alternate" hreflang="en" href="__BASEURL__/thirst-makers.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
__BASE__
html,body{height:100%;overflow:hidden}
.app{display:flex;flex-direction:column;height:100svh}

header.top{display:flex;align-items:center;gap:.3rem;padding:.4rem .6rem;
 padding-top:calc(.4rem + env(safe-area-inset-top));border-bottom:1px solid var(--linea);
 background:var(--papel);flex-shrink:0}
.top .vuelta{font-family:system-ui,sans-serif;font-size:.8rem;text-decoration:none;
 color:var(--suave);padding:.5rem;min-height:44px;display:flex;align-items:center}
.cap-actual{flex:1;text-align:center;font-size:.78rem;color:var(--suave);
 font-family:system-ui,sans-serif;overflow:hidden;text-overflow:ellipsis;
 white-space:nowrap;padding:0 .3rem}

#zona{flex:1;position:relative;overflow:hidden;min-height:0}
#libro{height:100%;padding:1.6rem var(--marg) 1rem;overflow:hidden}
#flujo{height:100%;column-gap:2.4rem;column-fill:auto;
 transition:transform .28s cubic-bezier(.22,.61,.36,1)}
.continuo #zona{overflow-y:auto;-webkit-overflow-scrolling:touch}
.continuo #libro{height:auto;padding-bottom:5rem}
.continuo #flujo{height:auto!important;columns:auto!important;transform:none!important}

.toque{position:absolute;top:0;bottom:0;width:24%;z-index:5;border:0;
 border-radius:0;min-width:0;padding:0;cursor:pointer;
 background:none;display:flex;align-items:center;justify-content:center;
 font-family:Georgia,serif;font-size:2rem;line-height:1;color:var(--suave);
 -webkit-tap-highlight-color:transparent}
.toque.izq{left:0}.toque.der{right:0}
.toque:hover,.toque:active,.toque:focus{background:none}
.toque:focus-visible{outline:2px solid var(--foco);outline-offset:-8px;border-radius:.6rem}
.toque:before{opacity:0;transition:opacity .16s}
.toque.izq:before{content:"‹"}
.toque.der:before{content:"›"}
@media(hover:hover) and (pointer:fine){
 .toque:hover:before{opacity:.55}
}
.toque:active:before{opacity:.8}
.continuo .toque{display:none}

section{break-before:column}
section:first-child{break-before:auto}
.rotulo{font-family:system-ui,sans-serif;font-size:.7rem;letter-spacing:.2em;
 text-transform:uppercase;color:var(--suave);text-align:center}
.rotulo.inter{color:var(--acento)}
h2{text-align:center;font-weight:400;font-size:1.35em;font-style:italic;
 margin:.5rem 0 1.8rem;line-height:1.3}
p{text-align:justify;hyphens:auto;text-indent:1.2em;orphans:2;widows:2}
p:first-of-type,p.dial,blockquote+p,.sep+p{text-indent:0}
p.dial{text-indent:0}
blockquote{margin:1.1rem 0;padding-left:1rem;border-left:2px solid var(--linea);
 font-style:italic;color:var(--suave);text-align:left}
blockquote strong{font-style:normal;color:var(--tinta)}
.sep{border:0;text-align:center;margin:1.4rem 0;height:1.4rem}
.sep:after{content:"· · ·";color:var(--suave);letter-spacing:.5em;font-size:.85rem}
.leyendo{background:var(--caja);box-shadow:0 0 0 .2em var(--caja)}

footer.bot{display:flex;align-items:center;gap:.5rem;padding:.45rem .6rem;
 padding-bottom:calc(.45rem + env(safe-area-inset-bottom));
 border-top:1px solid var(--linea);background:var(--papel);flex-shrink:0}
.pag{flex:1;text-align:center;font-family:system-ui,sans-serif;font-size:.8rem;
 color:var(--suave);font-variant-numeric:tabular-nums}
.barrita{position:absolute;left:0;bottom:0;height:3px;background:var(--acento);
 width:0;z-index:8}

.panel{position:fixed;inset:auto 0 0 0;z-index:100;background:var(--papel);
 border-top:1px solid var(--linea);max-height:82svh;overflow-y:auto;
 padding:1.1rem 1.1rem calc(1.6rem + env(safe-area-inset-bottom));display:none;
 box-shadow:0 -8px 30px rgba(0,0,0,.18)}
.panel.on{display:block}
.panel h3{font-family:system-ui,sans-serif;font-size:.72rem;letter-spacing:.16em;
 text-transform:uppercase;color:var(--suave);font-weight:500;margin:1.2rem 0 .5rem}
.panel h3:first-of-type{margin-top:.4rem}
.fila{display:flex;gap:.45rem;flex-wrap:wrap}
.fila button{flex:1;min-width:4.2rem}
.notaComp{font-size:.85rem;color:var(--suave);text-indent:0;text-align:left;margin:.3rem 0 .9rem;font-family:system-ui,sans-serif}
.qrCaja{display:flex;justify-content:center;padding:.9rem;background:#fff;
 border:1px solid var(--linea);border-radius:.7rem}
.qrCaja svg{display:block;max-width:100%;height:auto}
.urlTxt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.78rem;
 word-break:break-all;color:var(--suave);text-align:center;text-indent:0;margin:.7rem 0 .9rem}
.reanudar{position:fixed;inset:0;z-index:130;background:rgba(0,0,0,.55);
 display:none;align-items:center;justify-content:center;padding:1.3rem}
.reanudar.on{display:flex}
.tarjetaR{background:var(--papel);border-radius:.9rem;padding:1.5rem;max-width:23rem;
 width:100%;border:1px solid var(--linea)}
.tarjetaR .rot{font-family:system-ui,sans-serif;font-size:.68rem;letter-spacing:.18em;
 text-transform:uppercase;color:var(--suave)}
.rCap{font-size:1.2rem;font-style:italic;margin:.5rem 0 .3rem;line-height:1.3}
.rMeta{font-family:system-ui,sans-serif;font-size:.82rem;color:var(--suave)}
button.pri{background:var(--marca);color:var(--papel);border-color:var(--marca)}
button.pri:hover{background:var(--marca);opacity:.9}
#zonaMarcas{max-width:34rem;margin:0 auto;padding:0 1.1rem}
#zonaMarcas h4{font-family:system-ui,sans-serif;font-size:.68rem;letter-spacing:.16em;
 text-transform:uppercase;color:var(--suave);font-weight:500;margin:.2rem 0 .5rem}
.marca{display:flex;align-items:center;gap:.5rem;padding:.6rem .2rem;
 border-bottom:1px solid var(--linea)}
.marca a{flex:1;text-decoration:none;font-style:italic}
.marca .pc{font-family:system-ui,sans-serif;font-size:.74rem;color:var(--suave)}
.marca button{min-height:36px;min-width:36px;border:0;color:var(--suave)}
.etq{display:block;font-family:system-ui,sans-serif;font-size:.8rem;color:var(--suave);margin:.9rem 0 .35rem}
select{width:100%;min-height:44px;font-family:system-ui,sans-serif;font-size:.9rem;
 background:var(--papel);color:var(--tinta);border:1px solid var(--linea);
 border-radius:.5rem;padding:.5rem}
.velo{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:90;display:none}
.velo.on{display:block}
.cabpanel{display:flex;align-items:center;justify-content:space-between;
 font-family:system-ui,sans-serif;font-size:1rem}

#toc{position:fixed;inset:0;z-index:110;background:var(--papel);overflow-y:auto;
 display:none;padding:calc(.6rem + env(safe-area-inset-top)) 0 3rem}
#toc.on{display:block}
#toc .cab{display:flex;align-items:center;justify-content:space-between;
 padding:0 1rem 1rem;font-family:system-ui,sans-serif}
#toc ol{list-style:none;max-width:34rem;margin:0 auto;padding:0 1.1rem}
#toc a{display:block;padding:.85rem .2rem;text-decoration:none;
 border-bottom:1px solid var(--linea);min-height:44px}
#toc .n{font-family:system-ui,sans-serif;font-size:.64rem;letter-spacing:.16em;
 text-transform:uppercase;color:var(--suave);display:block}
#toc .t{font-style:italic}
#toc a[aria-current="true"]{background:var(--caja);border-left:3px solid var(--acento);
 padding-left:.7rem;margin-left:-.7rem}
#toc a[aria-current="true"] .t:after{content:" — __TXT_VASAQUI__";color:var(--acento);
 font-style:normal;font-family:system-ui,sans-serif;font-size:.68rem;letter-spacing:.12em;
 text-transform:uppercase}
#toc a[aria-current="true"] .n{color:var(--acento)}

.fin{padding:2rem 0 1rem;text-align:center}
.caja-cuenta{border:1px solid var(--linea);border-radius:.6rem;padding:1rem;
 margin:1.2rem 0;background:var(--caja);text-align:center}
.caja-cuenta .banco{font-family:system-ui,sans-serif;font-size:.7rem;
 letter-spacing:.13em;text-transform:uppercase;color:var(--suave)}
.caja-cuenta .extra{font-family:system-ui,sans-serif;font-size:.72rem;color:var(--suave);margin-top:.7rem;line-height:1.5}
.caja-cuenta .num{font-size:1.4rem;letter-spacing:.05em;margin:.4rem 0 .8rem;
 font-variant-numeric:tabular-nums}
@media(min-width:820px){
 :root{--marg:2.4rem}
 #flujo{columns:2}
 .continuo #libro{max-width:40rem;margin:0 auto}
}
</style>
</head>
<body>
<a class="saltar" href="#libro">__TXT_SALTAR__</a>

<div class="app" id="app">
 <header class="top">
  <a class="vuelta" href="__HOME__">‹ __TXT_BIB__</a>
  <span class="cap-actual" id="capActual">__TIT__</span>
  <button id="bMarca" aria-label="__TXT_MARCAR__" title="__TXT_MARCAR__">⚑</button>
  <button id="bComp" aria-label="__TXT_COMPARTIR__" title="__TXT_COMPARTIR__">↗</button>
  <button id="bVoz" aria-label="__TXT_VOZ__" title="__TXT_VOZ__">▶</button>
  <button id="bToc" aria-label="__TXT_IDX__" title="__TXT_IDX__">☰</button>
  <button id="bAa" aria-label="__TXT_AJU__" title="__TXT_AJU__">Aa</button>
 </header>

 <div id="zona">
  <div id="libro" role="document">
   <div id="flujo">__CUERPO__
    <section class="fin" id="sFin">
     <div class="rotulo">__TXT_FIN__</div>
     <h2>__TXT_ULT__</h2>
     __BLOQUE_APORTE__
     <p style="text-indent:0"><a href="__HOME__">__TXT_VOLVER__</a></p>
    </section>
   </div>
  </div>
  <button class="toque izq" id="tIzq" aria-label="__TXT_ANT__"></button>
  <button class="toque der" id="tDer" aria-label="__TXT_SIG__"></button>
  <div class="barrita" id="barrita" aria-hidden="true"></div>
 </div>

 <footer class="bot">
  <button id="bAnt" aria-label="__TXT_ANT__">‹</button>
  <div class="pag" id="pag" role="status" aria-live="polite">…</div>
  <button id="bSig" aria-label="__TXT_SIG__">›</button>
 </footer>
</div>

<div class="velo" id="velo"></div>

<div class="panel" id="panel" role="dialog" aria-modal="true" aria-label="__TXT_AJU__">
 <div class="cabpanel"><strong>__TXT_AJU__</strong>
  <button id="bCerrarPanel" aria-label="✕">✕</button></div>

 <h3 id="hTam">__TXT_TAM__</h3>
 <div class="fila" aria-labelledby="hTam">
  <button id="bMenos" aria-label="__TXT_TAM__ −">A −</button>
  <button disabled aria-live="polite" id="valTam" style="flex:1.4">100%</button>
  <button id="bMas" aria-label="__TXT_TAM__ +">A +</button>
 </div>

 <h3 id="hTip">__TXT_TIP__</h3>
 <div class="fila" role="group" aria-labelledby="hTip">
  <button data-fam="serif">Serif</button>
  <button data-fam="sans">Sans</button>
  <button data-fam="legible">__TXT_LEG__</button>
 </div>

 <h3 id="hTem">__TXT_COL__</h3>
 <div class="fila" role="group" aria-labelledby="hTem">
  <button data-tema="dia">__TXT_CLA__</button>
  <button data-tema="sepia">__TXT_SEP__</button>
  <button data-tema="noche">__TXT_OSC__</button>
  <button data-tema="contraste">__TXT_CON__</button>
 </div>

 <h3 id="hEsp">__TXT_ESP__</h3>
 <div class="fila" role="group" aria-labelledby="hEsp">
  <button data-lh="1.5">__TXT_CMP__</button>
  <button data-lh="1.75">__TXT_NRM__</button>
  <button data-lh="2.1">__TXT_AMP__</button>
 </div>
 <div class="fila" role="group" aria-label="Separación entre letras" style="margin-top:.45rem">
  <button data-ls="0em">__TXT_LN__</button>
  <button data-ls="0.04em">__TXT_LS__</button>
 </div>

 <h3 id="hModo">__TXT_MOD__</h3>
 <div class="fila" role="group" aria-labelledby="hModo">
  <button data-modo="paginas">__TXT_PAG__</button>
  <button data-modo="continuo">__TXT_SCR__</button>
 </div>

 <h3 id="hVoz">__TXT_VOZ__</h3>
 <div class="fila" role="group" aria-labelledby="hVoz">
  <button data-vel="0.7">__TXT_MLEN__</button>
  <button data-vel="0.85">__TXT_LEN__</button>
  <button data-vel="1">__TXT_NRM__</button>
  <button data-vel="1.15">__TXT_RAP__</button>
 </div>
 <label class="etq" for="selVoz">__TXT_ELIGEVOZ__</label>
 <select id="selVoz"></select>
 <p style="font-size:.82rem;color:var(--suave);margin-top:.6rem;text-indent:0;text-align:left">
  __TXT_NOTAVOZ__</p>
</div>

<nav id="toc" aria-label="__TXT_IDX__">
 <div class="cab"><strong>__TXT_IDX__</strong>
  <button id="bCerrarToc" aria-label="✕">✕</button></div>
 <div id="zonaMarcas"></div>
 <ol>__TOC__</ol>
</nav>

<div class="panel" id="compartir" role="dialog" aria-modal="true" aria-label="__TXT_COMPARTIR__">
 <div class="cabpanel"><strong>__TXT_COMPARTIR__</strong>
  <button id="bCerrarComp" aria-label="✕">✕</button></div>
 <p class="notaComp">__TXT_NOTACOMP__</p>
 <div id="qrCaja" class="qrCaja"></div>
 <p class="urlTxt" id="urlTxt"></p>
 <div class="fila">
  <button id="bEnviar">__TXT_ENVIAR__</button>
  <button id="bCopiarUrl">__TXT_COPIARURL__</button>
 </div>
 <div class="fila" style="margin-top:.45rem">
  <button id="bWa">WhatsApp</button>
  <button id="bDescargaQR">__TXT_BAJARQR__</button>
 </div>
</div>

<div class="reanudar" id="reanudar" role="dialog" aria-modal="true" aria-labelledby="rTit">
 <div class="tarjetaR">
  <div class="rot" id="rTit">__TXT_IBAPOR__</div>
  <div class="rCap" id="rCap"></div>
  <div class="rMeta" id="rMeta"></div>
  <div class="fila" style="margin-top:1.1rem">
   <button id="bSeguir" class="pri">__TXT_CONTINUAR__</button>
   <button id="bDesdeCero">__TXT_DESDECERO__</button>
  </div>
 </div>
</div>

<script>__QRJS__</script>
<script>
(function(){
var H=document.documentElement,K="__NS__:",app=document.getElementById("app"),
 flujo=document.getElementById("flujo"),libro=document.getElementById("libro"),
 zona=document.getElementById("zona"),pagOut=document.getElementById("pag"),
 barrita=document.getElementById("barrita"),capOut=document.getElementById("capActual"),
 secs=[].slice.call(flujo.querySelectorAll("section")),
 modo="paginas",p=0,total=1,ancho=0;

function get(k,d){var v=localStorage.getItem(K+k);return v===null?d:v}
function set(k,v){try{localStorage.setItem(K+k,v)}catch(e){}}

var FAM={serif:'"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif',
 sans:'-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
 legible:'Verdana,Tahoma,"DejaVu Sans",Geneva,sans-serif'};

function marcar(sel,attr,val){
 [].forEach.call(document.querySelectorAll(sel),function(b){
  b.setAttribute("aria-pressed",b.getAttribute(attr)===val?"true":"false")})}

function aplicar(){
 var tam=parseFloat(get("tam","1.075")),fam=get("fam","serif"),tema=get("tema","dia"),
  lh=get("lh","1.75"),ls=get("ls","0em");
 H.style.setProperty("--fs",tam+"rem");
 H.style.setProperty("--fam",FAM[fam]);
 H.style.setProperty("--lh",lh);
 H.style.setProperty("--ls",ls);
 H.dataset.tema=tema;
 document.getElementById("valTam").textContent=Math.round(tam/1.075*100)+"%";
 var tc={dia:"#faf8f4",sepia:"#f4e9d6",noche:"#14120f",contraste:"#000000"}[tema];
 document.querySelector('meta[name=theme-color]').content=tc;
 marcar("[data-fam]","data-fam",fam);marcar("[data-tema]","data-tema",tema);
 marcar("[data-lh]","data-lh",lh);marcar("[data-ls]","data-ls",ls);
 marcar("[data-vel]","data-vel",get("vel","0.85"));
 marcar("[data-modo]","data-modo",modo);
}

function medir(){
 if(modo==="continuo"){total=1;return}
 ancho=libro.clientWidth-parseFloat(getComputedStyle(libro).paddingLeft)
   -parseFloat(getComputedStyle(libro).paddingRight);
 var cols=innerWidth>=820?2:1, gap=parseFloat(getComputedStyle(flujo).columnGap)||0;
 var colw=(ancho-gap*(cols-1))/cols;
 flujo.style.columnWidth=colw+"px";
 flujo.style.height=libro.clientHeight-parseFloat(getComputedStyle(libro).paddingTop)
   -parseFloat(getComputedStyle(libro).paddingBottom)+"px";
 var paso=ancho+gap;
 total=Math.max(1,Math.round(flujo.scrollWidth/paso));
 flujo.dataset.paso=paso;
}

function ir(n,suave){
 if(modo==="continuo")return;
 p=Math.max(0,Math.min(total-1,n));
 var paso=parseFloat(flujo.dataset.paso||0);
 if(!suave)flujo.style.transition="none";
 flujo.style.transform="translateX("+(-p*paso)+"px)";
 if(!suave)requestAnimationFrame(function(){flujo.style.transition=""});
 pintar();set("pag",p);set("frac",p/Math.max(1,total-1));guardar();
}

function pctActual(){
 if(modo==="continuo"){var a=zona.scrollHeight-zona.clientHeight;
  return Math.round(a>0?zona.scrollTop/a*100:0)}
 return Math.round(total>1?p/(total-1)*100:0);
}
function pintar(){
 if(modo==="continuo"){
  var y=zona.scrollTop,alto=zona.scrollHeight-zona.clientHeight;
  barrita.style.width=(alto>0?y/alto*100:0)+"%";
  pagOut.textContent=pctActual()+"% __T_LEIDO__";
  set("scroll",y);
 }else{
  pagOut.textContent="__T_PAG__ "+(p+1)+" __T_DE__ "+total+"  ·  "+pctActual()+"%";
  barrita.style.width=(total>1?p/(total-1)*100:100)+"%";
 }
 var vista=null;
 for(var i=0;i<secs.length;i++){
  var r=secs[i].getBoundingClientRect();
  if(r.left<innerWidth*0.9&&r.right>0&&r.top<innerHeight)vista=secs[i];
 }
 if(vista){
  var n=vista.querySelector(".rotulo"),t=vista.querySelector("h2");
  capOut.textContent=(n?n.textContent:"")+(t&&t.textContent?" · "+t.textContent:"");
  [].forEach.call(document.querySelectorAll("#toc a"),function(a){
   a.setAttribute("aria-current",a.getAttribute("href")==="#"+vista.id?"true":"false")});
 }
}

function aSeccion(id){
 var el=document.getElementById(id);if(!el)return;
 if(modo==="continuo"){el.scrollIntoView({behavior:"smooth"});return}
 var paso=parseFloat(flujo.dataset.paso||1);
 var actual=-p*paso, x=el.getBoundingClientRect().left-flujo.getBoundingClientRect().left;
 ir(Math.round(x/paso),true);
}

function recalcular(mantener){
 var id=null;
 if(mantener&&modo==="paginas"){
  for(var i=0;i<secs.length;i++){var r=secs[i].getBoundingClientRect();
   if(r.left<innerWidth*0.9&&r.right>0){id=secs[i].id}}
 }
 medir();
 if(id)aSeccion(id);else ir(p,false);
}

function ponerModo(m){
 modo=m;set("modo",m);
 app.classList.toggle("continuo",m==="continuo");
 document.body.classList.toggle("continuo",m==="continuo");
 if(m==="continuo"){flujo.style.transform="";flujo.style.columnWidth="";
  flujo.style.height="";setTimeout(function(){
   var y=parseFloat(get("scroll","0"));if(y)zona.scrollTop=y;pintar()},30);
 }else{setTimeout(function(){medir();ir(p,false)},30)}
 aplicar();
}

document.getElementById("bMas").onclick=function(){
 var t=Math.min(2.2,parseFloat(get("tam","1.075"))+.09);set("tam",t);aplicar();recalcular(true)};
document.getElementById("bMenos").onclick=function(){
 var t=Math.max(.85,parseFloat(get("tam","1.075"))-.09);set("tam",t);aplicar();recalcular(true)};
[].forEach.call(document.querySelectorAll("[data-fam]"),function(b){
 b.onclick=function(){set("fam",b.dataset.fam);aplicar();recalcular(true)}});
[].forEach.call(document.querySelectorAll("[data-tema]"),function(b){
 b.onclick=function(){set("tema",b.dataset.tema);aplicar()}});
[].forEach.call(document.querySelectorAll("[data-lh]"),function(b){
 b.onclick=function(){set("lh",b.dataset.lh);aplicar();recalcular(true)}});
[].forEach.call(document.querySelectorAll("[data-ls]"),function(b){
 b.onclick=function(){set("ls",b.dataset.ls);aplicar();recalcular(true)}});
[].forEach.call(document.querySelectorAll("[data-modo]"),function(b){
 b.onclick=function(){ponerModo(b.dataset.modo)}});
[].forEach.call(document.querySelectorAll("[data-vel]"),function(b){
 b.onclick=function(){set("vel",b.dataset.vel);aplicar()}});

var panel=document.getElementById("panel"),velo=document.getElementById("velo"),
 toc=document.getElementById("toc");
function abrir(el){el.classList.add("on");velo.classList.add("on")}
function cerrar(){panel.classList.remove("on");toc.classList.remove("on");
 compartir.classList.remove("on");velo.classList.remove("on")}
document.getElementById("bAa").onclick=function(){abrir(panel)};
document.getElementById("bToc").onclick=function(){
 pintar();
 var act=toc.querySelector('a[aria-current="true"]');
 abrir(toc);
 if(act&&act.scrollIntoView)try{act.scrollIntoView({block:"center"})}catch(e){}
};
document.getElementById("bCerrarPanel").onclick=cerrar;
document.getElementById("bCerrarToc").onclick=cerrar;
velo.onclick=cerrar;
addEventListener("keydown",function(e){
 if(e.key==="Escape"){cerrar();return}
 if(panel.classList.contains("on")||toc.classList.contains("on"))return;
 if(e.key==="ArrowRight"||e.key==="PageDown"||e.key===" ")  {e.preventDefault();ir(p+1,true)}
 if(e.key==="ArrowLeft" ||e.key==="PageUp")                 {e.preventDefault();ir(p-1,true)}
 if(e.key==="Home")ir(0,true);
 if(e.key==="End")ir(total-1,true);
});

toc.addEventListener("click",function(e){
 var a=e.target.closest("a");if(!a)return;
 e.preventDefault();cerrar();aSeccion(a.getAttribute("href").slice(1))});

document.getElementById("bSig").onclick=function(){ir(p+1,true)};
document.getElementById("bAnt").onclick=function(){ir(p-1,true)};
document.getElementById("tDer").onclick=function(){ir(p+1,true)};
document.getElementById("tIzq").onclick=function(){ir(p-1,true)};

var x0=null,y0=null;
zona.addEventListener("touchstart",function(e){
 x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
zona.addEventListener("touchend",function(e){
 if(x0===null||modo==="continuo")return;
 var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;
 if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.4)ir(dx<0?p+1:p-1,true);
 x0=null},{passive:true});
zona.addEventListener("scroll",function(){if(modo==="continuo")pintar()},{passive:true});

var voz={on:false,i:0,nodos:[],lista:[]};
try{
var IDIOMA="__LANG__";

function puntuaVoz(v){
 var n=(v.name||"").toLowerCase(),p=0;
 if(/natural|neural/.test(n))p+=8;
 if(/premium|enhanced/.test(n))p+=6;
 if(/online/.test(n))p+=4;
 if(/google/.test(n))p+=4;
 if(v.localService===false)p+=2;
 if(/siri/.test(n))p+=3;
 if(/compact|espeak|pico|festival/.test(n))p-=8;
 if(IDIOMA==="en"&&/en-gb/i.test(v.lang))p+=1;
 return p;
}
function cargarVoces(){
 var todas=speechSynthesis.getVoices()||[];
 var vs=todas.filter(function(v){
  return (v.lang||"").toLowerCase().indexOf(IDIOMA)===0});
 if(!vs.length)vs=todas;
 vs.sort(function(a,b){return puntuaVoz(b)-puntuaVoz(a)});
 voz.lista=vs;
 var sel=document.getElementById("selVoz");
 if(!sel)return;
 sel.innerHTML="";
 vs.forEach(function(v,i){
  var o=document.createElement("option");
  o.value=v.name;o.textContent=v.name.replace(/Microsoft |Google /,"")+" · "+v.lang;
  sel.appendChild(o)});
 var guard=get("vozNom","");
 if(guard&&vs.some(function(v){return v.name===guard}))sel.value=guard;
 else if(vs[0])set("vozNom",vs[0].name);
}
if("speechSynthesis" in window){
 speechSynthesis.onvoiceschanged=cargarVoces;
 setTimeout(cargarVoces,120);
 var selv=document.getElementById("selVoz");
 if(selv)selv.onchange=function(){set("vozNom",this.value);
  if(voz.on){speechSynthesis.cancel();hablar()}};
}
function vozElegida(){
 var n=get("vozNom","");
 for(var i=0;i<voz.lista.length;i++)if(voz.lista[i].name===n)return voz.lista[i];
 return voz.lista[0]||null;
}
function textoVisible(){
 voz.nodos=[].slice.call(flujo.querySelectorAll("p,h2,blockquote")).filter(function(el){
  if(!el.textContent.trim())return false;
  var r=el.getBoundingClientRect();
  if(modo==="continuo")return r.bottom>0;
  return r.left>-20&&r.left<innerWidth});
 voz.i=0;
}
function limpiaTexto(t){
 return t.replace(/—/g," ").replace(/·/g," ").replace(/\s+/g," ").trim();
}
function hablar(){
 if(!voz.nodos[voz.i]){pararVoz();return}
 var el=voz.nodos[voz.i];
 [].forEach.call(flujo.querySelectorAll(".leyendo"),function(n){n.classList.remove("leyendo")});
 el.classList.add("leyendo");
 var u=new SpeechSynthesisUtterance(limpiaTexto(el.textContent));
 var v=vozElegida();
 if(v){u.voice=v;u.lang=v.lang}else{u.lang="__LANGVOZ__"}
 u.rate=parseFloat(get("vel","0.85"));
 u.pitch=1;u.volume=1;
 u.onend=function(){
  if(!voz.on)return;
  voz.i++;
  var pausa=/[.!?:;]$/.test(el.textContent.trim())?380:200;
  if(voz.i>=voz.nodos.length){
   ir(p+1,true);
   setTimeout(function(){if(voz.on){textoVisible();hablar()}},620);
  }else setTimeout(function(){if(voz.on)hablar()},pausa);
 };
 u.onerror=function(){if(voz.on){voz.i++;setTimeout(hablar,250)}};
 speechSynthesis.speak(u);
}
function pararVoz(){
 voz.on=false;speechSynthesis.cancel();
 var b=document.getElementById("bVoz");
 b.textContent="▶";b.setAttribute("aria-label","__TXT_VOZ__");
 [].forEach.call(flujo.querySelectorAll(".leyendo"),function(n){n.classList.remove("leyendo")});
}
document.getElementById("bVoz").onclick=function(){
 if(!("speechSynthesis" in window)){alert("__TXT_SINVOZ__");return}
 if(voz.on){pararVoz();return}
 if(!voz.lista.length)cargarVoces();
 voz.on=true;this.textContent="■";
 this.setAttribute("aria-label","__TXT_PARARVOZ__");
 textoVisible();hablar();
};

var cop=document.getElementById("bCopiar");
var etiquetaCopiar=cop.textContent;
cop.onclick=function(){
 var n=document.getElementById("numCuenta").textContent.trim();
 var ok=function(){cop.textContent="__TXT_COPIADO__";
  setTimeout(function(){cop.textContent=etiquetaCopiar},2200)};
 if(navigator.clipboard)navigator.clipboard.writeText(n).then(ok,ok);
 else{var t=document.createElement("textarea");t.value=n;document.body.appendChild(t);
  t.select();try{document.execCommand("copy")}catch(e){}t.remove();ok()}
};

function estadoActual(){
 var sec=null;
 for(var i=0;i<secs.length;i++){var r=secs[i].getBoundingClientRect();
  if(modo==="continuo"){if(r.top<innerHeight*0.5)sec=secs[i]}
  else if(r.left<innerWidth*0.9&&r.right>0)sec=secs[i]}
 var h2=sec?sec.querySelector("h2"):null,ro=sec?sec.querySelector(".rotulo"):null;
 var pct;
 if(modo==="continuo"){var alto=zona.scrollHeight-zona.clientHeight;
  pct=alto>0?zona.scrollTop/alto*100:0}
 else pct=total>1?p/(total-1)*100:0;
 return {sec:sec?sec.id:"",cap:(ro?ro.textContent:"")+(h2&&h2.textContent?" · "+h2.textContent:""),
  pct:Math.round(pct),frac:total>1?p/(total-1):0,pag:p,modo:modo,ts:Date.now()};
}
function guardar(){
 var e=estadoActual();
 set("frac",e.frac);set("pag",e.pag);set("pct",e.pct);
 set("sec",e.sec);set("cap",e.cap);set("ts",e.ts);
 if(modo==="continuo")set("scroll",zona.scrollTop);
}
addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden")guardar()});
addEventListener("pagehide",guardar);
addEventListener("blur",guardar);
addEventListener("beforeunload",guardar);
setInterval(function(){if(document.visibilityState==="visible")guardar()},4000);

function haceCuanto(ts){
 var d=Date.now()-ts,m=Math.round(d/60000);
 if(m<2)return "__T_AHORA__";
 if(m<60)return "__T_HACE__ "+m+" __T_MIN__";
 var h=Math.round(m/60);
 if(h<24)return "__T_HACE__ "+h+" __T_HORAS__";
 var dd=Math.round(h/24);
 return "__T_HACE__ "+dd+" __T_DIAS__";
}
function mostrarReanudar(){
 var pct=parseFloat(get("pct","0")),ts=parseFloat(get("ts","0")),cap=get("cap","");
 if(!(pct>1&&ts))return false;
 document.getElementById("rCap").textContent=cap||"—";
 document.getElementById("rMeta").textContent=pct+"% · "+haceCuanto(ts);
 document.getElementById("reanudar").classList.add("on");
 return true;
}
document.getElementById("bSeguir").onclick=function(){
 document.getElementById("reanudar").classList.remove("on");
 var sid=get("sec",""),f=parseFloat(get("frac","0"));
 if(modo==="continuo"){var y=parseFloat(get("scroll","0"));if(y)zona.scrollTop=y;pintar();return}
 medir();
 if(sid&&document.getElementById(sid))aSeccion(sid);
 else ir(Math.round(f*(total-1)),false);
};
document.getElementById("bDesdeCero").onclick=function(){
 document.getElementById("reanudar").classList.remove("on");
 if(modo==="continuo")zona.scrollTop=0; else ir(0,false);
 guardar();
};

}catch(errVoz){if(window.console)console.warn("Lectura en voz alta no disponible:",errVoz)}

try{
function marcas(){try{return JSON.parse(get("marcas","[]"))}catch(e){return[]}}
function pintarMarcas(){
 var L=marcas(),z=document.getElementById("zonaMarcas");
 if(!L.length){z.innerHTML="";return}
 var h='<h4>__TXT_MARCADORES__</h4>';
 L.forEach(function(mk,i){
  h+='<div class="marca"><a href="#'+mk.sec+'" data-f="'+mk.frac+'">'+
     (mk.cap||"—")+'</a><span class="pc">'+mk.pct+'%</span>'+
     '<button data-del="'+i+'" aria-label="__TXT_BORRAR__">✕</button></div>'});
 z.innerHTML=h;
 [].forEach.call(z.querySelectorAll("[data-del]"),function(b){
  b.onclick=function(ev){ev.preventDefault();ev.stopPropagation();
   var L2=marcas();L2.splice(parseInt(b.dataset.del,10),1);
   set("marcas",JSON.stringify(L2));pintarMarcas()}});
}
document.getElementById("bMarca").onclick=function(){
 var e=estadoActual(),L=marcas();
 L.unshift({sec:e.sec,cap:e.cap,pct:e.pct,frac:e.frac,ts:e.ts});
 if(L.length>20)L.pop();
 set("marcas",JSON.stringify(L));pintarMarcas();
 var b=this,t0=b.textContent;b.textContent="✓";
 setTimeout(function(){b.textContent=t0},1300);
};
pintarMarcas();

var URL_PUBLICA="__BASEURL__/__ESTE__";
function enlace(){
 if(URL_PUBLICA)return URL_PUBLICA;
 return location.href.split("#")[0];
}
var compartir=document.getElementById("compartir");
document.getElementById("bComp").onclick=function(){
 var u=enlace();
 document.getElementById("urlTxt").textContent=u;
 var esNoche=H.dataset.tema==="noche"||H.dataset.tema==="contraste";
 try{
  document.getElementById("qrCaja").innerHTML=QR.svg(u,220,"#111111","#ffffff");
 }catch(err){
  document.getElementById("qrCaja").textContent="—";
 }
 abrir(compartir);
};
document.getElementById("bCerrarComp").onclick=cerrar;
document.getElementById("bEnviar").onclick=function(){
 var d={title:document.title,text:"__TXT_TEXTOCOMP__",url:enlace()};
 if(navigator.share)navigator.share(d).catch(function(){});
 else{var b=this;navigator.clipboard&&navigator.clipboard.writeText(enlace());
  b.textContent="__TXT_COPIADO__";setTimeout(function(){b.textContent="__TXT_ENVIAR__"},2000)}
};
document.getElementById("bCopiarUrl").onclick=function(){
 var b=this,u=enlace();
 var ok=function(){b.textContent="__TXT_COPIADO__";
  setTimeout(function(){b.textContent="__TXT_COPIARURL__"},2000)};
 if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,ok);
 else{var x=document.createElement("textarea");x.value=u;document.body.appendChild(x);
  x.select();try{document.execCommand("copy")}catch(e){}x.remove();ok()}
};
document.getElementById("bWa").onclick=function(){
 location.href="https://wa.me/?text="+encodeURIComponent("__TXT_TEXTOCOMP__ "+enlace())};
document.getElementById("bDescargaQR").onclick=function(){
 var svg=document.querySelector("#qrCaja svg");if(!svg)return;
 var blob=new Blob([svg.outerHTML],{type:"image/svg+xml"});
 var a=document.createElement("a");a.href=URL.createObjectURL(blob);
 a.download="qr.svg";a.click();setTimeout(function(){URL.revokeObjectURL(a.href)},2000)};

}catch(errOpc){if(window.console)console.warn("Funciones opcionales no disponibles:",errOpc)}

var rt;addEventListener("resize",function(){clearTimeout(rt);
 rt=setTimeout(function(){recalcular(true)},220)});

aplicar();
ponerModo(get("modo","paginas"));
setTimeout(function(){
 medir();
 var reanudo=false;
 try{reanudo=mostrarReanudar()}catch(e){reanudo=false}
 if(!reanudo){
  var f=parseFloat(get("frac","0"));
  ir(f>0?Math.round(f*(total-1)):0,false);
 }
},80);
addEventListener("load",function(){setTimeout(function(){recalcular(true)},200)});
})();
</script>
</body>
</html>
"""

# ----------------------------------------------------------------- portada
INDEX = r"""<!DOCTYPE html>
<html lang="__LANG__" data-tema="dia">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__SITIO__ — Libros gratuitos para leer donde quieras</title>
<meta name="description" content="Libros completos y gratuitos para leer en el celular, la tablet o el computador. Sin registro, sin publicidad, con lector accesible. Libre uso en colegios y universidades.">
<meta name="theme-color" content="#faf8f4">
<meta property="og:title" content="__SITIO__">
<meta property="og:description" content="Libros completos y gratuitos, pensados para leerse en el celular.">
<meta property="og:image" content="__BASEURL__/__OGIMG__">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="__BASEURL__/__ESTE__">
<meta property="og:locale" content="__LOCALE__">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="__BASEURL__/__ESTE__">
<link rel="alternate" hreflang="es" href="__BASEURL__/index.html">
<link rel="alternate" hreflang="en" href="__BASEURL__/index-en.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script type="application/ld+json">__JSONLD__</script>
<style>
__BASE__
.envoltura{max-width:62rem;margin:0 auto;padding:0 1.4rem}
.barra{position:sticky;top:0;z-index:20;background:var(--papel);
 border-bottom:1px solid var(--linea)}
.barra .in{display:flex;align-items:center;gap:.3rem;padding:.5rem 1.4rem;
 max-width:62rem;margin:0 auto;flex-wrap:nowrap}
.idioma{font-family:system-ui,sans-serif;font-size:.82rem;text-decoration:none;
 color:var(--suave);border:1px solid var(--linea);border-radius:.5rem;
 padding:.6rem .9rem;margin-right:.3rem;min-height:44px;display:inline-flex;align-items:center}
.idioma:hover{background:var(--caja)}
.logo{font-size:1rem;letter-spacing:.02em;margin-right:auto;text-decoration:none;
 white-space:nowrap;flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis}
.etxt{margin-left:.35rem}
@media(max-width:560px){.etxt{display:none}.idioma{padding:.6rem .75rem}
 .barra .in{gap:.3rem;padding:.5rem 1rem}.logo{font-size:.94rem}}
@media(max-width:360px){.logo{font-size:.86rem}}

.hero{display:grid;gap:2.5rem;padding:3rem 0 3.5rem;align-items:center}
@media(min-width:780px){.hero{grid-template-columns:minmax(0,15rem) 1fr;gap:4rem;padding:4.5rem 0 5rem}}
.tomo{perspective:1400px;max-width:15rem;margin:0 auto;width:100%}
.tomo .cuerpo{transform:rotateY(-16deg) rotateX(3deg);transform-style:preserve-3d;
 position:relative;border-radius:2px 6px 6px 2px;overflow:hidden;
 box-shadow:14px 20px 40px rgba(0,0,0,.32),0 2px 6px rgba(0,0,0,.2);
 transition:transform .5s cubic-bezier(.22,.61,.36,1)}
.tomo:hover .cuerpo{transform:rotateY(-7deg) rotateX(1deg)}
.tomo svg{display:block;width:100%;height:auto}
.tomo .lomo{position:absolute;inset:0 auto 0 0;width:11px;
 background:linear-gradient(90deg,rgba(0,0,0,.55),rgba(255,255,255,.06));pointer-events:none}
h1{font-size:clamp(2.1rem,6.2vw,3.4rem);font-weight:400;line-height:1.08;letter-spacing:.005em}
.claim{color:var(--suave);font-size:1.05rem;margin-top:1.1rem;font-style:italic}
.sinopsis{margin-top:1.6rem;max-width:36rem}
.sinopsis p{margin-bottom:.9rem;text-align:justify;hyphens:auto}
.acciones{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1.9rem}
.principal{background:var(--marca);color:var(--papel);border-color:var(--marca);
 padding:0 1.6rem;font-size:.95rem;text-decoration:none;border-radius:.5rem;
 min-height:44px;display:inline-flex;align-items:center;border:1px solid var(--marca)}
.principal:hover{opacity:.88}
.datos{display:flex;gap:1.6rem;flex-wrap:wrap;margin-top:1.8rem;
 font-family:system-ui,sans-serif;font-size:.8rem;color:var(--suave)}
.datos b{display:block;font-size:1.35rem;color:var(--tinta);font-weight:400;font-family:var(--fam)}

.franja{border-top:1px solid var(--linea);border-bottom:1px solid var(--linea);
 background:var(--caja);padding:3.2rem 0}
.rot{font-family:system-ui,sans-serif;font-size:.7rem;letter-spacing:.2em;
 text-transform:uppercase;color:var(--suave);margin-bottom:1.4rem}
.grande{font-size:clamp(1.4rem,3.6vw,2rem);line-height:1.35;font-weight:400;
 max-width:42rem;margin-bottom:1.2rem}
.grande em{font-style:italic;color:var(--acento)}
.parrafo{max-width:38rem}
.parrafo p{margin-bottom:.9rem;text-align:justify;hyphens:auto}
.rejilla{display:grid;gap:1.1rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))}
.tarjeta{border:1px solid var(--linea);border-radius:.8rem;padding:1.3rem;background:var(--papel)}
.tarjeta h3{font-weight:400;font-size:1.1rem;margin-bottom:.4rem}
.tarjeta p{font-size:.92rem;color:var(--suave);line-height:1.6}
.tarjeta .ico{font-size:1.4rem;display:block;margin-bottom:.6rem;color:var(--acento)}

.docentes{padding:3.4rem 0}
.permiso{border:1px solid var(--acento);border-radius:.8rem;padding:1.5rem;
 background:var(--caja);max-width:42rem;margin-top:1.2rem}
.permiso ul{list-style:none;margin:1rem 0}
.permiso li{padding:.4rem 0 .4rem 1.6rem;position:relative;font-size:.96rem}
.permiso li:before{content:"✓";position:absolute;left:0;color:var(--acento)}
.permiso .no{color:var(--suave);font-size:.9rem;margin-top:1rem}
.licencia{font-family:system-ui,sans-serif;font-size:.78rem;letter-spacing:.1em;
 text-transform:uppercase;color:var(--acento);margin-top:1.2rem;display:block}

.difundir{border-top:1px solid var(--linea);background:var(--caja);padding:3.4rem 0}
.kit{display:grid;gap:1.6rem;grid-template-columns:1fr;margin-top:1.6rem}
@media(min-width:760px){.kit{grid-template-columns:auto 1fr;gap:2.4rem}}
.qrbox{background:#fff;border:1px solid var(--linea);border-radius:.8rem;
 padding:1rem;text-align:center;width:min(15rem,100%);margin:0 auto}
.qrbox svg{display:block;width:100%;height:auto}
.qrbox .pie{font-family:system-ui,sans-serif;font-size:.7rem;color:#666;margin-top:.6rem}
.textos{display:grid;gap:.9rem}
.texto{border:1px solid var(--linea);border-radius:.7rem;background:var(--papel);
 padding:1rem 1.1rem}
.texto p{font-size:.95rem;margin-bottom:.7rem;white-space:pre-line}
.texto .acc{display:flex;gap:.5rem;flex-wrap:wrap}
.texto button{font-size:.82rem;min-height:40px}
.enlaces{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:1.4rem}
.enlaces a{font-family:system-ui,sans-serif;font-size:.85rem;text-decoration:none;
 border:1px solid var(--linea);border-radius:.5rem;padding:.65rem 1rem;
 min-height:44px;display:inline-flex;align-items:center;background:var(--papel)}
.enlaces a:hover{border-color:var(--acento)}

.catalogo{padding:3.4rem 0}
.libro{display:grid;grid-template-columns:6.5rem 1fr;gap:1.3rem;
 border:1px solid var(--linea);border-radius:.8rem;padding:1.2rem;
 text-decoration:none;background:var(--caja);align-items:start;margin-bottom:1rem}
.libro:hover{border-color:var(--acento)}
.libro .mini{border-radius:2px;overflow:hidden;box-shadow:3px 4px 12px rgba(0,0,0,.25)}
.libro .mini svg{display:block;width:100%;height:auto}
.libro .tit{font-size:1.3rem;line-height:1.2;display:block}
.libro .des{color:var(--suave);font-size:.92rem;margin-top:.5rem;line-height:1.6}
.libro .meta{font-family:system-ui,sans-serif;font-size:.68rem;letter-spacing:.1em;
 text-transform:uppercase;color:var(--acento);margin-top:.9rem;display:block}
.hueco{display:grid;grid-template-columns:6.5rem 1fr;gap:1.3rem;align-items:center;
 border:1px dashed var(--linea);border-radius:.8rem;padding:1.2rem;margin-bottom:1rem}
.hueco .lomoV{height:9.2rem;border:1px dashed var(--linea);border-radius:2px;
 background:repeating-linear-gradient(135deg,transparent,transparent 7px,
 var(--linea) 7px,var(--linea) 8px);opacity:.5}
.hueco .tit{font-size:1.15rem;line-height:1.25;display:block;color:var(--suave)}
.hueco .des{color:var(--suave);font-size:.9rem;margin-top:.45rem;display:block;
 font-style:italic;opacity:.85}
.nota{border-left:2px solid var(--acento);padding:.2rem 0 .2rem 1.4rem;
 margin:2.6rem 0 1rem;max-width:38rem}
.nota h3{font-family:system-ui,sans-serif;font-size:.7rem;letter-spacing:.2em;
 text-transform:uppercase;color:var(--suave);font-weight:500;margin-bottom:.9rem}
.nota p{margin-bottom:.85rem;text-align:justify;hyphens:auto;font-size:.98rem}
.nota .firma{font-style:italic;color:var(--suave);text-align:left;margin-top:1.2rem}
.pie{border-top:1px solid var(--linea);padding:2.4rem 0 3rem;color:var(--suave);
 font-family:system-ui,sans-serif;font-size:.82rem}
.pie a{color:var(--suave)}
.velo{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:90;display:none}
.velo.on{display:block}
.hoja{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:100;
 background:var(--papel);border:1px solid var(--linea);border-radius:.9rem;
 padding:1.3rem;width:min(24rem,92vw);display:none;max-height:90svh;overflow:auto}
.hoja.on{display:block}
.cabpanel{display:flex;align-items:center;justify-content:space-between;
 font-family:system-ui,sans-serif;margin-bottom:.6rem}
.notaComp{font-size:.85rem;color:var(--suave);font-family:system-ui,sans-serif;margin-bottom:.9rem}
.qrCaja{display:flex;justify-content:center;padding:.9rem;background:#fff;
 border:1px solid var(--linea);border-radius:.7rem}
.qrCaja svg{display:block;max-width:100%;height:auto}
.urlTxt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.76rem;
 word-break:break-all;color:var(--suave);text-align:center;margin:.7rem 0 .9rem}
.filaB{display:flex;gap:.45rem;flex-wrap:wrap}
.filaB button{flex:1;min-width:6rem}
@media(min-width:700px){:root{--fs:1.14rem}}
</style>
</head>
<body>
<a class="saltar" href="#principal">Saltar al contenido</a>

<div class="barra"><div class="in">
 <a class="logo" href="index.html">__SITIO__</a>
 <button id="bCompIdx" aria-label="Compartir este sitio">↗<span class="etxt">Compartir</span></button>
 <button id="bTema" aria-label="Cambiar entre modo claro y oscuro">◐<span class="etxt">Tema</span></button>
</div></div>

<main id="principal">
<div class="envoltura">
 <div class="hero">
  <div class="tomo"><div class="cuerpo">__CUBIERTA__<div class="lomo"></div></div></div>
  <div>
   <h1>Fabricantes de sed</h1>
   <p class="claim">Una novela sobre la persuasión, la verdad y el precio de las palabras.</p>
   <div class="sinopsis">
    <p>Tomás Alcázar es el publicista más premiado en lengua española y le queda un solo encargo: enseñarle a mentir a una máquina. Para entrenarla debe recorrer, documento a documento, toda la historia del convencimiento humano.</p>
    <p>Mientras lo hace, alguien empieza a meter bajo su puerta fotocopias de sus propios cuadernos de juventud, subrayadas por una mano que no es la suya.</p>
   </div>
   <div class="acciones">
    <a href="fabricantes-de-sed.html" class="principal">Leer ahora, gratis</a>
    <a href="#difundir" style="text-decoration:none"><button>Difundirlo</button></a>
   </div>
   <div class="datos">
    <span><b>12</b> capítulos</span>
    <span><b>6</b> interludios</span>
    <span><b>~3 h</b> de lectura</span>
    <span><b>0 $</b> siempre</span>
   </div>
  </div>
 </div>
</div>

<div class="franja"><div class="envoltura">
 <p class="rot">Por qué existe esto</p>
 <p class="grande">La mayoría de la gente no dejó de leer. Dejó de <em>terminar</em> lo que empieza.</p>
 <div class="parrafo">
  <p>Casi nadie abandona un libro porque sea malo. Lo abandona porque lo empezó en el sofá un domingo y no volvió a encontrar ese hueco. Porque en el bus no se puede sostener un tomo con una mano. Porque la letra era pequeña, o el archivo pesaba demasiado, o al reanudar ya no sabía por dónde iba.</p>
  <p>Nada de eso tiene que ver con las ganas de leer. Tiene que ver con el sitio y el momento en que hoy se lee, que es de pie, en trayectos de veinte minutos, en una pantalla de seis pulgadas.</p>
  <p>Esta biblioteca está hecha para ese momento. Los libros son completos, gratuitos y están pensados para leerse a pedazos sin perder el hilo.</p>
 </div>
</div></div>

<div class="envoltura" style="padding:3.4rem 0">
 <p class="rot">Pensado para leerse en el bus</p>
 <div class="rejilla">
  <div class="tarjeta"><span class="ico" aria-hidden="true">❯</span>
   <h3>Se pasa página</h3>
   <p>Deslice el dedo o toque el borde de la pantalla. Nada de scroll infinito perdiendo el renglón en cada frenada.</p></div>
  <div class="tarjeta"><span class="ico" aria-hidden="true">A</span>
   <h3>Letra hasta el 200%</h3>
   <p>El libro se repagina solo. Suba el tamaño cuanto necesite: nunca se corta ni se sale del margen.</p></div>
  <div class="tarjeta"><span class="ico" aria-hidden="true">◐</span>
   <h3>Cuatro modos de color</h3>
   <p>Claro, sepia, oscuro y alto contraste en amarillo sobre negro para baja visión.</p></div>
  <div class="tarjeta"><span class="ico" aria-hidden="true">♪</span>
   <h3>Lectura en voz alta</h3>
   <p>Con la voz que ya trae su teléfono. El libro se convierte en audiolibro y sigue solo al pasar de página.</p></div>
  <div class="tarjeta"><span class="ico" aria-hidden="true">↩</span>
   <h3>Recuerda dónde iba</h3>
   <p>Cierre cuando quiera, aunque entre una llamada. Al volver, abre en el capítulo donde lo dejó.</p></div>
  <div class="tarjeta"><span class="ico" aria-hidden="true">✈</span>
   <h3>Funciona sin datos</h3>
   <p>El libro entero pesa lo que una foto. Una vez abierto, se lee sin señal en todo el trayecto.</p></div>
 </div>
</div>

<div class="franja" id="docentes"><div class="envoltura docentes" style="padding-top:0;padding-bottom:0">
 <p class="rot">Para profesores, colegios y bibliotecas</p>
 <p class="grande">Sí, puede usarlo en clase. No hace falta que escriba a pedir permiso.</p>
 <div class="permiso">
  <p style="font-family:system-ui,sans-serif;font-size:.9rem;color:var(--suave)">Queda autorizado, por adelantado y sin trámite, a:</p>
  <ul>
   <li>Imprimirlo y fotocopiarlo, entero o por capítulos</li>
   <li>Proyectarlo y leerlo en voz alta en el aula</li>
   <li>Subirlo al aula virtual o a la intranet del colegio</li>
   <li>Ponerlo como lectura obligatoria u optativa</li>
   <li>Repartir el enlace y el código QR por donde quiera</li>
   <li>Guardarlo en el catálogo de la biblioteca</li>
  </ul>
  <p class="no">Lo único que no puede hacerse es venderlo ni publicar versiones modificadas. Basta con citar al autor.</p>
  <span class="licencia">Licencia CC BY-NC-ND 4.0</span>
 </div>
 <p style="max-width:38rem;margin-top:1.6rem;color:var(--suave);font-size:.95rem">
  Sobre el contenido: la novela trata de publicidad, manipulación y honestidad. No contiene violencia explícita ni sexo. Es apropiada de <strong>15 años en adelante</strong>, y funciona especialmente bien en clases de ética, comunicación, filosofía, lengua y medios.</p>
</div></div>

<div class="difundir" id="difundir"><div class="envoltura">
 <p class="rot">Difúndalo</p>
 <p class="grande">Un libro que nadie pasa a nadie es un libro que no existe.</p>
 <p class="parrafo" style="margin-bottom:1rem">Aquí está todo lo que necesita para repartirlo: el código, los textos y el cartel para imprimir. Tómelo y úselo sin avisar.</p>

 <div class="kit">
  <div>
   <div class="qrbox">
    <div id="qrKit"></div>
    <div class="pie">Apunte la cámara del celular</div>
   </div>
   <div class="enlaces" style="justify-content:center">
    <a href="#" id="bajarQR" download="qr-libros-para-pensar.svg">Descargar código</a>
   </div>
  </div>

  <div class="textos">
   <div class="texto">
    <p id="t1">Escribí una novela para leer en el bus.

Un hombre que se ganó la vida convenciendo a otros empieza a recibir de vuelta sus propios cuadernos de juventud, página a página.

Tres horas. Gratis, completa, y funciona sin señal.

__BASEURL__</p>
    <div class="acc"><button data-copiar="t1">Copiar este texto</button></div>
   </div>
   <div class="texto">
    <p id="t2">Una novela completa y gratis, pensada para leerse en el celular: se pasa página, sube la letra hasta el 200%, se lee en voz alta y funciona sin datos.

Libre para usar en clase.

__BASEURL__</p>
    <div class="acc"><button data-copiar="t2">Copiar este texto</button></div>
   </div>
  </div>
 </div>

 <div class="enlaces">
  <a href="cartel.html" target="_blank" rel="noopener">Cartel para imprimir</a>
  <a href="og-es.png" download>Imagen para redes</a>
  <a href="cubierta.svg" download>Cubierta del libro</a>
  <a href="#" id="waKit">Enviar por WhatsApp</a>
 </div>
</div></div>

<div class="envoltura catalogo">
 <p class="rot">Catálogo</p>
 <a class="libro" href="fabricantes-de-sed.html">
  <span class="mini">__MINI__</span>
  <span>
   <span class="tit">Fabricantes de sed</span>
   <span class="des">El hombre que enseñó al mundo a desear recibe su propio cuaderno de juventud de vuelta — y descubre que la única persuasión que nunca ha probado es la verdad.</span>
   <span class="meta">Novela · Dawin Salazar · Leer ahora</span>
  </span>
 </a>

 <div class="hueco">
  <div class="lomoV"></div>
  <div>
   <span class="tit">El segundo libro aparecerá aquí</span>
   <span class="des">Sin fecha. Cuando esté terminado, no antes.</span>
  </div>
 </div>

 <div class="nota">
  <h3>Sobre esta biblioteca</h3>
  <p>Aquí va a haber más libros. No sé cuántos ni cuándo: escribo de noche, después del trabajo, y el primero me llevó meses. Lo que sí puedo decir es en qué condiciones van a salir, porque eso no depende de la inspiración.</p>
  <p>Completos. Gratis. Desde el primer día. Sin capítulo de muestra que se corta cuando la cosa se pone interesante, sin registro y sin publicidad.</p>
  <p>Si quiere enterarse del siguiente, lo más simple es guardar esta página en sus marcadores. No hay lista de correo. Si algún día la hay, será para avisar de un libro nuevo y para nada más.</p>
  <p class="firma">Dawin Salazar</p>
 </div>
</div>
</main>

<div class="velo" id="velo"></div>
<div class="hoja" id="hojaComp" role="dialog" aria-modal="true" aria-label="Compartir">
 <div class="cabpanel"><strong>Compartir</strong><button id="bCerrarHoja" aria-label="Cerrar">✕</button></div>
 <p class="notaComp">Enséñele este código a alguien: con la cámara del teléfono abre la biblioteca. O envíe el enlace.</p>
 <div id="qrCaja" class="qrCaja"></div>
 <p class="urlTxt" id="urlTxt"></p>
 <div class="filaB">
  <button id="bEnviar">Compartir…</button>
  <button id="bCopiarUrl">Copiar enlace</button>
  <button id="bWa">WhatsApp</button>
 </div>
</div>

<footer class="pie"><div class="envoltura">
 __SITIO__ · Lectura libre · Sin registro, sin publicidad, sin rastreo.<br>
 Textos de Dawin Salazar bajo licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es" rel="license noopener" target="_blank">CC BY-NC-ND 4.0</a>.
</div></footer>

<script>__QRJS__</script>
<script>
(function(){
 var H=document.documentElement,K="lpp:";
 var t=localStorage.getItem(K+"tema");if(t)H.dataset.tema=t;
 document.getElementById("bTema").onclick=function(){
  var n=H.dataset.tema==="noche"?"dia":"noche";H.dataset.tema=n;
  localStorage.setItem(K+"tema",n);
  document.querySelector('meta[name=theme-color]').content=n==="noche"?"#14120f":"#faf8f4"};

 var velo=document.getElementById("velo"),hoja=document.getElementById("hojaComp");
 function u(){return location.href.split("#")[0]}
 document.getElementById("bCompIdx").onclick=function(){
  document.getElementById("urlTxt").textContent=u();
  try{document.getElementById("qrCaja").innerHTML=QR.svg(u(),230,"#111111","#ffffff")}
  catch(e){document.getElementById("qrCaja").textContent="—"}
  hoja.classList.add("on");velo.classList.add("on")};
 function cerrarH(){hoja.classList.remove("on");velo.classList.remove("on")}
 document.getElementById("bCerrarHoja").onclick=cerrarH;
 velo.onclick=cerrarH;
 addEventListener("keydown",function(e){if(e.key==="Escape")cerrarH()});
 document.getElementById("bEnviar").onclick=function(){
  var d={title:document.title,url:u()};
  if(navigator.share)navigator.share(d).catch(function(){});
  else{navigator.clipboard&&navigator.clipboard.writeText(u());this.textContent="Copiado ✓"}};
 var c=document.getElementById("bCopiarUrl");
 var etiquetaC=c.textContent;
 c.onclick=function(){
  var ok=function(){c.textContent="Copiado ✓";
   setTimeout(function(){c.textContent=etiquetaC},2000)};
  if(navigator.clipboard)navigator.clipboard.writeText(u()).then(ok,ok);else ok()};
 document.getElementById("bWa").onclick=function(){
  location.href="https://wa.me/?text="+encodeURIComponent(u())};

 try{
  var svgKit=QR.svg("__BASEURL__",300,"#111111","#ffffff");
  document.getElementById("qrKit").innerHTML=svgKit;
  var b=new Blob([svgKit],{type:"image/svg+xml"});
  document.getElementById("bajarQR").href=URL.createObjectURL(b);
 }catch(e){}

 [].forEach.call(document.querySelectorAll("[data-copiar]"),function(b){
  var et=b.textContent;
  b.onclick=function(){
   var txt=document.getElementById(b.dataset.copiar).textContent;
   var ok=function(){b.textContent="Copiado ✓";
    setTimeout(function(){b.textContent=et},2000)};
   if(navigator.clipboard)navigator.clipboard.writeText(txt).then(ok,ok);else ok()}});

 var wa=document.getElementById("waKit");
 if(wa)wa.onclick=function(e){e.preventDefault();
  location.href="https://wa.me/?text="+encodeURIComponent(
   document.getElementById("t1").textContent)};
})();
</script>
</body>
</html>
"""



APORTE_ES = """<p style="text-indent:0">Este libro es gratis y va a seguir siéndolo. No pido dinero: no hay ninguna cuenta al final de esta página.</p>
     <p style="text-indent:0"><strong>Lo único que pido es que se lo pase a una persona.</strong> La que se le haya venido a la cabeza mientras leía.</p>
     <p style="text-indent:0">Y si es usted profesor o bibliotecario: puede imprimirlo, proyectarlo, repartirlo y pedirlo como lectura. El permiso está dado por escrito.</p>
     <div class="caja-cuenta">
      <div class="banco">Compartir</div>
      <div class="num" id="numCuenta">libros-para-pensar.netlify.app</div>
      <button id="bCopiar">Copiar enlace</button>
      <div class="extra">Léalo gratis · Compártalo libre · CC BY-NC-ND 4.0</div>
     </div>"""

APORTE_EN = """<p style="text-indent:0">This book is free and will stay free. I am not asking for money: there is no account number at the bottom of this page.</p>
     <p style="text-indent:0"><strong>All I ask is that you pass it on to one person.</strong> The one who came into your head while you were reading.</p>
     <p style="text-indent:0">And if you are a teacher or a librarian: you may print it, project it, hand it out and set it as reading. The permission is already given, in writing.</p>
     <div class="caja-cuenta">
      <div class="banco">Share</div>
      <div class="num" id="numCuenta">libros-para-pensar.netlify.app</div>
      <button id="bCopiar">Copy link</button>
      <div class="extra">Free to read · Free to share · CC BY-NC-ND 4.0</div>
     </div>"""

UI_ES = dict(TXT_BIB="Biblioteca", TXT_VOZ="Lectura en voz alta", TXT_IDX="Índice",
  TXT_AJU="Ajustes de lectura", TXT_ANT="Página anterior", TXT_SIG="Página siguiente",
  TXT_SALTAR="Saltar al texto del libro", TXT_TAM="Tamaño de letra", TXT_TIP="Tipografía",
  TXT_COL="Color", TXT_ESP="Espaciado", TXT_MOD="Modo de lectura", TXT_LEG="Alta legibilidad",
  TXT_CLA="Claro", TXT_SEP="Sepia", TXT_OSC="Oscuro", TXT_CON="Alto contraste",
  TXT_CMP="Compacto", TXT_NRM="Normal", TXT_AMP="Amplio", TXT_LN="Letras normales",
  TXT_LS="Letras separadas", TXT_PAG="Pasar páginas", TXT_SCR="Desplazamiento",
  TXT_LEN="Lenta", TXT_RAP="Rápida", TXT_FIN="Fin", TXT_ULT="Una última cosa",
  TXT_VOLVER="Volver a la biblioteca", TXT_MLEN="Muy lenta",
  TXT_ELIGEVOZ="Elegir voz",
  TXT_NOTAVOZ="Usa las voces instaladas en su teléfono o computador. Si suena metálica, pruebe otra en la lista: las que dicen «Natural» u «Online» son las mejores. Pulse ▶ arriba para empezar.",
  TXT_SINVOZ="Su navegador no permite la lectura en voz alta.",
  TXT_PARARVOZ="Detener la lectura en voz alta",
  TXT_MARCAR="Guardar un marcador aquí", TXT_COMPARTIR="Compartir el libro",
  TXT_MARCADORES="Sus marcadores", TXT_BORRAR="Borrar marcador",
  TXT_NOTACOMP="Enséñele este código a alguien: con la cámara del teléfono abre el libro. O envíe el enlace.",
  TXT_ENVIAR="Compartir…", TXT_COPIARURL="Copiar enlace", TXT_COPIADO="Copiado ✓",
  TXT_BAJARQR="Descargar QR", TXT_IBAPOR="Iba por aquí",
  TXT_CONTINUAR="Continuar", TXT_DESDECERO="Empezar de nuevo",
  TXT_TEXTOCOMP="Le comparto este libro. Es gratis y se lee completo:",
  T_AHORA="hace un momento", T_HACE="hace", T_MIN="minutos", T_HORAS="horas", T_DIAS="días",
  T_PAG="Página", T_DE="de", T_LEIDO="leído", TXT_VASAQUI="va por aquí")

UI_EN = dict(TXT_BIB="Library", TXT_VOZ="Read aloud", TXT_IDX="Contents",
  TXT_AJU="Reading settings", TXT_ANT="Previous page", TXT_SIG="Next page",
  TXT_SALTAR="Skip to the text of the book", TXT_TAM="Text size", TXT_TIP="Typeface",
  TXT_COL="Colour", TXT_ESP="Spacing", TXT_MOD="Reading mode", TXT_LEG="High legibility",
  TXT_CLA="Light", TXT_SEP="Sepia", TXT_OSC="Dark", TXT_CON="High contrast",
  TXT_CMP="Tight", TXT_NRM="Normal", TXT_AMP="Loose", TXT_LN="Normal letters",
  TXT_LS="Spaced letters", TXT_PAG="Page turn", TXT_SCR="Scrolling",
  TXT_LEN="Slow", TXT_RAP="Fast", TXT_FIN="The end", TXT_ULT="One last thing",
  TXT_VOLVER="Back to the library", TXT_MLEN="Very slow",
  TXT_ELIGEVOZ="Choose a voice",
  TXT_NOTAVOZ="Uses the voices installed on your phone or computer. If it sounds metallic, try another one from the list: the ones marked “Natural” or “Online” are the best. Press ▶ above to start.",
  TXT_SINVOZ="Your browser does not support read-aloud.",
  TXT_PARARVOZ="Stop reading aloud",
  TXT_MARCAR="Save a bookmark here", TXT_COMPARTIR="Share this book",
  TXT_MARCADORES="Your bookmarks", TXT_BORRAR="Delete bookmark",
  TXT_NOTACOMP="Show this code to someone: their phone camera opens the book. Or send the link.",
  TXT_ENVIAR="Share…", TXT_COPIARURL="Copy link", TXT_COPIADO="Copied ✓",
  TXT_BAJARQR="Download QR", TXT_IBAPOR="You were here",
  TXT_CONTINUAR="Continue", TXT_DESDECERO="Start again",
  TXT_TEXTOCOMP="Sharing this book with you. It's free and complete:",
  T_AHORA="just now", T_HACE="", T_MIN="minutes ago", T_HORAS="hours ago", T_DIAS="days ago",
  T_PAG="Page", T_DE="of", T_LEIDO="read", TXT_VASAQUI="you are here")

IDX_EN = {
 "cartel.html":"poster.html",
 "https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es":"https://creativecommons.org/licenses/by-nc-nd/4.0/",
 "og-es.png":"og-en.png",
 "Textos de Dawin Salazar bajo licencia":"Texts by Dawin Salazar under licence",
 "Libre para usar en clase.":"Free to use in class.",
 "Una novela completa y gratis, pensada para leerse en el celular: se pasa página, sube la letra hasta el 200%, se lee en voz alta y funciona sin datos.":"A complete, free novel built to be read on a phone: real page turns, text up to 200%, read-aloud, and it works with no data.",
 "Tres horas. Gratis, completa, y funciona sin señal.":"Three hours. Free, complete, and it works underground.",
 "Un hombre que se ganó la vida convenciendo a otros empieza a recibir de vuelta sus propios cuadernos de juventud, página a página.":"A man who made his living convincing people starts getting his own old notebooks back, one page at a time.",
 "Escribí una novela para leer en el bus.":"I wrote a novel to be read on the bus.",
 "Enviar por WhatsApp":"Send on WhatsApp",
 "Cubierta del libro":"Book cover",
 "Imagen para redes":"Image for social",
 "Cartel para imprimir":"Poster to print",
 "Copiar este texto":"Copy this text",
 "Descargar código":"Download the code",
 "Apunte la cámara del celular":"Point your phone camera",
 "Aquí está todo lo que necesita para repartirlo: el código, los textos y el cartel para imprimir. Tómelo y úselo sin avisar.":"Here is everything you need to hand it out: the code, the texts and a poster to print. Take it and use it without asking.",
 "Un libro que nadie pasa a nadie es un libro que no existe.":"A book nobody passes to anybody is a book that doesn't exist.",
 "Difúndalo":"Spread it",
 "Sobre el contenido: la novela trata de publicidad, manipulación y honestidad. No contiene violencia explícita ni sexo. Es apropiada de <strong>15 años en adelante</strong>, y funciona especialmente bien en clases de ética, comunicación, filosofía, lengua y medios.":"On content: the novel is about advertising, manipulation and honesty. It contains no explicit violence and no sex. Suitable from <strong>age 15 up</strong>, and it works particularly well in ethics, communication, philosophy, language and media classes.",
 "Licencia CC BY-NC-ND 4.0":"CC BY-NC-ND 4.0 licence",
 "Lo único que no puede hacerse es venderlo ni publicar versiones modificadas. Basta con citar al autor.":"The only things you can't do are sell it or publish modified versions. Just credit the author.",
 "Guardarlo en el catálogo de la biblioteca":"Add it to the library catalogue",
 "Repartir el enlace y el código QR por donde quiera":"Hand out the link and the QR code anywhere you like",
 "Ponerlo como lectura obligatoria u optativa":"Set it as required or optional reading",
 "Subirlo al aula virtual o a la intranet del colegio":"Upload it to your virtual classroom or school intranet",
 "Proyectarlo y leerlo en voz alta en el aula":"Project it and read it aloud in class",
 "Imprimirlo y fotocopiarlo, entero o por capítulos":"Print and photocopy it, whole or by chapters",
 "Queda autorizado, por adelantado y sin trámite, a:":"You are authorised, in advance and with no paperwork, to:",
 "Sí, puede usarlo en clase. No hace falta que escriba a pedir permiso.":"Yes, you can use it in class. No need to write and ask permission.",
 "Para profesores, colegios y bibliotecas":"For teachers, schools and libraries",
 "Cierre cuando quiera, aunque entre una llamada. Al volver, abre en el capítulo donde lo dejó.":"Close it whenever, even if a call comes in. It reopens at the chapter you left.",
 "Esta biblioteca está hecha para ese momento. Los libros son completos, gratuitos y están pensados para leerse a pedazos sin perder el hilo.":"This library is built for that moment. The books are complete, free, and made to be read in pieces without losing the thread.",
 "Nada de eso tiene que ver con las ganas de leer. Tiene que ver con el sitio y el momento en que hoy se lee, que es de pie, en trayectos de veinte minutos, en una pantalla de seis pulgadas.":"None of that has anything to do with wanting to read. It has to do with where and when reading actually happens now: standing up, in twenty-minute journeys, on a six-inch screen.",
 "Casi nadie abandona un libro porque sea malo. Lo abandona porque lo empezó en el sofá un domingo y no volvió a encontrar ese hueco. Porque en el bus no se puede sostener un tomo con una mano. Porque la letra era pequeña, o el archivo pesaba demasiado, o al reanudar ya no sabía por dónde iba.":"Almost nobody abandons a book because it's bad. They abandon it because they started it on the sofa on a Sunday and never found that gap again. Because you can't hold a hardback with one hand on the bus. Because the text was too small, or the file too heavy, or because coming back they'd lost their place.",
 "La mayoría de la gente no dejó de leer. Dejó de <em>terminar</em> lo que empieza.":"Most people didn't stop reading. They stopped <em>finishing</em> what they start.",
 "Por qué existe esto":"Why this exists",
 "Difundirlo":"Share it",
 "Libros completos y gratuitos para leer en el celular, la tablet o el computador. Sin registro, sin publicidad, con lector accesible. Libre uso en colegios y universidades.":"Complete, free books to read on your phone, tablet or computer. No sign-up, no advertising, accessible reader. Free to use in schools and universities.",
 "c.textContent=\"Copiado ✓\"":"c.textContent=\"Copied ✓\"",
 "aria-label=\"Compartir\">":"aria-label=\"Share\">",
 "b.textContent=\"Copiar enlace\"":"b.textContent=\"Copy link\"",
 "b.textContent=\"Copiado ✓\"":"b.textContent=\"Copied ✓\"",
 "this.textContent=\"Copiado ✓\"":"this.textContent=\"Copied ✓\"",
 ">Copiar enlace<":">Copy link<",
 ">Compartir…<":">Share…<",
 "Enséñele este código a alguien: con la cámara del teléfono abre la biblioteca. O envíe el enlace.":"Show this code to someone: their phone camera opens the library. Or send the link.",
 "aria-label=\"Cerrar\">✕":"aria-label=\"Close\">✕",
 "<strong>Compartir</strong>":"<strong>Share</strong>",
 "aria-label=\"Cambiar entre modo claro y oscuro\"":"aria-label=\"Switch between light and dark mode\"",
 "aria-label=\"Compartir este sitio\"":"aria-label=\"Share this site\"",
 "class=\"etxt\">Tema":"class=\"etxt\">Theme",
 "class=\"etxt\">Compartir":"class=\"etxt\">Share",
 "Sin fecha. Cuando esté terminado, no antes.":"No date. When it's finished, not before.",
 "El segundo libro aparecerá aquí":"The second book will appear here",
 "Si quiere enterarse del siguiente, lo más simple es guardar esta página en sus marcadores. No hay lista de correo. Si algún día la hay, será para avisar de un libro nuevo y para nada más.":"If you want to know when the next one appears, the simplest thing is to bookmark this page. There is no mailing list. If there ever is one, it will be to announce a new book and nothing else.",
 "Completos. Gratis. Desde el primer día. Sin capítulo de muestra que se corta cuando la cosa se pone interesante, sin registro y sin publicidad.":"Complete. Free. From day one. No sample chapter that stops just as it gets interesting, no sign-up, no advertising.",
 "Aquí va a haber más libros. No sé cuántos ni cuándo: escribo de noche, después del trabajo, y el primero me llevó meses. Lo que sí puedo decir es en qué condiciones van a salir, porque eso no depende de la inspiración.":"There will be more books here. I don't know how many or when: I write at night, after work, and the first one took me months. What I can tell you is the terms they will come out on, because that part doesn't depend on inspiration.",
 "Sobre esta biblioteca":"About this library",
 "Libros gratuitos para leer donde quieras":"Free books to read anywhere",
 "Libros completos y gratuitos, pensados para leerse en el celular. Sin registro, sin muro de pago, con lector accesible.":"Complete, free books built to be read on a phone. No sign-up, no paywall, accessible reader.",
 "Libros completos y gratuitos, pensados para leerse en el celular.":"Complete, free books built to be read on a phone.",
 "Saltar al contenido":"Skip to content",
 "Cambiar entre modo claro y oscuro":"Switch between light and dark mode",
 "◐ Tema":"◐ Theme",
 "Fabricantes de sed":"Thirst Makers",
 "Una novela sobre la persuasión, la verdad y el precio de las palabras.":"A novel about persuasion, truth, and the price of words.",
 "Tomás Alcázar es el publicista más premiado en lengua española y le queda un solo encargo: enseñarle a mentir a una máquina. Para entrenarla debe recorrer, documento a documento, toda la historia del convencimiento humano.":"Tomás Alcázar is the most awarded advertising man in the Spanish language, and he has one commission left: to teach a machine how to lie. To train it he must work through the entire history of human persuasion, document by document.",
 "Mientras lo hace, alguien empieza a meter bajo su puerta fotocopias de sus propios cuadernos de juventud, subrayadas por una mano que no es la suya.":"While he does, someone begins pushing photocopies of his own youthful notebooks under his door, underlined in a hand that is not his.",
 "Leer ahora, gratis":"Read now, free",
 "Apoyar el proyecto":"Support the campaign",
 "capítulos":"chapters","interludios":"interludes",
 "de lectura":"reading time","siempre":"always",
 "Pensado para leerse en el bus":"Built for the bus",
 "Se pasa página":"Real page turns",
 "Deslice el dedo o toque el borde de la pantalla. Nada de scroll infinito perdiendo el renglón en cada frenada.":"Swipe, or tap the edge of the screen. No endless scroll losing your line at every stop.",
 "Letra hasta el 200%":"Text up to 200%",
 "El libro se repagina solo. Suba el tamaño cuanto necesite: nunca se corta ni se sale del margen.":"The book repaginates itself. Raise the size as far as you need: nothing is ever cut off.",
 "Cuatro modos de color":"Four colour modes",
 "Claro, sepia, oscuro y alto contraste en amarillo sobre negro para baja visión.":"Light, sepia, dark, and high contrast in yellow on black for low vision.",
 "Lectura en voz alta":"Read aloud",
 "Con la voz que ya trae su teléfono. El libro se convierte en audiolibro y sigue solo al pasar de página.":"Using the voice already on your phone. The book becomes an audiobook and turns its own pages.",
 "Recuerda dónde iba":"Remembers your place",
 "Cierre cuando quiera. Al volver, abre exactamente en la página donde lo dejó.":"Close it whenever. It reopens on exactly the page you left.",
 "Funciona sin datos":"Works without data",
 "El libro entero pesa lo que una foto. Una vez abierto, se lee sin señal en todo el trayecto.":"The whole book weighs what a photo does. Once open, it reads with no signal at all.",
 "Catálogo":"Catalogue",
 "El hombre que enseñó al mundo a desear recibe su propio cuaderno de juventud de vuelta — y descubre que la única persuasión que nunca ha probado es la verdad.":"The man who taught the world to want gets his own youthful notebook back — and discovers that the one form of persuasion he has never tried is the truth.",
 "Novela · Dawin Salazar · Leer ahora":"A novel · Dawin Salazar · Read now",
 "Próximo título":"Next title",
 "En preparación. Reemplace este bloque cuando esté listo.":"In preparation.",
 "Aportes":"Contributions",
 "Lectura libre · Sin registro, sin publicidad, sin rastreo.":"Free to read · No sign-up, no advertising, no tracking.",
 "Libros para pensar":"Books to think with",
}

CAMBIO_IDIOMA = ('<a class="idioma" href="__OTRO__" hreflang="__OTROLANG__" '
                 'lang="__OTROLANG__">__OTROTXT__</a>')


QRJS = open(os.path.join(RAIZ,"src","qr.js"),encoding="utf-8").read()



def jsonld(es, baseurl):
    import json
    libro = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": "Fabricantes de sed" if es else "Thirst Makers",
        "author": {"@type": "Person", "name": "Dawin Salazar"},
        "inLanguage": "es" if es else "en",
        "bookFormat": "https://schema.org/EBook",
        "isAccessibleForFree": True,
        "genre": ["Ficción literaria", "Novela"] if es else ["Literary fiction", "Novel"],
        "numberOfPages": 130,
        "url": baseurl + ("/fabricantes-de-sed.html" if es else "/thirst-makers.html"),
        "image": baseurl + ("/og-es.png" if es else "/og-en.png"),
        "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "description": ("Un publicista recibe de vuelta sus propios cuadernos de juventud "
                        "y descubre que la única persuasión que nunca ha probado es la verdad."
                        if es else
                        "An advertising man gets his own youthful notebooks back and discovers "
                        "that the one form of persuasion he has never tried is the truth."),
        "publisher": {"@type": "Organization", "name": "Libros para pensar" if es else "Books to think with",
                      "url": baseurl},
        "potentialAction": {"@type": "ReadAction",
            "target": baseurl + ("/fabricantes-de-sed.html" if es else "/thirst-makers.html")},
    }
    return json.dumps(libro, ensure_ascii=False, indent=1)


CARTEL = r"""<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TCARTEL__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#e9e6e0;font-family:Georgia,"Times New Roman",serif;padding:1.5rem;
 display:flex;flex-direction:column;align-items:center;gap:1rem}
.barra{font-family:system-ui,sans-serif;font-size:.85rem;color:#555;text-align:center;
 max-width:21cm}
.barra button{font:inherit;padding:.6rem 1.2rem;margin:.4rem;border:1px solid #999;
 background:#fff;border-radius:.4rem;cursor:pointer}
.hoja{width:21cm;min-height:29.7cm;background:#15120d;color:#f2e9da;
 padding:2.4cm 2cm;display:flex;flex-direction:column;align-items:center;
 text-align:center;box-shadow:0 6px 30px rgba(0,0,0,.3)}
.hoja .marca{font-family:system-ui,sans-serif;font-size:10pt;letter-spacing:.32em;
 text-transform:uppercase;color:#a08b68}
.hoja h1{font-size:52pt;line-height:1.02;font-weight:400;margin:1.1cm 0 .3cm;
 letter-spacing:.01em}
.hoja .sub{font-size:14pt;font-style:italic;color:#c9975a;line-height:1.5}
.hoja .autor{font-size:12pt;letter-spacing:.22em;color:#a99b86;margin-top:.5cm}
.hoja .linea{width:5cm;height:1px;background:#c9975a;opacity:.7;margin:1cm 0}
.hoja .gancho{font-size:17pt;line-height:1.5;max-width:15cm;margin-bottom:1cm}
.hoja .qr{background:#fff;padding:.5cm;border-radius:4px}
.hoja .qr svg{display:block;width:6.5cm;height:6.5cm}
.hoja .url{font-family:system-ui,sans-serif;font-size:12pt;letter-spacing:.05em;
 margin-top:.6cm;color:#f2e9da}
.hoja .datos{font-family:system-ui,sans-serif;font-size:10.5pt;color:#a99b86;
 margin-top:.8cm;line-height:1.8}
.hoja .lic{font-family:system-ui,sans-serif;font-size:8.5pt;color:#7e7362;
 margin-top:auto;padding-top:1cm;letter-spacing:.08em}
@media print{
 body{background:#fff;padding:0;gap:0}
 .barra{display:none}
 .hoja{box-shadow:none;width:100%;min-height:100vh;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
 @page{size:A4;margin:0}
}
</style>
</head>
<body>
<div class="barra">
 <p>__AYUDACARTEL__</p>
 <button onclick="print()">__IMPRIMIR__</button>
 <button onclick="location.href='__HOME__'">__VOLVER__</button>
</div>

<div class="hoja">
 <div class="marca">__SITIO__</div>
 <h1>__TITULO__</h1>
 <p class="sub">__SUBT__</p>
 <p class="autor">DAWIN SALAZAR</p>
 <div class="linea"></div>
 <p class="gancho">__GANCHO__</p>
 <div class="qr" id="qr"></div>
 <p class="url">__URLCORTA__</p>
 <p class="datos">__DATOS__</p>
 <p class="lic">__LIC__</p>
</div>

<script>__QRJS__</script>
<script>
try{document.getElementById("qr").innerHTML=QR.svg("__BASEURL__",400,"#111111","#ffffff")}
catch(e){document.getElementById("qr").textContent="__BASEURL__"}
</script>
</body>
</html>
"""


def construir(lang):
    es = (lang == "es")
    partes = PARTS if es else ["EN_MANUSCRITO.md", "EN_MANUSCRITO_P2.md", "EN_MANUSCRITO_P3.md", "EN_MANUSCRITO_P4.md"]
    titulo, epi, secs = parse(partes)
    ui = UI_ES if es else UI_EN
    cuerpo, toc = [], []
    for s in secs:
        rot = " inter" if s["kind"] == "interludio" else ""
        cuerpo.append('<section id="%s" aria-labelledby="h-%s">'
            '<div class="rotulo%s">%s</div><h2 id="h-%s">%s</h2>\n%s</section>'
            % (s["id"], s["id"], rot, html.escape(s["num"]), s["id"],
               html.escape(s["titulo"] or ""), s["html"]))
        toc.append('<li><a href="#%s"><span class="n">%s</span>'
                   '<span class="t">%s</span></a></li>'
                   % (s["id"], html.escape(s["num"]), html.escape(s["titulo"] or "")))

    lector = READER
    for k, v in ui.items():
        lector = lector.replace("__" + k + "__", v)
    lector = (lector.replace("__QRJS__", QRJS).replace("__BASE__", BASECSS)
        .replace("__CUERPO__", "\n".join(cuerpo)).replace("__TOC__", "\n".join(toc))
        .replace("__BLOQUE_APORTE__", APORTE_ES if es else APORTE_EN)
        .replace("__TIT__", html.escape(titulo or ""))
        .replace("__SITIO__", SITIO if es else "Books to think with")
        .replace("__HOME__", "index.html" if es else "index-en.html")
        .replace("__LANGVOZ__", "es-ES" if es else "en-GB")
        .replace("__LANG__", "es" if es else "en")
        .replace("__NS__", "fds-es" if es else "fds-en")
        .replace("__OGDESC__", "El hombre que enseñó al mundo a desear recibe su propio cuaderno de juventud de vuelta." if es else "The man who taught the world to want gets his own youthful notebook back.")
        .replace("__OGIMG__", "og-es.png" if es else "og-en.png")
        .replace("__LOCALE__", "es_CO" if es else "en_GB")
        .replace("__ESTE__", "fabricantes-de-sed.html" if es else "thirst-makers.html")
        .replace("__BASEURL__", BASEURL))

    portada = INDEX
    if not es:
        for a, b in sorted(IDX_EN.items(), key=lambda x: -len(x[0])):
            portada = portada.replace(a, b)
        portada = portada.replace("__CUBIERTA__", CUBIERTA_EN)
        portada = portada.replace("__MINI__", CUBIERTA_EN.replace(
            'role="img"', 'role="presentation" aria-hidden="true"'))
        portada = portada.replace('href="fabricantes-de-sed.html"', 'href="thirst-makers.html"')
        otro = ('<a class="idioma" href="index.html" hreflang="es" lang="es">Español</a>')
    else:
        portada = portada.replace("__CUBIERTA__", CUBIERTA)
        portada = portada.replace("__MINI__", CUBIERTA.replace(
            'role="img"', 'role="presentation" aria-hidden="true"'))
        otro = ('<a class="idioma" href="index-en.html" hreflang="en" lang="en">English</a>')

    portada = (portada.replace("__JSONLD__", jsonld(es, BASEURL))
        .replace("__QRJS__", QRJS).replace("__LANG__", "es" if es else "en")
        .replace("__BASE__", BASECSS)
        .replace("__SITIO__", SITIO if es else "Books to think with")
        .replace("__BANCO__", BANCO).replace("__CUENTA__", CUENTA)
        .replace("__BLOQUE_APORTE__", (APORTE_ES if es else APORTE_EN)
                 .replace('style="text-indent:0"', 'style="max-width:36rem"'))
        .replace("__OGIMG__", "og-es.png" if es else "og-en.png")
        .replace("__LOCALE__", "es_CO" if es else "en_GB")
        .replace("__ESTE__", "index.html" if es else "index-en.html")
        .replace("__BASEURL__", BASEURL)
        .replace('<button id="bTema"', otro + '<button id="bTema"'))

    C = dict(
      TCARTEL="Cartel — Fabricantes de sed" if es else "Poster — Thirst Makers",
      AYUDACARTEL=("Imprima esta página en A4 y péguela donde quiera. Se ve igual en blanco y negro."
                   if es else
                   "Print this page on A4 and put it up anywhere. It works in black and white too."),
      IMPRIMIR="Imprimir" if es else "Print",
      VOLVER="Volver" if es else "Back",
      TITULO="Fabricantes de sed" if es else "Thirst Makers",
      SUBT=("Una novela sobre la persuasión,<br>la verdad y el precio de las palabras"
            if es else
            "A novel about persuasion, truth,<br>and the price of words"),
      GANCHO=("Un hombre que se ganó la vida convenciendo a otros empieza a recibir de vuelta sus propios cuadernos de juventud."
              if es else
              "A man who made his living convincing people starts getting his own old notebooks back."),
      URLCORTA=BASEURL.replace("https://",""),
      DATOS=("Novela completa · Gratis · Sin registro<br>Tres horas de lectura · Funciona sin señal"
             if es else
             "Complete novel · Free · No sign-up<br>Three hours of reading · Works with no signal"),
      LIC=("Libre para imprimir, repartir y usar en clase · CC BY-NC-ND 4.0"
           if es else
           "Free to print, hand out and use in class · CC BY-NC-ND 4.0"),
      SITIO=SITIO if es else "Books to think with",
      HOME="index.html" if es else "index-en.html",
      LANG="es" if es else "en",
      BASEURL=BASEURL, QRJS=QRJS)
    cartel = CARTEL
    for k, v in C.items():
        cartel = cartel.replace("__" + k + "__", v)
    open(os.path.join(OUT, "cartel.html" if es else "poster.html"), "w",
         encoding="utf-8").write(cartel)

    nom_lector = "fabricantes-de-sed.html" if es else "thirst-makers.html"
    nom_indice = "index.html" if es else "index-en.html"
    open(os.path.join(OUT, nom_lector), "w", encoding="utf-8").write(lector)
    open(os.path.join(OUT, nom_indice), "w", encoding="utf-8").write(portada)
    print(lang, "→", nom_lector, nom_indice, "| secciones:", len(secs))


def main():
    construir("es")
    construir("en")
    open(os.path.join(OUT, "cubierta.svg"), "w", encoding="utf-8").write(CUBIERTA)
    open(os.path.join(OUT, "cover-en.svg"), "w", encoding="utf-8").write(CUBIERTA_EN)


if __name__ == "__main__":
    main()
