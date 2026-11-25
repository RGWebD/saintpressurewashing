#!/usr/bin/env python3
"""Saint Pressure Washing LLC — demo site generator (RGWebD). Writes static site to ./docs"""
import json, os, shutil, html, datetime
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, 'docs')
BASE = 'https://rgwebd.github.io/saintpressurewashing/'
E = lambda s: html.escape(str(s), quote=True)
YEAR = datetime.date.today().year
D = dict(
  name='Saint Pressure Washing LLC', short='Saint Pressure Washing',
  phone='(281) 908-7222', tel='tel:+12819087222', sms='sms:+12819087222',
  email='saintpressurewashing@gmail.com',
  facebook='https://www.facebook.com/SaintPressureWashingLLC', instagram='https://www.instagram.com/saintpressurewashing/',
  oldsite='https://saintpressurewashing.com', nextdoor='https://nextdoor.com/pages/saint-pressure-washing-llc-cypress-tx/',
  city='Cypress', region='TX',
  slogan="You make the mess, we'll do the rest",
  intro='Commercial pressure washing servicing the greater Houston area. Call today for a free quote & consultation!',
  # hours as listed on directory/Google summary — flagged for confirmation
  hours={'mo':(450,1050),'tu':(450,1050),'we':(450,1050),'th':(450,1050),'fr':(450,1050),'sa':(510,1110),'su':(570,930)},
)
DAYS=[('mo','Monday'),('tu','Tuesday'),('we','Wednesday'),('th','Thursday'),('fr','Friday'),('sa','Saturday'),('su','Sunday')]
def fmt_t(m):
    h, mi = divmod(m, 60); ap = 'PM' if h >= 12 else 'AM'; h = h % 12 or 12
    return f'{h}:{mi:02d} {ap}'
