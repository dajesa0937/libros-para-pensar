# -*- coding: utf-8 -*-
OG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<defs>
 <linearGradient id="f" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#241f18"/><stop offset="1" stop-color="#0d0b08"/></linearGradient>
 <radialGradient id="h" cx="0.28" cy="0.45" r="0.5">
  <stop offset="0" stop-color="#c9975a" stop-opacity="0.18"/>
  <stop offset="1" stop-color="#c9975a" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1200" height="630" fill="url(#f)"/>
<rect width="1200" height="630" fill="url(#h)"/>

<g transform="translate(120,150)">
 <rect x="6" y="10" width="240" height="360" fill="#000" opacity="0.45"/>
 <rect width="240" height="360" fill="#1b1710" stroke="#3a3227"/>
 <rect width="9" height="360" fill="#000" opacity="0.5"/>
 <g stroke="#c9975a" fill="none" stroke-linecap="round" transform="translate(120,92) scale(0.52)">
  <line x1="0" y1="-40" x2="0" y2="14" stroke-width="2.6"/>
  <g transform="rotate(-9)">
   <line x1="-96" y1="14" x2="96" y2="14" stroke-width="3.4"/>
   <line x1="-96" y1="14" x2="-96" y2="60" stroke-width="2"/>
   <line x1="96" y1="14" x2="96" y2="60" stroke-width="2"/>
   <path d="M-126 60 Q-96 96 -66 60" stroke-width="3"/>
   <path d="M66 60 Q96 90 126 60" stroke-width="3"/>
  </g>
  <circle cx="0" cy="-44" r="8" stroke-width="2.6"/>
 </g>
 <text x="120" y="212" fill="#f2e9da" font-family="Georgia,serif" font-size="30" text-anchor="middle" letter-spacing="0.5">__T1__</text>
 <text x="120" y="242" fill="#f2e9da" font-family="Georgia,serif" font-size="17" text-anchor="middle" opacity="0.72" letter-spacing="6">__T2__</text>
 <text x="120" y="284" fill="#f2e9da" font-family="Georgia,serif" font-size="34" text-anchor="middle" letter-spacing="2">__T3__</text>
 <line x1="72" y1="308" x2="168" y2="308" stroke="#c9975a" stroke-width="1" opacity="0.85"/>
 <text x="120" y="336" fill="#a99b86" font-family="Georgia,serif" font-size="13" text-anchor="middle" letter-spacing="1.6">DAWIN SALAZAR</text>
</g>

<g transform="translate(470,0)">
 <text x="0" y="238" fill="#f4ece0" font-family="Georgia,serif" font-size="62" letter-spacing="0.5">__TIT__</text>
 <text x="0" y="298" fill="#c9975a" font-family="Georgia,serif" font-size="25" font-style="italic">__SUB1__</text>
 <text x="0" y="332" fill="#c9975a" font-family="Georgia,serif" font-size="25" font-style="italic">__SUB2__</text>
 <line x1="0" y1="372" x2="150" y2="372" stroke="#4a4238" stroke-width="1.5"/>
 <text x="0" y="416" fill="#9d9284" font-family="Georgia,serif" font-size="21">__L1__</text>
 <text x="0" y="448" fill="#9d9284" font-family="Georgia,serif" font-size="21">__L2__</text>
</g>
</svg>'''

ES = (OG.replace("__T1__","FABRICANTES").replace("__T2__","DE").replace("__T3__","SED")
        .replace("__TIT__","Fabricantes de sed")
        .replace("__SUB1__","Una novela sobre la persuasión,")
        .replace("__SUB2__","la verdad y el precio de las palabras")
        .replace("__L1__","Libro completo, gratis.")
        .replace("__L2__","Sin registro y sin publicidad."))

EN = (OG.replace("__T1__","THE").replace("__T2__","THIRST").replace("__T3__","MAKERS")
        .replace("__TIT__","Thirst Makers")
        .replace("__SUB1__","A novel about persuasion, truth,")
        .replace("__SUB2__","and the price of words")
        .replace("__L1__","The complete book, free.")
        .replace("__L2__","No sign-up, no advertising."))

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="12" fill="#1b1710"/>
<g stroke="#c9975a" fill="none" stroke-linecap="round" stroke-width="3">
 <line x1="32" y1="16" x2="32" y2="30"/>
 <g transform="rotate(-10 32 30)">
  <line x1="12" y1="30" x2="52" y2="30"/>
  <path d="M6 38 Q12 48 18 38"/>
  <path d="M46 38 Q52 46 58 38"/>
  <line x1="12" y1="30" x2="12" y2="38" stroke-width="2"/>
  <line x1="52" y1="30" x2="52" y2="38" stroke-width="2"/>
 </g>
 <circle cx="32" cy="14" r="3"/>
</g></svg>'''
