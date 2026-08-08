// DOM mínimo: sólo lo que usa el lector. Suficiente para ejecutar el script real.
const fs=require('fs');
function crearEntorno(html){
 const idsAttr=[...html.matchAll(/<([a-z0-9]+)([^>]*\bid="([^"]+)"[^>]*)>/gi)];
 const nodos={};
 function Nodo(id,tag,attrs){
  this.id=id;this.tagName=(tag||"div").toUpperCase();this.textContent="";
  this.innerHTML="";this.style={_p:{},setProperty(k,v){this._p[k]=v},
   getPropertyValue(k){return this._p[k]||""}};
  this.dataset={};this._cls=new Set();this.children=[];this.attrs=attrs||{};
  this.classList={
   add:c=>this._cls.add(c), remove:c=>this._cls.delete(c),
   toggle:(c,f)=>{f?this._cls.add(c):this._cls.delete(c)},
   contains:c=>this._cls.has(c)};
  this.hidden=false;this.onclick=null;this.onchange=null;
  this.click=()=>{if(this.onclick)this.onclick.call(this,{preventDefault(){},stopPropagation(){}})};
  this.setAttribute=(k,v)=>{this.attrs[k]=v};
  this.getAttribute=k=>this.attrs[k]===undefined?null:this.attrs[k];
  this.addEventListener=()=>{};this.removeEventListener=()=>{};
  this.getBoundingClientRect=()=>({left:0,right:380,top:0,bottom:640,width:380,height:640});
  this.scrollIntoView=()=>{};
  this.appendChild=n=>{this.children.push(n);return n};
  this.querySelectorAll=()=>[];this.querySelector=()=>null;
  this.closest=()=>null;this.offsetHeight=640;this.offsetLeft=0;
  this.clientWidth=380;this.clientHeight=640;this.scrollWidth=53200;
  this.scrollTop=0;this.scrollHeight=64000;
 }
 for(const m of idsAttr){const id=m[3];nodos[id]=new Nodo(id,m[1],{})}
 // clases usadas por selector de atributo
 const porAttr={};
 for(const m of html.matchAll(/data-(fam|tema|lh|ls|modo|vel)="([^"]+)"/g)){
  const k="data-"+m[1];(porAttr[k]=porAttr[k]||[]).push(
   Object.assign(new Nodo("",  "button",{[k]:m[2]}),{dataset:{[m[1]]:m[2]}}))}
 const secciones=[...html.matchAll(/<section id="(s\d+)"/g)].map(m=>{
  const n=new Nodo(m[1],"section",{});n.querySelector=s=>{
   const q=new Nodo("","div",{});q.textContent=s===".rotulo"?"CAPÍTULO 1":"La palabra que faltaba";return q};
  return n});
 const almacen={};
 const doc={
  documentElement:Object.assign(new Nodo("html","html",{}),{dataset:{}}),
  getElementById:id=>nodos[id]||null,
  querySelector:s=>{
   if(s.startsWith("[")){const k=s.slice(1,s.indexOf("="));const v=s.match(/="([^"]+)"/)[1];
    return (porAttr[k]||[]).find(n=>n.getAttribute(k)===v)||null}
   if(s==='meta[name=theme-color]')return new Nodo("","meta",{});
   return null},
  querySelectorAll:s=>{
   if(s==="main section"||s==="p,h2,blockquote")return secciones;
   if(s.startsWith("[")){const k=s.slice(1,s.replace("]","=").indexOf("="));
    return porAttr[k]||[]}
   if(s==="#toc a")return [];
   return []},
  createElement:t=>new Nodo("",t,{}),
  body:new Nodo("body","body",{}),
  title:"libro", visibilityState:"visible",
  addEventListener:()=>{}
 };
 doc.body.appendChild=n=>n;
 const win={
  document:doc, innerWidth:380, innerHeight:640, scrollY:0,
  localStorage:{getItem:k=>k in almacen?almacen[k]:null,
   setItem:(k,v)=>{almacen[k]=String(v)}, removeItem:k=>{delete almacen[k]},
   get length(){return Object.keys(almacen).length}},
  addEventListener:()=>{}, setTimeout:(f,t)=>setTimeout(f,Math.min(t||0,5)),
  setInterval:()=>0, clearTimeout:clearTimeout, requestAnimationFrame:f=>setTimeout(f,0),
  speechSynthesis:{getVoices:()=>[{name:"Ana",lang:"es-ES",localService:true}],
   speak(){}, cancel(){}},
  navigator:{clipboard:{writeText:()=>Promise.resolve()}},
  location:{href:"https://ejemplo.com/libro.html"},
  alert:()=>{}, Blob:function(){}, URL:{createObjectURL:()=>"blob:", revokeObjectURL(){}},
  SpeechSynthesisUtterance:function(t){this.text=t},
  scrollTo:()=>{}, getComputedStyle:()=>({paddingLeft:"22px",paddingRight:"22px",
   paddingTop:"26px",paddingBottom:"16px",columnGap:"38px",getPropertyValue:()=>"1.075rem"}),
  Math, Date, JSON, parseFloat, parseInt, isNaN, Infinity, console, Error, String, Number, Array, Object
 };
 win.window=win; win.self=win; win.globalThis=win;
 return {win,doc,nodos,almacen,secciones};
}
module.exports={crearEntorno};