REVIEWS=[
  dict(name='Jason Cruz', src='Facebook recommendation', when='', text='10/10 experience, Tony knows what he’s doing and he’s always on time. 100% recommend coming from a business owner.'),
  dict(name='Amanda Lipscomb', src='Facebook recommendation', when='', text='I could not recommend Saint Power Washing higher. The level of professionalism is super high. The owner, Tony, is an exceptional communicator and team leader. I was very impressed with their work. They kept the job sites clean and completed all jobs so well and in a very timely manner. I have and will keep hiring the team to come back.'),
  dict(name='C. S., Cypress', src='Nextdoor neighbor', when='', text='Saint Pressure Washing LLC in Cypress, 281-908-7222. Tony does a GREAT job and is a nice young man.'),
]
SERVICES=[
  dict(id='commercial-pressure-washing', short='Commercial Pressure Washing', blurb='High-flow washing for lots, garages, walks and storefronts.',
       body='Commercial pressure washing uses specialized high-flow equipment at the right pressure to remove dirt, algae stains and contaminants — keeping a property clean, safe and professional-looking.',
       pts=['Parking lots, drive lanes & walkways','Dirt, algae stains & contaminants lifted','High flow with the right pressure for the surface','Keeps the property safe and professional'],
       img='warehouse-midwash', alt='Warehouse floor mid-wash: a sharp line between grimy and freshly washed concrete', portrait=True, tag='Mid-wash · warehouse floor'),
  dict(id='parking-lot-striping', short='Parking Lot Striping', blurb='Crisp new lines, stalls and ADA spaces.',
       body='Parking lot striping applies clear, durable markings that improve traffic flow, maximize space and keep people safe. Proper striping boosts visibility, supports ADA compliance and keeps a property organized and professional.',
       pts=['Clear, durable stall & lane markings','ADA parking spaces and access aisles','Better traffic flow and more usable space','Restripes that sharpen a first impression'],
       img='ada-stripes', alt='Freshly painted ADA parking spaces with blue symbols and white hatched access aisle beside a new building', tag='ADA layout · fresh paint'),
  dict(id='construction-cleanup', short='Construction Cleanup', blurb='Post-build wash-down, ready for final layout.',
       body='Post-construction cleaning removes the dust, debris and residue left after building or renovation work, so the site is safe, spotless and ready for the final ADA-compliant parking layout.',
       pts=['Dust, debris & residue washed off','New concrete ready for handoff','Followed by the final ADA parking layout','Wash + striping from one crew'],
       img='f07', alt='Aerial view of a new-construction lot with fresh red fire lanes and white stalls between two buildings', tag='New construction · wash + layout'),
  dict(id='residential-surface-cleaning', short='Residential Surface Cleaning', blurb='Driveways, exteriors and soft washing for homes.',
       body='Residential pressure washing uses controlled high-pressure cleaning to remove dirt, mold and buildup from your home’s exterior — protecting surfaces and boosting curb appeal. For delicate surfaces, soft washing uses lower pressure with a cleaning agent.',
       pts=['Driveways, walks & flatwork','Soft washing for siding and exteriors','Dirt, mold and buildup removed','Protects surfaces, boosts curb appeal'],
       img='residential-drive', alt='Aerial view of a large two-story home with a long, freshly cleaned concrete driveway', tag='Residential · driveway'),
]
JOBLOG=[
  ('Fresh lines. Clean finish. A proper restripe can completely transform a property’s first impression.','Harris County courthouse annex · Houston'),
  ('Quick turn around on this County facility for our friends @hcsotexas','County facility · Baytown'),
  ('Texans season is around the corner and our customers use this lot for game day parking!!','NRG Stadium area · Houston'),
  ('3 day turn around on a full new construction wash and striping layout done for our customers','New construction · Tomball'),
]
GALLERY=[  # (img, tags, alt)
  ('hero-lot-m','lots','Aerial view of a large, freshly striped commercial parking lot with new tree islands'),
  ('f04','night striping','Night shot of yellow-hatched ADA spaces and blue symbols under the lot lights'),
  ('f17','striping','Close aerial of two blue ADA spaces, white stalls and a red fire lane'),
  ('f01','night lots','Large commercial lot under the lights at night, freshly striped in yellow'),
  ('f09','washing','A wet wash path cutting across a lot beside a new building'),
  ('f18','striping','Hatched access aisles and three ADA spaces along a red fire lane'),
  ('f05','night striping','Fenced lot at night with fresh yellow angled stalls and arrows'),
  ('f03','washing lots','Fenced county facility lot from above'),
  ('f08','striping','ADA space and fresh white stalls by a new stone-and-steel building'),
  ('f10','lots','Fire lane and lot behind a metal building beside the tracks'),
  ('f02','lots','Overhead of a big retail lot with planted islands'),
  ('f19','striping','Long drive lane with red fire-lane lines and stalls along a warehouse'),
  ('residential-drive','washing','Aerial of a home with a long, clean concrete driveway'),
  ('ada-stripes','striping','Fresh ADA layout with blue symbols and white access aisle'),
]
PAGES=[('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('about.html','About & FAQ'),('contact.html','Free Quote')]
_dims={}
def dims(name):
    if name not in _dims:
        p=os.path.join(ROOT,'img',name+'.webp'); _dims[name]=Image.open(p).size
    return _dims[name]
def img(name, alt, cls='', lazy=True, sizes=None, extra=''):
    w,h=dims(name)
    return f'<img src="img/{name}.webp" width="{w}" height="{h}" alt="{E(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}{f" class=\"{cls}\"" if cls else ""}{extra}>'
I_PHONE='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
I_SMS='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
I_MAIL='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
I_ARROWS='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6-6 6 6 6M15 6l6 6-6 6"/></svg>'
I_ADA='<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><circle cx="11" cy="4" r="2"/><path d="M10 7h2v5h5v2h-6.9zM9.2 9.6 9 12a5 5 0 1 0 6.5 5.6l1.8 0A7 7 0 1 1 9.2 9.6z"/><path d="M16 14h2l2 5-1.8.7z"/></svg>'
LOCALBIZ_ID=BASE+'#business'
def biz_schema():
    oh=[]
    grp={}
    for k,full in DAYS:
        v=D['hours'][k]; grp.setdefault(v,[]).append(full)
    for (o,c),days in grp.items():
        oh.append({'@type':'OpeningHoursSpecification','dayOfWeek':days,'opens':f'{o//60:02d}:{o%60:02d}','closes':f'{c//60:02d}:{c%60:02d}'})
    return {'@context':'https://schema.org','@type':'HomeAndConstructionBusiness','@id':LOCALBIZ_ID,'name':D['name'],'description':D['intro'],
      'url':BASE,'telephone':'+1-281-908-7222','email':D['email'],'slogan':D['slogan'],'image':BASE+'og.jpg','logo':BASE+'brand/logo-badge-1200.png',
      'address':{'@type':'PostalAddress','addressLocality':'Cypress','addressRegion':'TX','addressCountry':'US'},
      'areaServed':[{'@type':'City','name':n} for n in ['Houston','Cypress','Baytown','Tomball']]+[{'@type':'AdministrativeArea','name':'Greater Houston'}],
      'openingHoursSpecification':oh,'sameAs':[D['facebook'],D['instagram'],D['oldsite'],D['nextdoor']],
      'hasOfferCatalog':{'@type':'OfferCatalog','name':'Services','itemListElement':[{'@type':'Offer','itemOffered':{'@type':'Service','name':s['short'],'description':s['body']}} for s in SERVICES]},
      'review':[{'@type':'Review','author':{'@type':'Person','name':r['name']},'reviewBody':r['text'],'publisher':{'@type':'Organization','name':r['src'].split()[0]}} for r in REVIEWS]}
def crumbs_schema(path,title):
    items=[{'@type':'ListItem','position':1,'name':'Home','item':BASE}]
    if path!='index.html': items.append({'@type':'ListItem','position':2,'name':title,'item':BASE+path})
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':items}
def head(path,title,desc,schemas,home=False):
    canon=BASE+('' if path=='index.html' else path)
    ld=''.join(f'<script type="application/ld+json">{json.dumps(s,ensure_ascii=False)}</script>' for s in schemas)
    pre='<link rel="preload" as="image" href="img/hero-lot.webp" media="(min-width:601px)"><link rel="preload" as="image" href="img/hero-lot-m.webp" media="(max-width:600px)">' if home else ''
    return f'''<!doctype html><html lang="en" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}"><meta name="theme-color" content="#06090f">
<meta property="og:type" content="website"><meta property="og:site_name" content="{E(D['name'])}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE}og.jpg">
<link rel="icon" href="brand/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="brand/favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="brand/favicon-192.png"><link rel="apple-touch-icon" href="brand/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,700..900&family=Barlow:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
{pre}<link rel="stylesheet" href="assets/site.css?v=1">{ld}
</head><body>
<a class="skip" href="#main">Skip to content</a><div class="prog" aria-hidden="true"></div>
'''
def nav(path):
    li=''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==path else ""}>{t}</a></li>' for h,t in PAGES)
    ml=''.join(f'<a class="ml" href="{h}">{t}</a>' for h,t in PAGES)
    return f'''<header class="nav" role="banner">
<a class="brand" href="index.html" aria-label="{E(D['name'])} — home"><img src="brand/logo-badge-240.webp" width="240" height="215" alt="{E(D['name'])} logo"><span>Saint<small>Pressure Washing</small></span></a>
<nav aria-label="Main"><ul>{li}</ul></nav>
<a class="btn ghost cta-n" href="{D['sms']}">{I_SMS}Text</a><a class="btn cta-n mag" href="{D['tel']}">{I_PHONE}{D['phone']}</a>
<button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mmenu"><i></i><i></i><i></i></button>
</header>
<div class="mmenu" id="mmenu">{ml}<div class="row"><a class="btn" href="{D['tel']}">{I_PHONE}Call {D['phone']}</a><a class="btn ghost" href="{D['sms']}">{I_SMS}Text us</a></div></div>
<main id="main">'''
def footer():
    links=''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in PAGES)
    hrs=''.join(f'<li>{full[:3]} · {fmt_t(D["hours"][k][0])}–{fmt_t(D["hours"][k][1])}</li>' for k,full in DAYS)
    return f'''</main>
<footer><div class="wrap"><div class="fgrid">
<div><img class="flogo" src="brand/logo-badge-520.webp" width="520" height="466" alt="{E(D['name'])} logo" loading="lazy"><p>Commercial pressure washing, parking-lot striping and construction cleanup — plus residential surface cleaning — across Greater Houston. Based in Cypress, TX.</p><p class="y" style="font-family:var(--fm);font-size:13px;letter-spacing:.08em;text-transform:uppercase">“{E(D['slogan'])}”</p></div>
<div><h4>Pages</h4><ul>{links}<li><a href="services.html#process">How quotes work</a></li></ul></div>
<div><h4>Reach us</h4><ul><li><a href="{D['tel']}">{D['phone']}</a> · call or text</li><li><a href="mailto:{D['email']}">{D['email']}</a></li><li>Cypress, TX · serving Greater Houston</li><li><a href="{D['facebook']}" target="_blank" rel="noopener">Facebook</a> · <a href="{D['instagram']}" target="_blank" rel="noopener">Instagram</a></li></ul></div>
<div><h4>Hours (as listed)</h4><ul>{hrs}</ul></div>
</div><div class="fbase"><span>© {YEAR} {E(D['name'])} · Cypress, TX</span><span>Design preview by <a href="https://github.com/RGWebD" target="_blank" rel="noopener">RGWebD</a></span></div></div></footer>
<div class="mbar" role="region" aria-label="Quick contact"><a class="btn" href="{D['tel']}">{I_PHONE}Call</a><a class="btn water" href="{D['sms']}">{I_SMS}Text a photo</a></div>
<div class="pill" role="note">Design preview by <a href="https://github.com/RGWebD" target="_blank" rel="noopener">RGWebD</a><button type="button" aria-label="Dismiss preview note">×</button></div>
<script>window.SPW_HOURS={json.dumps(D['hours'])};</script>
<script src="assets/site.js?v=1" defer></script>
</body></html>
'''
def chip_live(): return '<span class="chip" data-live><span class="dot"></span><span class="t">Hours as listed</span></span>'
def phero(path,title,crumb,h1,lede,image,alt,tag,outline,extra=''):
    return f'''<section class="phero"><div class="outline" aria-hidden="true">{outline}</div><div class="wrap grid">
<div class="rv"><div class="crumbs"><a href="index.html">Home</a> / {crumb}</div><h1>{h1}</h1><p class="lede">{lede}</p>
<div class="ctas"><a class="btn mag" href="{D['tel']}">{I_PHONE}Call {D['phone']}</a><a class="btn ghost" href="{D['sms']}">{I_SMS}Text a photo</a></div>{extra}</div>
<div class="frame rv d2">{img(image,alt,lazy=False)}<span class="tag">{tag}</span></div>
</div></section>'''
def cta_band(h='Get a free quote & consultation',p='Call or text a photo of the job — lots, garages, walks, new construction or your driveway. Saint will size it up and give you a clear, upfront estimate.'):
    return f'''<section class="sec tight"><div class="wrap"><div class="cta rv"><div class="drops" aria-hidden="true"></div>
<div><h2>{h}</h2><p>{p}</p></div>
<div class="ctas"><a class="btn mag" href="{D['tel']}">{I_PHONE}Call {D['phone']}</a><a class="btn ghost" href="{D['sms']}">{I_SMS}Text a photo</a><a class="btn ghost" href="mailto:{D['email']}?subject=Free%20quote%20request">{I_MAIL}Email</a></div>
</div></div></section>'''
def quotes():
    q=''.join(f'''<figure class="quote rv d{i}"><div class="st">{E(r["src"])}</div><blockquote>{E(r['text'])}</blockquote><figcaption>— {E(r['name'])}</figcaption></figure>''' for i,r in enumerate(REVIEWS))
    return f'<div class="quotes">{q}</div>'
