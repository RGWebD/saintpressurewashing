(()=>{
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const $=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>[...c.querySelectorAll(s)];
document.documentElement.classList.remove('no-js');
// loader (home only, once per session)
const ld=$('.loader');
const go=()=>document.body.classList.add('ready');
if(ld){
  let seen=false;try{seen=sessionStorage.getItem('spw-intro')}catch(e){}
  if(RM||seen){ld.remove();go();}
  else{try{sessionStorage.setItem('spw-intro','1')}catch(e){}
    setTimeout(()=>{ld.classList.add('done');go();setTimeout(()=>ld.remove(),1100)},1500);}
}else go();
// nav
const nav=$('.nav'),prog=$('.prog'),mbar=$('.mbar');
const onS=()=>{const y=scrollY,h=document.documentElement.scrollHeight-innerHeight;
  nav&&nav.classList.toggle('solid',y>40);if(prog)prog.style.transform=`scaleX(${h>0?y/h:0})`;
  if(mbar)mbar.classList.toggle('show',y>innerHeight*.5);};
addEventListener('scroll',onS,{passive:true});onS();
const bg=$('.burger'),mm=$('.mmenu');
if(bg&&mm){const t=o=>{bg.setAttribute('aria-expanded',o);mm.classList.toggle('open',o);document.body.style.overflow=o?'hidden':''};
  bg.addEventListener('click',()=>t(bg.getAttribute('aria-expanded')!=='true'));
  $$('a',mm).forEach(a=>a.addEventListener('click',()=>t(false)));
  addEventListener('keydown',e=>{if(e.key==='Escape')t(false)});}
// pill
const pill=$('.pill');if(pill){try{if(sessionStorage.getItem('spw-pill'))pill.classList.add('gone')}catch(e){}
  $('button',pill).addEventListener('click',()=>{pill.classList.add('gone');try{sessionStorage.setItem('spw-pill','1')}catch(e){}});}
// reveals
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);
  if(e.target.dataset.count!==undefined)count(e.target);}}),{threshold:.18,rootMargin:'0px 0px -6% 0px'});
$$('.rv,.stalls,[data-count]').forEach(el=>io.observe(el));
function count(el){const to=+el.dataset.count;if(RM){el.textContent=to;return}
  const t0=performance.now(),d=1400;const f=t=>{const p=Math.min(1,(t-t0)/d),e=1-Math.pow(1-p,3);el.textContent=Math.round(to*e);if(p<1)requestAnimationFrame(f);else el.textContent=to};requestAnimationFrame(f);}
// timeline fill
const tl=$('.timeline');if(tl&&!RM){const fill=$('.fill',tl);const u=()=>{const r=tl.getBoundingClientRect();const p=Math.min(1,Math.max(0,(innerHeight*.85-r.top)/(r.height+innerHeight*.35)));fill.style.setProperty('--t',p.toFixed(3))};addEventListener('scroll',u,{passive:true});u();}
// before/after sweep
$$('.ba').forEach(ba=>{const r=$('input',ba);const set=v=>{ba.style.setProperty('--p',v+'%');r.value=v;r.setAttribute('aria-valuetext',`${Math.round(v)}% before shown`)};
  r.addEventListener('input',()=>set(+r.value));
  let demo=!RM;
  const stop=()=>demo=false;['pointerdown','keydown','touchstart'].forEach(ev=>ba.addEventListener(ev,stop,{passive:true}));
  if(demo){const o=new IntersectionObserver(es=>{if(es[0].isIntersecting){o.disconnect();const t0=performance.now();
    const f=t=>{if(!demo)return;const p=Math.min(1,(t-t0)/2600);const v=p<.5?50+40*Math.sin(p*2*Math.PI):50-40*Math.sin((p-.5)*2*Math.PI);set(v);if(p<1)requestAnimationFrame(f);else set(50)};requestAnimationFrame(f)}},{threshold:.5});o.observe(ba)}
});
// tilt cards
if(!RM&&matchMedia('(hover:hover)').matches)$$('.tilt').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`perspective(900px) rotateY(${x*7}deg) rotateX(${-y*7}deg) translateY(-4px)`});c.addEventListener('pointerleave',()=>c.style.transform='')});
// magnetic buttons
if(!RM&&matchMedia('(hover:hover)').matches)$$('.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.25}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
// parallax
const px=$$('[data-px]');if(px.length&&!RM){const u=()=>px.forEach(el=>{const r=el.getBoundingClientRect();const c=r.top+r.height/2-innerHeight/2;el.style.translate=`0 ${(-c*(+el.dataset.px)).toFixed(1)}px`});addEventListener('scroll',u,{passive:true});u();}
// open/closed badge (hours as listed, America/Chicago)
const H=window.SPW_HOURS;
if(H){const now=new Date(new Date().toLocaleString('en-US',{timeZone:'America/Chicago'}));const d=now.getDay(),m=now.getHours()*60+now.getMinutes();
  const keys=['su','mo','tu','we','th','fr','sa'];const fmt=x=>{let h=Math.floor(x/60),mi=x%60,ap=h>=12?'PM':'AM';h=h%12||12;return h+(mi?':'+String(mi).padStart(2,'0'):'')+' '+ap};
  const today=H[keys[d]];let txt,open=false;
  if(today&&m>=today[0]&&m<today[1]){open=true;txt=`Open now · until ${fmt(today[1])}`}
  else{let i=0,nd=d,nx=null;if(today&&m<today[0])nx=[0,today[0]];else{for(i=1;i<8;i++){const k=keys[(d+i)%7];if(H[k]){nx=[i,H[k][0]];nd=(d+i)%7;break}}}
    const dn=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];txt=nx?`Closed · opens ${nx[0]===0?'today':nx[0]===1?'tomorrow':dn[nd]} ${fmt(nx[1])}`:'Call for hours';}
  $$('[data-live]').forEach(el=>{el.classList.add(open?'open':'closed');$('.t',el).textContent=txt});
  const tr=$(`.hours tr[data-d="${keys[d]}"]`);if(tr)tr.classList.add('today');}
