"""Génère les pages HTML du site dans dist/. Lancer : python3 build.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
R = json.loads((ROOT / "route-svg.json").read_text())

NAV = [("index.html", "Accueil"), ("parcours.html", "Parcours"), ("place/index.html", "Le village"), ("horaires.html", "Horaires"),
       ("infos-pratiques.html", "Infos pratiques"), ("association.html", "Association")]

ICONS = {
    "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "bib": '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h8M8 14h5"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "bag": '<path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "bolt": '<path d="M13 3 5 14h6l-1 7 8-11h-6l1-7z"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5a3 3 0 0 1 0 6M21 20c0-2.7-1.6-5-4-5.7"/>',
    "hand": '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v5M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9a1.5 1.5 0 0 1 3 0v4a8 8 0 0 1-8 8h-.5a6 6 0 0 1-5-2.7L3 15.5a1.5 1.5 0 0 1 2.4-1.8L7 15"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3z"/>',
}
def ico(n): return f'<span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg></span>'

def route_svg(cls="", labels=True, runner=True):
    km = "".join(f'<circle class="km-dot" cx="{x}" cy="{y}" r="16"/><text class="km-txt" x="{x+26}" y="{y+10}">{i}</text>'
                 for i, (x, y) in enumerate(R["km"]) if i and labels)
    sx, sy = R["km"][0]
    return (f'<svg class="{cls}" viewBox="0 0 {R["w"]} {R["h"]}" role="img" aria-label="Tracé de la boucle de 5 km dans Toulouse">'
            f'<path class="route-bg" d="{R["d"]}"/><path class="route-path" d="{R["d"]}"/>{km}'
            f'<circle class="start-dot" cx="{sx}" cy="{sy}" r="20"/>'
            + (f'<circle class="runner" r="11" cx="{sx}" cy="{sy}" style="opacity:0"/>' if runner else "") + "</svg>")

CUR = ' aria-current="page"'

def page(slug, title, desc, body, head_extra="", scripts=""):
    links = "".join(f'<a href="{h}"{CUR if h == slug else ""}>{t}</a>' for h, t in NAV)
    foot_links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV + [("inscriptions.html", "Inscriptions")])
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#14040c">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='24' fill='%2314040c'/%3E%3Ctext x='50' y='70' font-size='58' font-weight='900' font-style='italic' text-anchor='middle' fill='%23ff3d97' font-family='Arial'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@1,800;1,900&family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{head_extra}<script src="script.js" defer></script>
{scripts}</head>
<body>
<div class="glow" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html">STUD<span>’N RUN</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span></button>
    <nav class="nav-links" id="nav" aria-label="Navigation principale">{links}<a class="cta" href="inscriptions.html"{CUR if slug == "inscriptions.html" else ""}>S’inscrire</a></nav>
  </div>
</header>
<main>
{body}
</main>
<div class="notice" role="note">Site de démonstration · Date, horaires, tarifs et équipe sont fictifs. Le parcours est le tracé réel prévu.</div>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-big" aria-hidden="true">STUD<span>’N</span> RUN</div>
    <div class="foot-row"><span>Course étudiante · Place Saint-Pierre · Toulouse</span><nav aria-label="Pied de page">{foot_links}</nav></div>
  </div>
</footer>
</body>
</html>
'''

def hero(eyebrow, h1, lead):
    return f'<section class="page-hero"><div class="wrap"><p class="eyebrow rv">{eyebrow}</p><h1 class="rv d1">{h1}</h1><p class="lead rv d2">{lead}</p></div></section>'

MARQ = '<div class="marquee{cls}" aria-hidden="true"><div class="marquee-track">' + "".join(
    f"<span>{w}</span>" for w in ["5 KM", "10 KM", "PLACE SAINT-PIERRE", "TOUS CAMPUS", "22 MAI 2027", "UNE VILLE, DEUX DÉFIS"] * 4) + "</div></div>"

def loops(n):
    return f'<svg class="loops" viewBox="0 0 {R["w"]} {R["h"]}" aria-hidden="true">' + "".join(
        f'<path d="{R["d"]}" transform="translate({i*60} {i*60})"/>' for i in range(n)) + "</svg>"

CTA = '''<section><div class="wrap"><div class="cta-band rv">
<span class="ring" style="width:500px;height:500px;left:-150px;top:-200px"></span><span class="ring" style="width:380px;height:380px;right:-120px;bottom:-180px"></span>
<p class="eyebrow" style="color:#fff">5 000 dossards</p><h2>T’ES CHAUD&nbsp;?</h2>
<p class="lead" style="margin:0 auto 30px;color:#ffe3f0">Inscriptions du 1er février au 15 mai 2027. 5 ou 10 km, tu choisis ton défi.</p>
<div class="btns" style="justify-content:center"><a class="btn" href="inscriptions.html">Je prends mon dossard <span class="arr">→</span></a></div>
</div></div></section>'''

STEPS = [
    ("0", "Place Saint-Pierre", "Départ au bord de la Garonne, au cœur du quartier étudiant. L’ambiance est garantie dès la ligne."),
    ("0,2", "Allée de Barcelone", "On remonte le long du canal de Brienne, à l’ombre des platanes."),
    ("0,8", "Les boulevards", "Leclerc, Duportal, Lascrosses puis d’Arcole : de grandes avenues pour trouver son rythme."),
    ("2,0", "Saint-Sernin", "Rue de l’Arc puis rue Saint-Bernard jusqu’à la basilique. Point d’eau en vue."),
    ("2,6", "Capitole", "La rue du Taur mène tout droit à la place du Capitole, le cœur de la ville."),
    ("3,0", "Centre historique", "Rues Saint-Rome et des Changes jusqu’à Esquirol, puis la rue de Metz vers le fleuve."),
    ("3,7", "Pont Neuf", "Première traversée de la Garonne, avec la vue sur les quais."),
    ("4,0", "Saint-Cyprien", "Rue de la République puis rue du Pont Saint-Pierre, côté rive gauche."),
    ("4,7", "Pont Saint-Pierre", "Retour rive droite, dernière ligne droite vers la place. Pour le 10 km, c’est reparti pour un tour."),
]
KM = R["km_total"]; KMs = f"{KM:.2f}".replace(".", ","); KM2s = f"{2*KM:.2f}".replace(".", ",")

# ---------------- ACCUEIL ----------------
index = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Course étudiante · Toulouse</p>
      <h1><span class="l"><span>STUD’N</span></span><span class="l"><span><em>RUN</em></span></span></h1>
      <div class="hero-meta"><span class="chip"><b>22.05</b> 2027</span><span class="chip">Place Saint-Pierre</span><span class="chip"><b>5</b> ou <b>10</b> km</span></div>
      <p class="lead">Tous les campus de Toulouse sur la même ligne de départ. Une boucle au cœur de la ville, deux ponts sur la Garonne, et une arrivée en fête.</p>
      <div class="btns" style="margin-top:28px"><a class="btn" href="inscriptions.html">Je m’inscris <span class="arr">→</span></a><a class="btn ghost" href="parcours.html">Voir le parcours 3D</a></div>
      <div class="countdown" data-date="2027-05-22T09:30:00+02:00" aria-label="Compte à rebours avant le départ">
        <div><b>–</b><span>jours</span></div><div><b>–</b><span>heures</span></div><div><b>–</b><span>min</span></div><div><b>–</b><span>sec</span></div>
      </div>
    </div>
    <div class="hero-route">{route_svg()}</div>
  </div>
  <span class="scroll-hint">Défiler</span>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">Choisis ton défi</p><h2 class="rv d1">UNE VILLE.<br><em>DEUX DÉFIS.</em></h2></div>
    <p class="lead rv d2">La même boucle de 5 km, à courir une fois ou deux. Débutant ou habitué, il y a une distance pour toi.</p></div>
    <div class="duo">
      <article class="dist rv">{loops(1)}<span class="tag">Découverte</span><div class="big">5<small>KM</small></div>
        <ul><li><span>Boucles</span><b>1</b></li><li><span>Distance</span><b>{KMs} km</b></li><li><span>Dénivelé</span><b>≈ 50 m D+</b></li></ul></article>
      <article class="dist hot rv d1">{loops(2)}<span class="tag">Challenge</span><div class="big">10<small>KM</small></div>
        <ul><li><span>Boucles</span><b>2</b></li><li><span>Distance</span><b>{KM2s} km</b></li><li><span>Dénivelé</span><b>≈ 100 m D+</b></li></ul></article>
    </div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">La boucle</p><h2 class="rv d1">5 KM DANS<br><em>LA VILLE ROSE.</em></h2></div>
    <a class="btn ghost rv d2" href="parcours.html">Explorer en 3D <span class="arr">→</span></a></div>
    <div class="story">
      <div class="story-map">{route_svg(runner=True)}</div>
      <ol class="steps">{"".join(f'<li class="step"><span class="km">{k}<small style="font-size:.45em"> km</small></span><div><h3>{t}</h3><p>{d}</p></div></li>' for k, t, d in STEPS)}</ol>
    </div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap stats">
    <div class="stat rv"><b data-count="5000">0</b><span>dossards</span></div>
    <div class="stat rv d1"><b data-count="{KM}">0</b><span>km par boucle</span></div>
    <div class="stat rv d2"><b data-count="2">0</b><span>ponts sur la Garonne</span></div>
    <div class="stat rv d3"><b data-count="1">0</b><span>place en fête à l’arrivée</span></div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">Prépare ta course</p><h2 class="rv d1">TOUT CE QU’IL<br><em>FAUT SAVOIR.</em></h2></div></div>
    <div class="grid-3">
      <a class="card rv" href="horaires.html">{ico("bolt")}<span class="go">↗</span><h3>Horaires</h3><p>Dossards, échauffement, départ et remise des prix.</p></a>
      <a class="card rv d1" href="infos-pratiques.html">{ico("pin")}<span class="go">↗</span><h3>Infos pratiques</h3><p>Accès, consigne, ravitaillement et questions fréquentes.</p></a>
      <a class="card rv d2" href="association.html">{ico("users")}<span class="go">↗</span><h3>L’équipe</h3><p>L’asso, les BDE et les bénévoles derrière la course.</p></a>
    </div>
  </div>
</section>
{CTA}
'''

# ---------------- PARCOURS ----------------
lo, hi = R["lo"], R["hi"]
parcours = hero("Le parcours", "LA <em>BOUCLE</em>", f"Départ et arrivée Place Saint-Pierre. Une boucle de {KMs} km, une fois pour le 5 km, deux fois pour le 10 km.") + f'''
<section style="padding-top:0">
  <div class="wrap">
    <div class="map-shell rv">
      <div id="map3d" aria-label="Carte 3D interactive du parcours"></div>
      <div class="map-ui"><button class="btn" id="fly-btn" type="button">▶&nbsp; Survoler le parcours</button><button class="btn ghost" id="reset-btn" type="button" style="background:rgba(20,4,12,.75)">Vue d’ensemble</button><div class="map-progress"><i></i></div><span class="map-km">0,00 km</span></div>
      <noscript><img src="assets/parcours-carte.jpg" alt="Carte du parcours"></noscript>
    </div>
    <p style="color:var(--muted);font-size:.85rem;margin-top:12px">Ctrl + molette pour zoomer, clic droit + glisser pour pivoter et incliner. Deux doigts sur mobile.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="stats" style="margin-bottom:60px">
      <div class="stat rv"><b>{KMs}</b><span>km par boucle</span></div>
      <div class="stat rv d1"><b>{KM2s}</b><span>km pour 2 boucles</span></div>
      <div class="stat rv d2"><b>≈50</b><span>m D+ par boucle</span></div>
      <div class="stat rv d3"><b>{round(lo)}–{round(hi)}</b><span>m d’altitude</span></div>
    </div>
    <div class="profile rv">
      <p class="eyebrow">Profil altimétrique · 1 boucle</p>
      <svg viewBox="0 0 1000 230" role="img" aria-label="Profil altimétrique de la boucle, de {round(lo)} à {round(hi)} mètres">
        <defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff3d97" stop-opacity=".55"/><stop offset="1" stop-color="#ff3d97" stop-opacity="0"/></linearGradient></defs>
        <path class="area" d="{R["prof"]} L1000 200 L0 200 Z"/><path class="ln" d="{R["prof"]}"/>
        {"".join(f'<text x="{min(max(i*1000/KM,14),985):.0f}" y="225" text-anchor="middle">{i} km</text>' for i in range(6))}
      </svg>
    </div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">Points de passage</p><h2 class="rv d1">KILOMÈTRE<br><em>PAR KILOMÈTRE.</em></h2></div></div>
    <ol class="timeline">{"".join(f'<li class="tl rv{" key" if i in (0, len(STEPS)-1) else ""}"><time>{k} km</time><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (k, t, d) in enumerate(STEPS))}</ol>
    <div class="btns rv" style="margin-top:50px"><a class="btn" href="assets/stud-n-run-plan-parcours.pdf" download>Télécharger le plan (PDF) <span class="arr">↓</span></a><a class="btn ghost" href="assets/stud-n-run-parcours.gpx" download>Trace GPX pour ta montre <span class="arr">↓</span></a></div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap">
  <div class="cta-band rv" style="text-align:left;background:linear-gradient(120deg,#33101f,#1f0814)">
    <p class="eyebrow">Maquette 3D</p><h2 style="font-size:clamp(3rem,8vw,7rem)">LE VILLAGE<br><em>JOUR DE COURSE</em></h2>
    <p class="lead" style="margin-bottom:26px">La Place Saint-Pierre à l’échelle réelle : bâtiments, quais, gradins, pont et arche de départ et d’arrivée. Survole la place et explore l’implantation du village.</p>
    <div class="btns"><a class="btn" href="place/index.html">Explorer la place en 3D <span class="arr">→</span></a></div>
  </div>
</div></section>
{CTA}
'''

# ---------------- HORAIRES ----------------
PROG = [("8 h 00", "Ouverture du village", "Accueil Place Saint-Pierre, consigne et stands des BDE.", False),
        ("8 h 00 – 9 h 15", "Retrait des dossards", "Au stand accueil, avec ta pièce d’identité et ta carte étudiante.", False),
        ("9 h 15", "Échauffement collectif", "Dix minutes en musique pour se mettre dans le rythme.", False),
        ("9 h 25", "Appel au départ", "Le 10 km dans le premier sas, le 5 km juste derrière.", False),
        ("9 h 30", "Départ 5 & 10 km", "Le départ est donné. Le 5 km fait une boucle, le 10 km en fait deux.", True),
        ("10 h 45", "Fermeture de la course", "Les derniers coureurs du 10 km passent la ligne.", False),
        ("11 h 00", "Remise des prix", "Podiums par distance, prix du campus le plus représenté, puis la fête continue.", True)]
horaires = hero("Samedi 22 mai 2027", "LE <em>JOUR J</em>", "Le programme de la journée, du café du matin jusqu’aux podiums.") + f'''
<section style="padding-top:0"><div class="wrap">
<ol class="timeline">{"".join(f'<li class="tl rv{" key" if k else ""}"><time>{h}</time><div><h3>{t}</h3><p>{d}</p></div></li>' for h, t, d, k in PROG)}</ol>
</div></section>
{CTA}
'''

# ---------------- INFOS ----------------
FAQ = [("À qui s’adresse la course ?", "Aux étudiants des écoles et universités de Toulouse, débutants comme coureurs réguliers. Dans cet exemple, la course est ouverte aux étudiants majeurs, quel que soit leur niveau."),
       ("5 ou 10 km, je choisis comment ?", "Le 5 km est une boucle, idéale pour une première course. Le 10 km, ce sont deux boucles pour ceux qui veulent un vrai chrono. Tu choisis à l’inscription."),
       ("Quels documents faut-il fournir ?", "Les justificatifs demandés (carte étudiante, document médical) seront précisés à l’ouverture des inscriptions, selon la réglementation en vigueur."),
       ("Y a-t-il du ravitaillement ?", "Un point d’eau vers le km 2,5, près de Saint-Sernin, où les coureurs du 10 km passent deux fois. Un ravitaillement complet attend tout le monde à l’arrivée."),
       ("Je peux venir encourager ?", "Oui ! La Place Saint-Pierre et les deux ponts sont les meilleurs spots. Reste derrière les barrières pour laisser le passage aux coureurs."),
       ("Comment devenir bénévole ?", "Accueil, dossards, signaleurs sur le parcours : découvre les rôles sur la page Association.")]
infos = hero("Infos pratiques", "BIEN <em>PRÉPARÉ</em>", "Accès, services et réponses aux questions fréquentes.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="grid-3">
  <div class="card rv">{ico("pin")}<h3>Accès</h3><p>Place Saint-Pierre, Toulouse. Viens à pied, à vélo ou en transports, il n’y a pas de parking sur place.</p></div>
  <div class="card rv d1">{ico("bib")}<h3>Dossards</h3><p>Retrait au stand accueil du village, de 8 h 00 à 9 h 15 le jour de la course.</p></div>
  <div class="card rv d2">{ico("bag")}<h3>Consigne</h3><p>Consigne gratuite au village. Garde tes objets de valeur avec toi.</p></div>
  <div class="card rv">{ico("drop")}<h3>Ravitaillement</h3><p>Point d’eau au km 2,5, ravitaillement complet à l’arrivée. Gobelets recyclables.</p></div>
  <div class="card rv d1">{ico("heart")}<h3>Secours</h3><p>Un poste de secours au village, une équipe mobile sur le parcours et des signaleurs à chaque carrefour.</p></div>
  <div class="card rv d2">{ico("star")}<h3>Après la course</h3><p>Podiums, stands des BDE et musique sur la place pour fêter ça.</p></div>
</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">FAQ</p><h2 class="rv d1">QUESTIONS<br><em>FRÉQUENTES.</em></h2></div></div>
<div class="faq rv">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
</div></section>
{CTA}
'''

# ---------------- INSCRIPTIONS ----------------
inscriptions = hero("Inscriptions · du 1er février au 15 mai 2027", "PRENDS TON <em>DOSSARD</em>", "Cette page est un exemple : aucune inscription ni aucun paiement ne sont possibles pour l’instant.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="grid-2">
  <div class="card price rv"><span class="badge" style="background:rgba(255,255,255,.1)">Découverte</span><h3 style="font-size:3rem">5 KM</h3><div class="amt">8€<small> / dossard</small></div>
    <ul><li>1 boucle de {KMs} km</li><li>Chronométrage</li><li>Ravitaillement à l’arrivée</li><li>Accès au village</li></ul>
    <a class="btn ghost" aria-disabled="true" role="link">Bientôt disponible</a></div>
  <div class="card price feat rv d1"><span class="badge">Challenge</span><h3 style="font-size:3rem">10 KM</h3><div class="amt">8€<small> / dossard</small></div>
    <ul><li>2 boucles, {KM2s} km</li><li>Chronométrage avec temps de passage</li><li>Point d’eau au km 2,5 et 7,5</li><li>Accès au village</li></ul>
    <a class="btn" aria-disabled="true" role="link">Bientôt disponible</a></div>
</div>
<div class="stats" style="margin-top:60px">
  <div class="stat rv"><b data-count="5000">0</b><span>places au total</span></div>
  <div class="stat rv d1"><b>18+</b><span>étudiants majeurs</span></div>
  <div class="stat rv d2"><b>01.02</b><span>ouverture</span></div>
  <div class="stat rv d3"><b>15.05</b><span>clôture</span></div>
</div>
</div></section>
'''

# ---------------- ASSOCIATION ----------------
TEAM = [("C", "Camille Martin", "Présidence et coordination"), ("A", "Alex Moreau", "Parcours et logistique"), ("L", "Lina Bernard", "Bénévoles et vie de campus")]
association = hero("L’association", "PORTER LA <em>COURSE</em>", "Une équipe étudiante qui rassemble les campus toulousains autour du sport.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">L’équipe (fictive)</p><h2 class="rv d1">ON EST<br><em>DERRIÈRE.</em></h2></div></div>
<div class="team">{"".join(f'<div class="card member rv{" d"+str(i) if i else ""}"><div class="av" aria-hidden="true">{a}</div><div><h3>{n}</h3><p>{r}</p></div></div>' for i, (a, n, r) in enumerate(TEAM))}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">Rejoins le mouvement</p><h2 class="rv d1">COMMENT<br><em>T’IMPLIQUER.</em></h2></div></div>
<div class="grid-3">
  <div class="card rv">{ico("users")}<h3>Étudiants et BDE</h3><p>Relaie la course sur ton campus et monte une équipe avec ton école.</p></div>
  <div class="card rv d1">{ico("hand")}<h3>Bénévoles</h3><p>Accueil, dossards, ravitaillement, signaleurs : environ 30 personnes à mobiliser le jour J.</p></div>
  <div class="card rv d2">{ico("star")}<h3>Partenaires</h3><p>Apporte un soutien matériel ou financier et associe ta marque à l’événement.</p></div>
</div>
<p style="color:var(--muted);font-size:.85rem;margin-top:30px">Ces personnes et ces rôles sont fictifs. Aucun contact réel n’est associé à cette démonstration.</p>
</div></section>
{CTA}
'''

MAP_HEAD = '<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">\n'
MAP_JS = '<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js" defer></script>\n<script src="parcours-3d.js" defer></script>\n'
D = "Stud’N Run, course étudiante à Toulouse : 5 et 10 km au départ de la Place Saint-Pierre."
PAGES = {
    "index.html": ("Stud’N Run · Course étudiante Toulouse", index, "", ""),
    "parcours.html": ("Parcours · Stud’N Run", parcours, MAP_HEAD, MAP_JS),
    "horaires.html": ("Horaires · Stud’N Run", horaires, "", ""),
    "infos-pratiques.html": ("Infos pratiques · Stud’N Run", infos, "", ""),
    "inscriptions.html": ("Inscriptions · Stud’N Run", inscriptions, "", ""),
    "association.html": ("Association · Stud’N Run", association, "", ""),
}
for slug, (t, body, h, s) in PAGES.items():
    (DIST / slug).write_text(page(slug, t, D, body, h, s))
print("ok", len(PAGES), "pages")