def sweep(name,before_alt,after_alt,label='Drag to wash'):
    w,h=dims(name+'-before')
    return f'''<div class="ba" style="--p:50%">
<img src="img/{name}-before.webp" width="{w}" height="{h}" alt="{E(before_alt)}" loading="lazy">
<img class="after" src="img/{name}-after.webp" width="{w}" height="{h}" alt="{E(after_alt)}" loading="lazy">
<div class="spray" aria-hidden="true"></div><div class="bar" aria-hidden="true"></div><span class="knob" aria-hidden="true">{I_ARROWS}</span>
<span class="lab l">Before</span><span class="lab r">After</span>
<input type="range" min="0" max="100" value="50" step="1" aria-label="{E(label)}: slide to compare before and after">
</div>'''
# ---------------- pages
def page_home():
    p='index.html'; title='Saint Pressure Washing LLC | Commercial Pressure Washing & Striping, Houston TX'
    desc='Commercial pressure washing, parking lot striping, ADA layout and construction cleanup across Greater Houston — plus residential surface cleaning. Based in Cypress. Free quotes: (281) 908-7222.'
    out=head(p,title,desc,[biz_schema(),crumbs_schema(p,'Home')],home=True)+nav(p)
    tape=''.join(f'<span>{t}</span>' for t in ['Commercial pressure washing','Parking lot striping','ADA parking layout','Construction cleanup','Soft washing','Free quote & consultation'])
    stalls=''
    for i,s in enumerate(SERVICES):
        ada=i==1
        stalls+=f'''<a class="stall{' ada' if ada else ''}" href="services.html#{s['id']}"><svg class="lines" aria-hidden="true" preserveAspectRatio="none"><line x1="0" y1="0" x2="0" y2="100%" pathLength="1"/>{'<line x1="100%" y1="0" x2="100%" y2="100%" pathLength="1"/>' if i==3 else ''}</svg>
{'<span class="sym">'+I_ADA+'</span>' if ada else ''}<span class="no">0{i+1}</span><h3>{s['short']}</h3><p>{s['blurb']}</p><span class="go">Details</span></a>'''
    out+=f'''
<div class="loader" aria-hidden="true"><svg viewBox="0 0 420 150"><line class="y" x1="10" y1="10" x2="10" y2="110" pathLength="1" style="animation-delay:0s"/><line x1="110" y1="10" x2="110" y2="110" pathLength="1" style="animation-delay:.12s"/><line x1="210" y1="10" x2="210" y2="110" pathLength="1" style="animation-delay:.24s"/><line x1="310" y1="10" x2="310" y2="110" pathLength="1" style="animation-delay:.36s"/><line class="y" x1="410" y1="10" x2="410" y2="110" pathLength="1" style="animation-delay:.48s"/><line class="y" x1="10" y1="110" x2="410" y2="110" pathLength="1" style="animation-delay:.6s"/><text x="210" y="146" text-anchor="middle">SAINT</text></svg></div>
<section class="hero" aria-label="Intro">
<div class="bg" aria-hidden="true"><picture><source media="(max-width:600px)" srcset="img/hero-lot-m.webp"><img src="img/hero-lot.webp" width="1960" height="1440" alt="" fetchpriority="high"></picture>
<div class="grime"></div><div class="washline"></div></div>
<div class="shade"></div><div class="bigtype" aria-hidden="true">CLEAN</div>
<div class="wrap in">
<span class="eyebrow">Commercial pressure washing · Greater Houston</span>
<h1 aria-label="You make the mess. We'll do the rest."><span class="jet" aria-hidden="true">You make</span><span class="jet" aria-hidden="true">the mess.</span><span class="jet y" aria-hidden="true">We’ll do</span><span class="jet y" aria-hidden="true">the rest.</span></h1>
<p class="lede">Pressure washing, parking-lot striping and construction cleanup for commercial properties across Greater Houston — plus residential surface cleaning and soft washing. Call today for a free quote &amp; consultation.</p>
<div class="ctas"><a class="btn mag" href="{D['tel']}">{I_PHONE}Call {D['phone']}</a><a class="btn ghost" href="{D['sms']}">{I_SMS}Text a photo of the job</a></div>
<div class="chips"><span class="chip">Free quote &amp; consultation</span><span class="chip">Based in Cypress · serving Greater Houston</span>{chip_live()}</div>
</div><div class="scrollcue" aria-hidden="true"></div></section>
<div class="tapewrap"><div class="tape" aria-hidden="true"><div class="track"><div class="run">{tape}</div><div class="run">{tape}</div></div></div></div>

<section class="sec"><div class="wrap sweep">
<div class="rv">{sweep('sweep-lot','Before: faded stalls and grimy concrete on a fenced lot','After: the same lot washed, with crisp new white stalls, ADA spaces and a hatched aisle')}</div>
<div class="rv d2"><span class="eyebrow">The clean sweep</span><h2>Same lot. <span class="b">New</span> first impression.</h2>
<p>Drag the nozzle across. On the left, faded paint and years of grime. On the right, the same lot washed down and restriped — fresh stalls, ADA spaces and a hatched access aisle.</p>
<div class="ticket"><strong style="font-family:var(--fd);font-stretch:112%;text-transform:uppercase">Job ticket</strong><dl><dt>Scope</dt><dd>Wash + restripe</dd><dt>Layout</dt><dd>Stalls, ADA spaces, access aisle</dd><dt>Source</dt><dd>Saint’s own before &amp; after photos</dd></dl></div>
</div></div></section>

<section class="sec alt"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">What Saint does</span><h2>Four services. One crew.</h2></div><p class="rv d1">From a full wash-down to the last ADA symbol, commercial properties get the wash and the paint from the same team.</p></div>
<div class="stalls">{stalls}</div><div class="stallbar" aria-hidden="true"></div></div></section>

<section class="sec"><div class="wrap"><div class="nums">
<div class="num rv"><b><span data-count="3">3</span><small>days</small></b><p>Turnaround on a full new-construction wash <em>and</em> striping layout in Tomball, per Saint’s own job post.</p></div>
<div class="num rv d1"><b><span data-count="4">4</span><small>services</small></b><p>Commercial washing, parking-lot striping, construction cleanup and residential surface cleaning.</p></div>
<div class="num rv d2"><b>Free</b><p>Quote &amp; consultation on every job. Pricing is based on the area, surface, buildup and what it takes to do it right.</p></div>
</div></div></section>

<section class="sec alt"><div class="wrap night">
<div class="rv"><span class="eyebrow">Under the lights</span><h2>Plenty of lots get done <span class="y">after dark.</span></h2><p>A lot of Saint’s work happens under the parking-lot lights — retail lots, county facilities, game-day parking and brand-new construction, with the rig parked right on site.</p>
<a class="btn water" href="work.html">See the work</a></div>
<div class="collage">
<figure class="c2 rv" data-px=".05">{img('f05','Fenced lot at night with fresh yellow angled stalls')}<figcaption>Fresh angled stalls</figcaption></figure>
<figure class="c1 rv d1" data-px="-.04">{img('rig-night','Saint’s flatbed rig with water tanks and equipment, parked on concrete at night')}<figcaption>The rig</figcaption></figure>
<figure class="c3 rv d2" data-px=".03">{img('f01','A large commercial lot under the lights at night, newly striped in yellow')}<figcaption>Retail lot · night</figcaption></figure>
</div></div></section>

<section class="sec"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">In their words</span><h2>“Tony knows what he’s doing.”</h2></div><p class="rv d1">Word for word from Saint’s Facebook recommendations and a Cypress neighbor on Nextdoor.</p></div>{quotes()}</div></section>

<section class="sec tight alt"><div class="wrap"><div class="teasers">
<a class="tcard tilt rv" href="services.html"><div class="ph">{img('ada-stripes','Fresh ADA parking layout')}</div><div class="tx"><span class="k">Services</span><h3>Wash. Stripe. Done.</h3><p>Every service, how quotes work, and what soft washing is.</p></div></a>
<a class="tcard tilt rv d1" href="work.html"><div class="ph">{img('f17','ADA spaces and fire lane from above')}</div><div class="tx"><span class="k">Our work</span><h3>The job log</h3><p>Another before &amp; after, plus lots from Houston to Baytown and Tomball.</p></div></a>
<a class="tcard tilt rv d2" href="about.html"><div class="ph">{img('f16','Aerial view of a new warehouse lot with fresh striping')}</div><div class="tx"><span class="k">About &amp; FAQ</span><h3>Who shows up</h3><p>Based in Cypress, on time, and they leave the site clean.</p></div></a>
</div></div></section>
{cta_band()}'''
    return out+footer()