// gallery filters + lightbox
const gal=$('.gal');
if(gal){const btns=$$('.filters button');btns.forEach(b=>b.addEventListener('click',()=>{btns.forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;$$('button',gal).forEach(g=>g.classList.toggle('hide',f!=='all'&&!g.dataset.tags.includes(f)))}));
  const lb=$('.lbx'),im=$('img',lb),cap=$('p',lb);let items=[],i=0,last=null;
  const show=()=>{const g=items[i];im.src=g.dataset.full;im.alt=$('img',g).alt;cap.textContent=`${i+1} / ${items.length} — ${$('img',g).alt}`};
  const open=g=>{items=$$('button:not(.hide)',gal);i=items.indexOf(g);last=g;show();lb.classList.add('open');document.body.style.overflow='hidden';$('.x',lb).focus()};
  const close=()=>{lb.classList.remove('open');document.body.style.overflow='';im.removeAttribute('src');last&&last.focus()};
  $$('button',gal).forEach(g=>g.addEventListener('click',()=>open(g)));
  $('.x',lb).addEventListener('click',close);$('.pv',lb).addEventListener('click',()=>{i=(i-1+items.length)%items.length;show()});$('.nx',lb).addEventListener('click',()=>{i=(i+1)%items.length;show()});
  lb.addEventListener('click',e=>{if(e.target===lb)close()});
  addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowRight')$('.nx',lb).click();if(e.key==='ArrowLeft')$('.pv',lb).click();
    if(e.key==='Tab'){const f=$$('button',lb);const a=f.indexOf(document.activeElement);e.preventDefault();f[(a+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
  let sx=null;lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)$(dx<0?'.nx':'.pv',lb).click();sx=null});}
// quote builder -> mailto / sms
const qf=$('.qform');
if(qf){const build=()=>{const v=n=>(qf.elements[n]&&qf.elements[n].value||'').trim();
  return `Hi Saint Pressure Washing, I'd like a free quote.\n\nName: ${v('name')}\nPhone: ${v('phone')}\nProperty type: ${v('ptype')}\nService: ${v('service')}\nCity / area: ${v('city')}\nDetails: ${v('details')}`};
  qf.addEventListener('submit',e=>{e.preventDefault();location.href=`mailto:saintpressurewashing@gmail.com?subject=${encodeURIComponent('Free quote request — '+(qf.elements.service.value||'Pressure washing'))}&body=${encodeURIComponent(build())}`});
  $('.qsms',qf).addEventListener('click',e=>{e.preventDefault();location.href=`sms:+12819087222?&body=${encodeURIComponent(build())}`});}
})();