def page_services():
    p='services.html'; title='Services | Pressure Washing, Striping & Cleanup — Saint Pressure Washing, Houston'
    desc='Commercial pressure washing, parking lot striping & ADA layout, post-construction cleanup and residential surface cleaning / soft washing in Greater Houston. Free quotes.'
    out=head(p,title,desc,[biz_schema(),crumbs_schema(p,'Services')])+nav(p)
    out+=phero(p,title,'Services','What Saint <span class="y">does.</span>','Four services built around commercial properties — and homeowners who want the same results on their driveway.','f16','Aerial of a new warehouse with a freshly washed and striped lot','Warehouse lot · aerial','SERVICES')
    for i,s in enumerate(SERVICES):
        pts=''.join(f'<li>{E(x)}</li>' for x in s['pts'])
        out+=f'''<section class="wrap svc" id="{s['id']}">
<div class="frame{' portrait' if s.get('portrait') else ''} rv">{img(s['img'],s['alt'])}<span class="tag">{s['tag']}</span></div>
<div class="rv d1"><span class="no">0{i+1} / 04</span><h2>{s['short']}</h2><p class="lede">{E(s['body'])}</p><ul>{pts}</ul>
<div class="ctas"><a class="btn mag" href="{D['tel']}">{I_PHONE}Quote this job</a><a class="btn ghost" href="contact.html">Send details</a></div></div></section>'''
    out+=f'''<section class="sec alt" id="process"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">How quotes work</span><h2>Clear, upfront pricing.</h2></div><p class="rv d1">No price sheet guessing. Saint looks at the actual job and gives you a fair, transparent estimate.</p></div>
<div class="timeline"><div class="fill" aria-hidden="true"></div>
<div class="step rv"><h3>Call or text</h3><p>Reach Saint at {D['phone']} — a photo of the area helps.</p></div>
<div class="step rv d1"><h3>Size it up</h3><p>Area size, surface type and condition, level of buildup and any special requirements.</p></div>
<div class="step rv d2"><h3>Clear estimate</h3><p>Equipment, materials and time are factored in, then you get a clear, upfront number.</p></div>
<div class="step rv d3"><h3>The work</h3><p>Washed, striped or both — done safely and on schedule.</p></div>
</div></div></section>
<section class="sec tight"><div class="wrap two"><div class="rv"><span class="eyebrow">Good to know</span><h2>What is soft washing?</h2></div>
<div class="note rv d1"><p>Soft-washing is the process of lower pressure water combined with a chemical agent that washes away unwanted growth or debris that has built up over time. It is proven to be the safest and most efficient way to clean the exterior of your home or property.</p><p class="flag" style="margin:0">— from Saint’s FAQ</p></div></div></section>
{cta_band('Need a lot washed or restriped?')}'''
    return out+footer()

def page_work():
    p='work.html'; title='Our Work | Before & After, Striping & Washing — Saint Pressure Washing'
    desc='Before-and-after photos and recent jobs from Saint Pressure Washing: parking lot washing and restriping, ADA layouts and new-construction cleanup across Houston, Baytown and Tomball.'
    out=head(p,title,desc,[biz_schema(),crumbs_schema(p,'Our Work')])+nav(p)
    out+=phero(p,title,'Our Work','The <span class="b">job</span> log.','Real lots, real paint — all photos are Saint’s own, from their Facebook page and website.','f06','Aerial of three metal warehouse buildings and their lots','Commercial park · aerial','THE WORK')
    logs=''.join(f'<div class="logc rv d{i%2}"><q>{E(t)}</q><span class="loc">{E(l)}</span></div>' for i,(t,l) in enumerate(JOBLOG))
    out+=f'''<section class="sec"><div class="wrap sweep rev">
<div class="rv d1"><span class="eyebrow">Clean sweep #2</span><h2>Bare lot → <span class="y">laid out.</span></h2><p>The same property from the air — before, with a worn lot and no layout; after, washed with fresh stalls, an ADA space, hatched aisle and a crisp red curb.</p></div>
<div class="rv">{sweep('sweep-annex','Before: a worn, unmarked lot around a white building','After: the same lot washed with new stalls, ADA spaces and red curb paint','Drag to restripe')}</div>
</div></section>
<section class="sec tight alt"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">From the job posts</span><h2>Straight from the crew.</h2></div><p class="rv d1">Captions from Saint’s own Facebook posts, with the place each job was tagged.</p></div><div class="log">{logs}</div></div></section>'''
    gb=''
    for name,tags,alt in GALLERY:
        gb+=f'<button type="button" data-tags="{tags}" data-full="img/{name}.webp" aria-label="Open photo: {E(alt)}">{img(name,alt)}<span>{"Night" if "night" in tags else tags.split()[0].title()}</span></button>'
    out+=f'''<section class="sec"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">Gallery</span><h2>Lots, lines &amp; wash-downs.</h2></div></div>
<div class="filters" role="group" aria-label="Filter photos"><button type="button" data-f="all" aria-pressed="true">All</button><button type="button" data-f="striping" aria-pressed="false">Striping</button><button type="button" data-f="washing" aria-pressed="false">Washing</button><button type="button" data-f="lots" aria-pressed="false">Big lots</button><button type="button" data-f="night" aria-pressed="false">Night jobs</button></div>
<div class="gal">{gb}</div>
<h3 style="margin-top:60px">Jobs tagged in</h3><ul class="areas"><li>Houston</li><li>Baytown</li><li>Tomball</li><li>Cypress</li><li>NRG Stadium area</li><li>Harris County facilities</li></ul></div></section>
<div class="lbx" role="dialog" aria-modal="true" aria-label="Photo viewer"><button class="x" type="button" aria-label="Close">×</button><button class="pv" type="button" aria-label="Previous photo">‹</button><img alt=""><button class="nx" type="button" aria-label="Next photo">›</button><p></p></div>
{cta_band('Want your lot in the next post?')}'''
    return out+footer()

FAQ=[
 ('How do you price your services?','Pricing depends on the size of the area, the type and condition of the surface, the level of buildup, and any special cleaning requirements. Saint also considers the equipment, materials and time needed to do the job safely and effectively, then gives a clear, upfront estimate — fair and transparent for every customer.'),
 ('What is soft washing?','Soft-washing is lower-pressure water combined with a chemical agent that washes away unwanted growth or debris built up over time. It is the safest and most efficient way to clean the exterior of a home or property.'),
 ('Why hire a professional instead of doing it myself?','The surfaces, cleaning products and pressure all affect how clean your surfaces get and how long they stay clean. Saint has the chemicals, equipment and experience to clean even the most difficult surfaces.'),
 ('Do you work on commercial properties?','Yes — commercial pressure washing is Saint’s main focus, along with parking lot striping, ADA parking layout and post-construction cleanup.'),
 ('Do you clean homes too?','Yes. Residential surface cleaning and soft washing cover driveways, walks and home exteriors.'),
 ('What areas do you serve?','Saint is based in Cypress and serves the greater Houston area. Recent jobs have been tagged in Houston, Baytown and Tomball.'),
 ('How do I get a quote?',f'Call or text {D["phone"]} or email {D["email"]}. Quotes and consultations are free.'),
]
def page_about():
    p='about.html'; title='About & FAQ | Saint Pressure Washing LLC — Cypress / Greater Houston'
    desc='Saint Pressure Washing LLC is based in Cypress, TX and serves Greater Houston with commercial pressure washing, striping and cleanup. Reviews and answers to common questions.'
    faq_schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}
    out=head(p,title,desc,[biz_schema(),crumbs_schema(p,'About & FAQ'),faq_schema])+nav(p)
    out+=phero(p,title,'About &amp; FAQ','Who <span class="y">shows up.</span>','Saint Pressure Washing LLC is based out of Cypress and services the suburbs all around Houston — commercial lots first, homes too.','rig-night','Saint’s flatbed rig with tanks and equipment, parked at night','The rig','ABOUT')
    vals=[('On time','“He’s always on time.”','Jason Cruz'),('Professional','“The level of professionalism is super high.”','Amanda Lipscomb'),('Clean job sites','“They kept the job sites clean.”','Amanda Lipscomb'),('Communicates','“An exceptional communicator and team leader.”','Amanda Lipscomb')]
    v=''.join(f'<div class="val rv d{i%3}"><b>{a}</b><p>{E(b)}</p><i>— {c}</i></div>' for i,(a,b,c) in enumerate(vals))
    fq=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in FAQ)
    out+=f'''<section class="sec"><div class="wrap two">
<div class="rv"><span class="eyebrow">The short version</span><h2>Commercial-first. <span class="b">Houston-wide.</span></h2></div>
<div class="rv d1"><p class="lede">Saint Pressure Washing LLC handles commercial pressure washing, parking lot striping and post-construction cleanup across the greater Houston area — and brings the same equipment to homeowners for driveways, exteriors and soft washing.</p>
<p>Their motto says it plainly: <strong class="y">“{E(D['slogan'])}.”</strong> Jobs have taken the crew to county facilities, retail centers, new construction in Tomball and lots used for Texans game-day parking.</p></div>
</div></section>
<section class="sec tight alt"><div class="wrap"><div class="head"><div class="rv"><span class="eyebrow">What customers notice</span><h2>Straight from reviews.</h2></div></div><div class="vals">{v}</div></div></section>
<section class="sec"><div class="wrap">{quotes()}</div></section>
<section class="sec alt" id="faq"><div class="wrap two"><div class="rv"><span class="eyebrow">FAQ</span><h2>Questions, answered.</h2><div class="frame" style="margin-top:30px">{img('f04','Night shot of yellow-hatched ADA spaces under the lot lights')}<span class="tag">ADA layout · night</span></div></div>
<div class="faq rv d1">{fq}</div></div></section>
{cta_band()}'''
    return out+footer()

def page_contact():
    p='contact.html'; title='Free Quote | Call or Text (281) 908-7222 — Saint Pressure Washing, Houston'
    desc='Get a free quote and consultation from Saint Pressure Washing LLC. Call or text (281) 908-7222 or email saintpressurewashing@gmail.com. Serving Greater Houston from Cypress, TX.'
    out=head(p,title,desc,[biz_schema(),crumbs_schema(p,'Free Quote')])+nav(p)
    out+=phero(p,title,'Free Quote','Free quote. <span class="y">Fast.</span>','Call, text a photo of the job, or send the details below. Quotes and consultations are free.','f19','Long drive lane with fresh fire-lane lines alongside a warehouse','Drive lane · fire lane','QUOTE',extra=f'<div class="chips">{chip_live()}</div>')
    opts=''.join(f'<option>{s["short"]}</option>' for s in SERVICES)
    hrs=''.join(f'<tr data-d="{k}"><td>{full}</td><td>{fmt_t(D["hours"][k][0])} – {fmt_t(D["hours"][k][1])}</td></tr>' for k,full in DAYS)
    out+=f'''<section class="sec"><div class="wrap">
<div class="ways"><a class="way rv" href="{D['tel']}"><small>Call</small><b>{D['phone']}</b><span>Talk it through and book a free consultation.</span></a>
<a class="way rv d1" href="{D['sms']}"><small>Text</small><b>Text a photo</b><span>Snap the lot, driveway or site and send it to {D['phone']}.</span></a>
<a class="way rv d2" href="mailto:{D['email']}?subject=Free%20quote%20request"><small>Email</small><b class="sm">{D['email']}</b><span>Plans, site maps or a long list? Email works.</span></a></div>
</div></section>
<section class="sec tight alt"><div class="wrap two">
<form class="qform rv" novalidate><h3>Quote builder</h3>
<label>Name<input name="name" autocomplete="name"></label><label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
<label>Property type<select name="ptype"><option>Commercial lot / building</option><option>New construction</option><option>HOA / multi-unit</option><option>Home</option><option>Other</option></select></label>
<label>Service<select name="service">{opts}</select></label>
<label class="full">City / area<input name="city" placeholder="e.g. Cypress, Tomball, Baytown"></label>
<label class="full">Details<textarea name="details" rows="4" placeholder="Approx. size, surface, number of stalls, timing…"></textarea></label>
<div class="ctas"><button class="btn" type="submit">{I_MAIL}Email this to Saint</button><button class="btn ghost qsms" type="button">{I_SMS}Text it instead</button></div>
<small>This opens your own email or messages app with everything filled in — nothing is sent until you hit send.</small></form>
<div class="rv d1"><h3>Hours</h3><table class="hours"><tbody>{hrs}</tbody></table><p class="flag" style="margin-top:12px">Hours as listed online — call to confirm. Times are Central.</p>
<h3 style="margin-top:40px">Service area</h3><p>Based in Cypress, serving Greater Houston — including Houston, Baytown, Tomball and the surrounding suburbs.</p>
<div class="map"><iframe title="Map of the Greater Houston service area" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Houston,+TX&amp;z=9&amp;output=embed"></iframe></div></div>
</div></section>'''
    return out+footer()

def page_404():
    p='404.html'; title='Page not found | Saint Pressure Washing LLC'
    b='/saintpressurewashing/'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="robots" content="noindex">
<link rel="icon" href="{b}brand/favicon.ico"><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,700..900&family=Barlow:wght@400;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet"><link rel="stylesheet" href="{b}assets/site.css?v=1"></head>
<body><main class="phero" style="min-height:100vh;display:grid;place-items:center;text-align:center"><div class="wrap"><img src="{b}brand/logo-badge-240.webp" width="240" height="215" alt="{E(D['name'])} logo" style="margin:0 auto 30px;width:160px">
<h1>Missed a <span class="y">spot.</span></h1><p class="lede" style="margin:0 auto 30px">That page isn’t here. Head back home or call for a free quote.</p>
<div class="ctas" style="justify-content:center"><a class="btn" href="{b}">Back home</a><a class="btn ghost" href="{D['tel']}">Call {D['phone']}</a></div></div></main></body></html>'''

def llms():
    s=f"""# {D['name']}
> {D['intro']} Motto: "{D['slogan']}."

- Phone (call or text): {D['phone']}
- Email: {D['email']}
- Based in: Cypress, TX — serves the greater Houston area (recent jobs tagged in Houston, Baytown, Tomball, Cypress)
- Hours as listed online (please call to confirm): Mon–Fri 7:30 AM–5:30 PM, Sat 8:30 AM–6:30 PM, Sun 9:30 AM–3:30 PM (Central)
- Free quote & consultation on every job
- Facebook: {D['facebook']} · Instagram: {D['instagram']} · Current site: {D['oldsite']}

## Services
""" + ''.join(f"- {s['short']}: {s['body']}\n" for s in SERVICES) + """
## Pricing
No published prices. Estimates depend on area size, surface type and condition, level of buildup and special requirements; a clear, upfront estimate is given after assessing the job.

## Reviews (verbatim)
""" + ''.join(f"- {r['name']} ({r['src']}): \"{r['text']}\"\n" for r in REVIEWS) + f"""
## Pages
- Home: {BASE}
- Services: {BASE}services.html
- Our Work (before/after, gallery, job posts): {BASE}work.html
- About & FAQ: {BASE}about.html
- Free Quote / Contact: {BASE}contact.html
"""
    return s

def og():
    from PIL import ImageDraw, ImageFont
    im=Image.open(os.path.join(ROOT,'img/hero-lot.webp')).convert('RGB')
    W,H=1200,630; r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1)); im=im.crop((0,(im.height-H)//2,W,(im.height-H)//2+H))
    ov=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(ov)
    for x in range(W): d.line([(x,0),(x,H)],fill=(6,9,15,int(235*max(0,1-x/900))))
    im=Image.alpha_composite(im.convert('RGBA'),ov)
    lg=Image.open(os.path.join(ROOT,'brand/logo-badge-1200.png')).convert('RGBA'); lg.thumbnail((300,300)); im.alpha_composite(lg,(60,60))
    d=ImageDraw.Draw(im)
    try:
        f1=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Archivo/Archivo-VariableFont_wdth,wght.ttf',62); f1.set_variation_by_axes([125,900])
        f2=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Barlow/Barlow-SemiBold.ttf',30)
    except Exception: f1=f2=ImageFont.load_default()
    d.text((60,360),"YOU MAKE THE MESS.",font=f1,fill='white'); d.text((60,430),"WE'LL DO THE REST.",font=f1,fill=(255,214,10))
    d.text((60,520),'Commercial pressure washing & striping · Greater Houston · (281) 908-7222',font=f2,fill=(200,225,245))
    im.convert('RGB').save(os.path.join(OUT,'og.jpg'),quality=86)

def main():
    if os.path.isdir(OUT):
        for n in os.listdir(OUT):
            if n in ('.git',): continue
            pth=os.path.join(OUT,n); shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
    os.makedirs(OUT+'/assets',exist_ok=True)
    for d in ('img','brand'): shutil.copytree(os.path.join(ROOT,d),os.path.join(OUT,d))
    for f in ('site.css','site.js'): shutil.copy(os.path.join(ROOT,'src',f),os.path.join(OUT,'assets',f))
    pages={'index.html':page_home(),'services.html':page_services(),'work.html':page_work(),'about.html':page_about(),'contact.html':page_contact(),'404.html':page_404()}
    for n,h in pages.items(): open(os.path.join(OUT,n),'w').write(h)
    open(os.path.join(OUT,'llms.txt'),'w').write(llms())
    open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    today=datetime.date.today().isoformat()
    open(os.path.join(OUT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{"" if h=="index.html" else h}</loc><lastmod>{today}</lastmod></url>' for h,_ in PAGES)+'</urlset>\n')
    open(os.path.join(OUT,'.nojekyll'),'w').write('')
    og(); print('built', list(pages))
if __name__=='__main__': main()
