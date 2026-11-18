"""Génère les pages HTML du site dans dist/. Lancer : python3 build.py"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
R = json.loads((ROOT / "route-svg.json").read_text())

NAV = [("index.html", "Accueil"), ("parcours.html", "Parcours"), ("ecoles.html", "Écoles"), ("horaires.html", "Horaires"),
       ("infos-pratiques.html", "Infos pratiques"), ("actualites.html", "Actualités"), ("partenaires.html", "Partenaires"), ("association.html", "Association")]

# Partenaires affichés dans le pied de page et sur la page Partenaires. Matecito = PLACEHOLDER (rien n'est signé) : à retirer avant « publie » si pas confirmé.
PARTNERS = []
# Réseaux sociaux : renseigner l'URL pour qu'ils s'affichent (rien n'est affiché tant que c'est vide).
SOCIAL = {"Instagram": "", "TikTok": "", "LinkedIn": ""}
CONTACT = "studnrun@gmail.com"

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
    social_links = "".join(f'<a href="{u}" rel="noopener" target="_blank">{n}</a>' for n, u in SOCIAL.items() if u)
    partners_strip = ('<div class="foot-partners"><span>Partenaires</span>' + "".join(f'<b>{x}</b>' for x in PARTNERS) + '<a href="partenaires.html">Devenir partenaire →</a></div>') if PARTNERS else ""
    foot_links = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV + [("inscriptions.html", "Inscriptions"), ("benevoles.html", "Bénévoles"), ("contact.html", "Contact")])
    legal = '<div class="foot-legal"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a><span>© 2026 Stud’N Run</span></div>'
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
<link rel="icon" href="assets/icone.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
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
    <a class="brand" href="index.html"><img src="assets/logo.svg" alt="Stud’N Run" width="244" height="44"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span></button>
    <nav class="nav-links" id="nav" aria-label="Navigation principale">{links}<a class="cta" href="inscriptions.html"{CUR if slug == "inscriptions.html" else ""}>S’inscrire</a></nav>
  </div>
</header>
<main>
{body}
</main>
<div class="notice" role="note">Site en construction · Les tarifs et le parcours sont provisoires.</div>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-big" aria-hidden="true">STUD<span>’N</span> RUN</div>
    {partners_strip}
    <div class="foot-row"><span>Course étudiante · Place Saint-Pierre · Toulouse · <a href="mailto:{CONTACT}">{CONTACT}</a></span><nav aria-label="Pied de page">{foot_links}{social_links}</nav></div>
    {legal}
  </div>
</footer>
</body>
</html>
'''

def hero(eyebrow, h1, lead):
    return f'<section class="page-hero"><div class="wrap"><p class="eyebrow rv">{eyebrow}</p><h1 class="rv d1">{h1}</h1><p class="lead rv d2">{lead}</p></div></section>'

MARQ = '<div class="marquee{cls}" aria-hidden="true"><div class="marquee-track">' + "".join(
    f"<span>{w}</span>" for w in ["5 KM", "10 KM", "PLACE SAINT-PIERRE", "TOUS CAMPUS", "12 JUIN 2027", "UNE VILLE, DEUX DÉFIS"] * 4) + "</div></div>"

def loops(n):
    return f'<svg class="loops" viewBox="0 0 {R["w"]} {R["h"]}" aria-hidden="true">' + "".join(
        f'<path d="{R["d"]}" transform="translate({i*60} {i*60})"/>' for i in range(n)) + "</svg>"

CTA = '''<section><div class="wrap"><div class="cta-band rv">
<span class="ring" style="width:500px;height:500px;left:-150px;top:-200px"></span><span class="ring" style="width:380px;height:380px;right:-120px;bottom:-180px"></span>
<p class="eyebrow" style="color:#fff">5 000 dossards</p><h2>T’ES CHAUD&nbsp;?</h2>
<p class="lead" style="margin:0 auto 30px;color:#ffe3f0">Inscriptions du 1er février au 5 juin 2027. 5 ou 10 km, tu choisis ton défi.</p>
<div class="btns" style="justify-content:center"><a class="btn" href="inscriptions.html">Je prends mon dossard <span class="arr">→</span></a></div>
</div></div></section>'''

STEPS = [
    ("0", "Esplanade de l’Université", "Départ à deux pas de la Place Saint-Pierre, au cœur du quartier étudiant. L’ambiance est garantie dès la ligne."),
    ("0,2", "Campus de Toulouse 1", "On remonte le boulevard Duportal puis on traverse le campus par les rues de l’Université et des Puits Creusés."),
    ("0,9", "Place Anatole France", "Puis la rue Valade, tout droit vers la Place Saint-Pierre et son village."),
    ("1,3", "Place Saint-Pierre", "Premier passage devant le village, juste avant de rejoindre les quais de la Garonne."),
    ("1,6", "Les quais", "Quai Lucien Lombard, place de la Daurade puis quais de la Daurade et de Tounis, face au fleuve."),
    ("2,5", "Quai de Tounis", "Point d’eau sur le quai, demi-tour au bout puis retour sur le même axe vers le Pont Neuf."),
    ("3,4", "Pont Neuf", "Traversée de la Garonne, avec la vue sur les quais."),
    ("3,6", "Saint-Cyprien", "Rue de la République puis rue du Pont Saint-Pierre, côté rive gauche."),
    ("4,4", "Pont Saint-Pierre", "Retour rive droite, dernière ligne droite vers l’esplanade. Pour le 10 km, c’est reparti pour un tour."),
]
KM = R["km_total"]; KMs = f"{KM:.2f}".replace(".", ","); KM2s = f"{R.get('km_total2', 2*KM):.2f}".replace(".", ",")

# ---------------- ACCUEIL ----------------
index = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Course étudiante · Toulouse</p>
      <h1><span class="l"><span>STUD’N</span></span><span class="l"><span><em>RUN</em></span></span></h1>
      <div class="hero-meta"><span class="chip"><b>12.06</b> 2027</span><span class="chip">Place Saint-Pierre</span><span class="chip"><b>5</b> ou <b>10</b> km</span></div>
      <p class="lead">Tous les campus de Toulouse sur la même ligne de départ. Une boucle au cœur de la ville, deux ponts sur la Garonne, et une arrivée en fête.</p>
      <div class="btns" style="margin-top:28px"><a class="btn" href="inscriptions.html">Je m’inscris <span class="arr">→</span></a><a class="btn ghost" href="parcours.html">Voir le parcours 3D</a></div>
      <div class="countdown" data-date="2027-06-12T17:30:00+02:00" aria-label="Compte à rebours avant le départ">
        <div><b>–</b><span>jours</span></div><div><b>–</b><span>heures</span></div><div><b>–</b><span>min</span></div><div><b>–</b><span>sec</span></div>
      </div>
    </div>
    <div class="hero-route">{route_svg()}</div>
  </div>
  <span class="scroll-hint">Défiler</span>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">Choisis ton défi</p><h2 class="rv d1">UNE VILLE. <em>DEUX DÉFIS.</em></h2></div>
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
    <div class="sec-head"><div><p class="eyebrow rv">La boucle</p><h2 class="rv d1">5 KM DANS <em>LA VILLE ROSE.</em></h2></div>
    <a class="btn ghost rv d2" href="parcours.html">Explorer en 3D <span class="arr">→</span></a></div>
    <div class="story">
      <div class="story-map">{route_svg(runner=True)}</div>
      <ol class="steps">{"".join(f'<li class="step"><span class="km">{k}<small style="font-size:.45em"> km</small></span><div><h3>{t}</h3><p>{d}</p></div></li>' for k, t, d in STEPS)}</ol>
    </div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap stats">
    <div class="stat rv"><b data-count="5000">0</b><span>coureurs, 5 ou 10 km</span></div>
    <div class="stat rv d1"><b data-count="189">0</b><span>écoles et universités invitées</span></div>
    <div class="stat rv d2"><b data-count="200">0</b><span>bénévoles le jour J</span></div>
    <div class="stat rv d3"><b data-count="3">0</b><span>associations soutenues</span></div>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow rv">Prépare ta course</p><h2 class="rv d1">TOUT CE QU’IL <em>FAUT SAVOIR.</em></h2></div></div>
    <div class="grid-3">
      <a class="card rv" href="horaires.html">{ico("bolt")}<span class="go">↗</span><h3>Horaires</h3><p>Dossards, départs, remise des prix et after run.</p></a>
      <a class="card rv d1" href="infos-pratiques.html">{ico("pin")}<span class="go">↗</span><h3>Infos pratiques</h3><p>Accès, consigne, ravitaillement et questions fréquentes.</p></a>
      <a class="card rv d2" href="association.html">{ico("users")}<span class="go">↗</span><h3>L’équipe</h3><p>L’asso, les BDE et les bénévoles derrière la course.</p></a>
    </div>
  </div>
</section>
{CTA}
'''

# ---------------- PARCOURS ----------------
lo, hi = R["lo"], R["hi"]
parcours = hero("Le parcours", "LA <em>BOUCLE</em>", f"Départ et arrivée Esplanade de l’Université, à côté de la Place Saint-Pierre. Une boucle de {KMs} km, une fois pour le 5 km, deux fois pour le 10 km.") + f'''
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
    <div class="stats" style="margin-bottom:30px">
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
    <div class="sec-head"><div><p class="eyebrow rv">Points de passage</p><h2 class="rv d1">KILOMÈTRE <em>PAR KILOMÈTRE.</em></h2></div></div>
    <ol class="timeline">{"".join(f'<li class="tl rv{" key" if i in (0, len(STEPS)-1) else ""}"><time>{k} km</time><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (k, t, d) in enumerate(STEPS))}</ol>
    <div class="btns rv" style="margin-top:50px"><a class="btn" href="assets/stud-n-run-plan-parcours.pdf" download>Télécharger le plan (PDF) <span class="arr">↓</span></a><a class="btn ghost" href="assets/stud-n-run-parcours.gpx" download>Trace GPX pour ta montre <span class="arr">↓</span></a></div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap">
  <div class="cta-band rv" style="text-align:left;background:linear-gradient(120deg,#33101f,#1f0814)">
    <p class="eyebrow">Maquette 3D</p><h2 style="font-size:clamp(2.2rem,4.6vw,3.8rem)">LE VILLAGE <em>JOUR DE COURSE</em></h2>
    <p class="lead" style="margin-bottom:26px">La Place Saint-Pierre à l’échelle réelle : bâtiments, quais, gradins, pont et arche de départ et d’arrivée. Survole la place et explore l’implantation du village.</p>
    <div class="btns"><a class="btn" href="place/index.html">Explorer la place en 3D <span class="arr">→</span></a></div>
  </div>
</div></section>
{CTA}
'''

# ---------------- HORAIRES ----------------
NBSP = "\u00a0"
DAYS = [("Vendredi 11 juin", "La veille", [
          ("17 h – 22 h", "Retrait des dossards", "À TSE (Toulouse School of Economics), avec ta pièce d’identité et ta carte étudiante.", False)]),
        ("Samedi 12 juin", "Le jour J", [
          ("9 h – 12 h", "Retrait des dossards", "Toujours à TSE, avec ta pièce d’identité et ta carte étudiante.", False),
          ("13 h 00", "Ouverture du village", "Accueil, consigne et stands des BDE.", False),
          ("17 h 20", "Appel du 5 km", "Direction la ligne de départ. Pas d’échauffement collectif : échauffe-toi de ton côté.", False),
          ("17 h 30", "Départ du 5 km", "Le 5 km fait une boucle.", True),
          ("18 h 30", "Appel du 10 km", "Le 10 km se place sur la ligne de départ.", False),
          ("18 h 45", "Départ du 10 km", "Le 10 km fait deux boucles.", True),
          ("20 h 45", "Remise des prix", "Podiums par distance, prix du campus le plus représenté.", True),
          ("21 h 30", "After run", "La fête continue au village.", False)])]
horaires = hero("Vendredi 11 et samedi 12 juin 2027", "LES <em>HORAIRES</em>", "Le programme, de la veille à l’after run.") + f'''
<section style="padding-top:0"><div class="wrap">
{"".join(f'<div class="day"><h2 class="day-title rv"><em>{d}</em> {t}</h2><ol class="timeline">' + "".join(f'<li class="tl rv{" key" if k else ""}"><time>{h.replace(" ", NBSP)}</time><div><h3>{ti}</h3><p>{de}</p></div></li>' for h, ti, de, k in items) + '</ol></div>' for d, t, items in DAYS)}
</div></section>
{CTA}
'''

# ---------------- INFOS ----------------
FAQ = [("À qui s’adresse la course ?", "Aux étudiants des écoles et universités de Toulouse, débutants comme coureurs réguliers. Dans cet exemple, la course est ouverte aux étudiants majeurs, quel que soit leur niveau."),
       ("5 ou 10 km, je choisis comment ?", "Le 5 km est une boucle, idéale pour une première course. Le 10 km, ce sont deux boucles pour ceux qui veulent un vrai chrono. Tu choisis à l’inscription."),
       ("Quels documents faut-il fournir ?", "Les justificatifs demandés (carte étudiante, document médical) seront précisés à l’ouverture des inscriptions, selon la réglementation en vigueur."),
       ("Y a-t-il du ravitaillement ?", "Un point d’eau vers le km 2,5, sur le quai de Tounis, où les coureurs du 10 km passent deux fois. Un ravitaillement complet attend tout le monde à l’arrivée."),
       ("Je peux venir encourager ?", "Oui ! La Place Saint-Pierre et les deux ponts sont les meilleurs spots. Reste derrière les barrières pour laisser le passage aux coureurs."),
       ("Où va l’argent des inscriptions ?", "Une partie des inscriptions et tous les dons du jour sont reversés, à parts égales, à trois associations qui luttent contre la précarité étudiante : Le Casse-dalle, Le Petit Sab’lé et Le Rayon 31."),
       ("Mon école ou mon BDE peut participer ?", "Oui, 189 écoles et universités toulousaines sont invitées. Chaque campus peut monter son équipe pour le challenge entre écoles : retrouve la liste sur la page Écoles ou écris-nous."),
       ("Une question qui n’est pas ici ?", f"Écris-nous à <a href=\"mailto:{CONTACT}\">{CONTACT}</a>, on te répond vite."),
       ("Comment devenir bénévole ?", "Accueil, dossards, signaleurs sur le parcours : découvre les rôles sur la page Association.")]
infos = hero("Infos pratiques", "BIEN <em>PRÉPARÉ</em>", "Accès, services et réponses aux questions fréquentes.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="grid-3">
  <div class="card rv">{ico("pin")}<h3>Accès</h3><p>Place Saint-Pierre, Toulouse. Viens à pied, à vélo ou en transports, il n’y a pas de parking sur place.</p></div>
  <div class="card rv d1">{ico("bib")}<h3>Dossards</h3><p>Retrait à TSE, la veille de 17 h à 22 h ou le matin de la course de 9 h à 12 h.</p></div>
  <div class="card rv d2">{ico("bag")}<h3>Consigne</h3><p>Consigne gratuite au village. Garde tes objets de valeur avec toi.</p></div>
  <div class="card rv">{ico("drop")}<h3>Ravitaillement</h3><p>Point d’eau au km 2,5, ravitaillement complet à l’arrivée. Gobelets recyclables.</p></div>
  <div class="card rv d1">{ico("heart")}<h3>Secours</h3><p>Un poste de secours au village, une équipe mobile sur le parcours et des signaleurs à chaque carrefour.</p></div>
  <div class="card rv d2">{ico("star")}<h3>Après la course</h3><p>Podiums, stands des BDE et musique sur la place pour fêter ça.</p></div>
</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">FAQ</p><h2 class="rv d1">QUESTIONS <em>FRÉQUENTES.</em></h2></div></div>
<div class="faq rv">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
</div></section>
{CTA}
'''

# ---------------- INSCRIPTIONS ----------------
FORM_JS = """<script>
document.getElementById("__ID__").addEventListener("submit", function (e) {
  e.preventDefault(); var f = e.target, n = document.getElementById("__ID__-note");
  if (!f.prenom.value.trim() || !/^\\S+@\\S+\\.\\S+$/.test(f.email.value) || !f.ok.checked) { n.textContent = "Complète ton prénom, un e-mail valide et coche la case."; return; }
  var body = "__TXT__\\n\\nPrénom : " + f.prenom.value + "\\nE-mail : " + f.email.value + "\\nÉcole : " + (f.ecole.value || "-");
  location.href = "mailto:__CONTACT__?subject=" + encodeURIComponent("__SUBJ__") + "&body=" + encodeURIComponent(body);
  n.textContent = "Ton application e-mail s’ouvre : envoie le message pour valider.";
});
</script>""".replace("__CONTACT__", CONTACT)
PREREG_JS = FORM_JS.replace("__ID__", "prereg").replace("__SUBJ__", "Pré-inscription Stud’N Run").replace("__TXT__", "Bonjour, prévenez-moi à l’ouverture des inscriptions.")

inscriptions = hero("Inscriptions · du 1er février au 5 juin 2027", "PRENDS TON <em>DOSSARD</em>", "Cette page est un exemple : aucune inscription ni aucun paiement ne sont possibles pour l’instant.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="grid-2">
  <div class="card price rv"><span class="badge" style="background:rgba(255,255,255,.1)">Découverte</span><h3 style="font-size:3rem">5 KM</h3><div class="amt">10€<small> / dossard</small></div>
    <ul><li>1 boucle de {KMs} km</li><li>Chronométrage</li><li>Ravitaillement à l’arrivée</li><li>Accès au village</li></ul>
    <a class="btn ghost" aria-disabled="true" role="link">Bientôt disponible</a></div>
  <div class="card price feat rv d1"><span class="badge">Challenge</span><h3 style="font-size:3rem">10 KM</h3><div class="amt">10€<small> / dossard</small></div>
    <ul><li>2 boucles, {KM2s} km</li><li>Chronométrage avec temps de passage</li><li>Point d’eau au km 2,5 et 7,5</li><li>Accès au village</li></ul>
    <a class="btn" aria-disabled="true" role="link">Bientôt disponible</a></div>
</div>
<div class="stats" style="margin-top:36px">
  <div class="stat rv"><b data-count="5000">0</b><span>places au total</span></div>
  <div class="stat rv d1"><b>18+</b><span>étudiants majeurs</span></div>
  <div class="stat rv d2"><b>01.02</b><span>ouverture</span></div>
  <div class="stat rv d3"><b>05.06</b><span>clôture</span></div>
</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="card prereg rv"><p class="eyebrow">Avant l’ouverture</p><h2>PRÉVIENS-MOI <em>QUAND ÇA OUVRE</em></h2>
<p class="lead" style="margin-bottom:24px">Laisse ton e-mail, on t’écrit le jour de l’ouverture des inscriptions. Rien d’autre.</p>
<form id="prereg" class="form" novalidate>
  <label>Prénom<input name="prenom" autocomplete="given-name" required></label>
  <label>E-mail<input name="email" type="email" autocomplete="email" required></label>
  <label>Ton école <small>(facultatif)</small><input name="ecole"></label>
  <label class="chk"><input type="checkbox" name="ok" required> J’accepte d’être contacté·e par Stud’N Run pour l’ouverture des inscriptions.</label>
  <button class="btn" type="submit">Me prévenir <span class="arr">→</span></button>
  <p class="form-note" id="prereg-note" role="status"></p>
</form></div>
</div></section>
{PREREG_JS}
'''

# ---------------- PARTENAIRES ----------------
partenaires = hero("Partenaires", "S’ASSOCIER <em>À LA COURSE</em>", "Un public jeune, réuni au même endroit, et une cause qui donne du sens.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">Ils nous soutiennent</p><h2 class="rv d1">NOS <em>PARTENAIRES</em></h2></div></div>
<div class="partner-wall rv">{"".join(f'<div class="partner-logo">{x}</div>' for x in PARTNERS)}<div class="partner-logo ghost">Votre marque ici</div></div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">Pourquoi s’associer</p><h2 class="rv d1">UN PUBLIC, <em>UNE CAUSE.</em></h2></div></div>
<div class="grid-3">
  <div class="card rv">{ico("users")}<h3>Un public jeune, réuni</h3><p>Jusqu’à 5 000 étudiants de 18 à 26 ans, issus de 189 écoles et universités toulousaines, sur la même ligne de départ.</p></div>
  <div class="card rv d1">{ico("heart")}<h3>Une cause qui donne du sens</h3><p>Une partie des inscriptions et tous les dons du jour sont reversés, à parts égales, à trois associations qui luttent contre la précarité étudiante.</p></div>
  <div class="card rv d2">{ico("star")}<h3>Un événement fait pour être vu</h3><p>Départ et arrivée au bord de la Garonne, arche, dossards, écran géant : votre soutien est visible du premier au dernier coureur.</p></div>
</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="cta-band rv" style="text-align:left;background:linear-gradient(120deg,#33101f,#1f0814)">
<p class="eyebrow">Devenir partenaire</p><h2 style="font-size:clamp(2.2rem,4.6vw,3.8rem)">PARLONS-EN <em>20 MINUTES</em></h2>
<p class="lead" style="margin-bottom:26px">Dites-nous ce que vous pouvez engager, en argent ou en nature : nous construisons ensemble la visibilité qui va avec.</p>
<div class="btns"><a class="btn" href="mailto:{CONTACT}?subject=Partenariat%20Stud%E2%80%99N%20Run">Nous écrire <span class="arr">→</span></a><a class="btn ghost" href="assets/StudNRun_fiche_partenaires.pdf" download>Télécharger la fiche (PDF) <span class="arr">↓</span></a></div>
</div></div></section>
'''


# ---------------- ACTUALITÉS ----------------
# Ajouter une actualité = une ligne ici (la plus récente en premier).
ARTICLES = [
    ("17 novembre 2026", "La date est fixée : samedi 12 juin 2027",
     "La première édition de Stud’N Run aura lieu le <b>samedi 12 juin 2027</b>, au départ de l’Esplanade de l’Université, à côté de la Place Saint-Pierre. Les inscriptions ouvriront le 1er février 2027."),
    ("17 novembre 2026", "Trois associations, une par université",
     "Une partie des inscriptions et tous les dons du jour seront reversés, à parts égales, à trois associations qui luttent contre la précarité étudiante : Le Casse-dalle (Jean-Jaurès), Le Petit Sab’lé (Paul-Sabatier) et Le Rayon 31 (Capitole)."),
    ("16 novembre 2026", "Un premier parcours de 4,96 km",
     "Le tracé provisoire est une boucle de 4,96 km autour du campus de Toulouse 1, avec les quais de la Garonne, le Pont Neuf, Saint-Cyprien et le Pont Saint-Pierre. Le 5 km fait une boucle, le 10 km en fait deux. Il reste à valider avec la Ville."),
    ("17 novembre 2026", "189 écoles invitées au challenge",
     "Universités, grandes écoles, écoles de commerce, d’ingénieurs, d’art, de santé : toutes les écoles post-bac de Toulouse sont invitées à monter leur équipe. La liste est sur la page Écoles."),
]
actualites = hero("Actualités", "LES <em>NOUVELLES</em>", "Où en est le projet, étape par étape.") + f'''
<section style="padding-top:0"><div class="wrap"><div class="news">
{"".join(f'<article class="card news-item rv"><time>{d}</time><h3>{t}</h3><p>{x}</p></article>' for d, t, x in ARTICLES)}
</div></div></section>
{CTA}
'''

# ---------------- BÉNÉVOLES ----------------
benevoles = hero("Bénévoles", "DEVIENS <em>BÉNÉVOLE</em>", "On cherche environ 200 personnes pour que la course se passe bien. Viens vivre la journée de l’intérieur.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">Les missions</p><h2 class="rv d1">TON RÔLE <em>LE JOUR J.</em></h2></div></div>
<div class="grid-3">
  <div class="card rv">{ico("bib")}<h3>Accueil et dossards</h3><p>Tu accueilles les coureurs, tu remets les dossards et tu les orientes dans le village.</p></div>
  <div class="card rv d1">{ico("pin")}<h3>Signaleurs</h3><p>Posté·e sur le parcours, tu guides les coureurs et tu veilles à la sécurité aux carrefours.</p></div>
  <div class="card rv d2">{ico("bag")}<h3>Ravitaillement et consigne</h3><p>Eau et ravitaillement à l’arrivée, consigne des sacs, remise des récompenses.</p></div>
</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="card prereg rv"><p class="eyebrow">Je me propose</p><h2>JE <em>VEUX AIDER</em></h2>
<p class="lead">Laisse-nous ton e-mail : on te recontacte avec les détails (horaires, repas, tenue). Une formation courte et un briefing sont prévus avant la course.</p>
<form id="vol" class="form" novalidate>
  <label>Prénom<input name="prenom" autocomplete="given-name" required></label>
  <label>E-mail<input name="email" type="email" autocomplete="email" required></label>
  <label>Ton école <small>(facultatif)</small><input name="ecole"></label>
  <label class="chk"><input type="checkbox" name="ok" required> J’accepte d’être contacté·e par Stud’N Run au sujet du bénévolat.</label>
  <button class="btn" type="submit">Proposer mon aide <span class="arr">→</span></button>
  <p class="form-note" id="vol-note" role="status"></p>
</form></div>
</div></section>
{FORM_JS.replace("__ID__", "vol").replace("__SUBJ__", "Bénévolat Stud’N Run").replace("__TXT__", "Bonjour, je souhaite être bénévole pour la course.")}
'''

# ---------------- CONTACT ----------------
contact = hero("Contact", "ON <em>SE PARLE</em> ?", "Une question, une idée, une envie d’aider : écris-nous.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="grid-3">
  <a class="card rv" href="mailto:{CONTACT}">{ico("users")}<span class="go">↗</span><h3>Coureurs, écoles, BDE</h3><p>{CONTACT}</p></a>
  <a class="card rv d1" href="mailto:{CONTACT}?subject=Partenariat%20Stud%E2%80%99N%20Run">{ico("star")}<span class="go">↗</span><h3>Entreprises et partenaires</h3><p>Écrivez-nous, ou consultez la page <b>Partenaires</b>.</p></a>
  <a class="card rv d2" href="mailto:{CONTACT}?subject=Presse%20Stud%E2%80%99N%20Run">{ico("hand")}<span class="go">↗</span><h3>Presse</h3><p>Un dossier de presse sera disponible ici avant la course. En attendant, écrivez-nous.</p></a>
</div>
</div></section>
'''

# ---------------- LÉGAL ----------------
legal_hero = lambda t, h: hero("Informations légales", h, "")
mentions = hero("Informations légales", "MENTIONS <em>LÉGALES</em>", "") + f'''
<section style="padding-top:0"><div class="wrap"><div class="prose">
<h2>Éditeur du site</h2>
<p>Stud’N Run, association loi 1901 déclarée à Toulouse (SIRET : en cours d’obtention). Siège : Toulouse.</p>
<p>Codirecteurs de la publication : Noah Salvatge et Yanis Jaber. Contact : <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<h2>Hébergement</h2>
<p>Site hébergé par GitHub Pages (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis).</p>
<h2>Propriété intellectuelle</h2>
<p>Le nom, le logo et les contenus du site appartiennent à Stud’N Run. Toute reproduction sans accord est interdite. Les logos des écoles et des partenaires appartiennent à leurs propriétaires.</p>
<h2>Responsabilité</h2>
<p>Les informations (date, parcours, horaires, tarifs) sont susceptibles d’évoluer jusqu’à la course et dépendent des autorisations de la Ville de Toulouse et de la préfecture.</p>
</div></div></section>
'''
confidentialite = hero("Informations légales", "VIE <em>PRIVÉE</em>", "") + f'''
<section style="padding-top:0"><div class="wrap"><div class="prose">
<h2>Quelles données ?</h2>
<p>Quand tu nous écris, ou que tu utilises le formulaire de pré-inscription ou de bénévolat, nous recevons ton prénom, ton e-mail et, si tu l’indiques, ton école. Ces formulaires ouvrent ton application e-mail : rien n’est envoyé tant que tu n’as pas envoyé le message toi-même.</p>
<h2>Pourquoi ?</h2>
<p>Uniquement pour te prévenir de l’ouverture des inscriptions ou te recontacter à propos du bénévolat. Tes données ne sont ni vendues ni transmises à des tiers.</p>
<h2>Combien de temps ?</h2>
<p>Jusqu’à la fin de l’édition 2027, puis supprimées, sauf si tu demandes à les conserver.</p>
<h2>Tes droits</h2>
<p>Tu peux demander l’accès, la rectification ou la suppression de tes données à tout moment à <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<h2>Cookies</h2>
<p>Ce site ne dépose aucun cookie de mesure d’audience ni de publicité, donc pas de bandeau à valider. Les polices (Google Fonts) et la carte du parcours sont chargées depuis des services externes, qui peuvent voir ton adresse IP comme sur tout site web.</p>
</div></div></section>
'''

# ---------------- ASSOCIATION ----------------
TEAM = [("N", "Noah Salvatge", "Codirecteur"), ("Y", "Yanis Jaber", "Codirecteur")]
association = hero("L’association", "PORTER LA <em>COURSE</em>", "Une équipe étudiante qui rassemble les campus toulousains autour du sport.") + f'''
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">L’équipe</p><h2 class="rv d1">ON EST <em>DERRIÈRE.</em></h2></div></div>
<div class="team">{"".join(f'<div class="card member rv{" d"+str(i) if i else ""}"><div class="av" aria-hidden="true">{a}</div><div><h3>{n}</h3><p>{r}</p></div></div>' for i, (a, n, r) in enumerate(TEAM))}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow rv">Rejoins le mouvement</p><h2 class="rv d1">COMMENT <em>T’IMPLIQUER.</em></h2></div></div>
<div class="grid-3">
  <div class="card rv">{ico("users")}<h3>Étudiants et BDE</h3><p>Relaie la course sur ton campus et monte une équipe avec ton école.</p></div>
  <div class="card rv d1">{ico("hand")}<h3>Bénévoles</h3><p>Accueil, dossards, ravitaillement, signaleurs : environ 200 personnes à mobiliser le jour J. <a href="benevoles.html" style="color:var(--pink-2)">Je m’inscris →</a></p></div>
  <div class="card rv d2">{ico("star")}<h3>Partenaires</h3><p>Apporte un soutien matériel ou financier et associe ta marque à l’événement.</p></div>
</div>

</div></section>
{CTA}
'''

# ---------------- ÉCOLES ----------------
CONTACT_MAIL = "studnrun@gmail.com"
ECOLES = json.loads((ROOT / "ecoles.json").read_text())
INFOS = {k: v for k, v in json.loads((ROOT / "ecoles-infos.json").read_text()).items() if not k.startswith("_")}
for e in ECOLES:
    i = INFOS.get(e["id"], {})
    e["i"] = {k: i[k] for k in ("referent", "instagram", "logo", "texte") if i.get(k)}
import math
_seen = {}
for e in ECOLES:  # écarte légèrement les points superposés (même coordonnée)
    if not e.get("xy"): continue
    k = tuple(e["xy"]); i = _seen.get(k, 0); _seen[k] = i + 1
    if i:
        a, r = i * 2.4, 0.0012 * math.sqrt(i)
        e["xy"] = [round(e["xy"][0] + r * math.sin(a), 5), round(e["xy"][1] + r * 1.4 * math.cos(a), 5)]
SCH_DATA = json.dumps(ECOLES, ensure_ascii=False).replace("</", "<\\/")
GROUPS = list(dict.fromkeys(e["g"] for e in sorted(ECOLES, key=lambda e: e["g"] != "Universités")))
N_REF = sum(1 for e in ECOLES if e["i"].get("referent"))
ecoles = f'''<section class="page-hero"><div class="wrap"><p class="eyebrow rv">Le challenge des écoles</p><h1 class="rv d1">{len(ECOLES)} ÉCOLES, <em>UNE COUPE</em></h1></div></section>
<section style="padding-top:0"><div class="wrap">
<div class="sch-tools rv">
  <label class="sr" for="sch-q">Chercher une école</label>
  <input id="sch-q" type="search" placeholder="Cherche ton école (ex. INSA, droit, Fermat…)" autocomplete="off">
  <div class="sch-filters" role="group" aria-label="Filtrer par catégorie">
    <button type="button" class="chip on" data-g="">Toutes</button>{"".join(f'<button type="button" class="chip" data-g="{g}">{g}</button>' for g in GROUPS)}
  </div>
  <div class="sch-bar"><p class="sch-count" aria-live="polite"><b id="sch-n">{len(ECOLES)}</b> écoles</p>
  <div class="sch-view" role="group" aria-label="Affichage"><button type="button" class="on" data-v="liste" aria-pressed="true">Liste</button><button type="button" data-v="carte" aria-pressed="false">Carte</button></div></div>
</div>
<div id="sch-map-wrap" class="sch-map-wrap" hidden><div id="sch-map" aria-label="Carte des écoles"></div><p class="sch-map-note">Point clair&nbsp;: emplacement approximatif (centre de la commune).</p></div>
<div id="sch-list" class="sch-list"></div>
<p class="sch-empty" id="sch-empty" hidden>Aucune école ne correspond. Elle n’est pas dans la liste&nbsp;? Pas de souci : choisis «&nbsp;Autre&nbsp;» à l’inscription et écris son nom.</p>
</div></section>
<dialog id="sch-dlg" class="sch-dlg" aria-labelledby="sch-dlg-t"><div id="sch-dlg-in"></div></dialog>
<script id="sch-data" type="application/json">{SCH_DATA}</script>
{CTA}
'''
SCH_HEAD = '''<style>
.sch-tools { display:grid; gap:16px; margin-bottom:28px }
#sch-q { width:100%; padding:16px 20px; font:600 1.05rem var(--body); color:var(--cream); background:rgba(255,255,255,.04); border:1px solid var(--line); border-radius:999px; outline:none }
#sch-q::placeholder { color:var(--muted) }
#sch-q:focus { border-color:var(--pink) }
.sch-filters { display:flex; flex-wrap:wrap; gap:8px }
.sch-filters .chip { cursor:pointer; color:var(--cream); font-family:var(--body) }
.sch-filters .chip.on { background:var(--pink); border-color:var(--pink); color:#fff }
.sch-count { margin:0; color:var(--muted) }
.sch-bar { display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap }
.sch-view { display:inline-flex; padding:4px; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.03) }
.sch-view button { padding:8px 18px; border:0; border-radius:999px; background:transparent; color:var(--cream); font:700 .9rem var(--body); cursor:pointer }
.sch-view button.on { background:var(--pink); color:#fff }
.sch-map-wrap { margin-bottom:10px }
#sch-map { height:min(70vh,640px); border:1px solid var(--line); border-radius:var(--r); overflow:hidden; background:var(--night) }
.sch-map-note { margin:10px 0 0; color:var(--muted); font-size:.82rem }
#sch-map .maplibregl-popup-content { background:var(--night); color:var(--cream); border:1px solid var(--line); border-radius:12px; padding:10px 14px; font:600 .88rem var(--body); box-shadow:0 8px 24px rgba(0,0,0,.4) }
#sch-map .maplibregl-popup-tip { display:none }
.sch-count b { color:var(--pink) }
.sch-grp h3 { font:italic 900 1.6rem/1 var(--display); text-transform:uppercase; margin:34px 0 14px; color:var(--blush) }
.sch-grp ul { list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:10px }
.sch-card { width:100%; height:100%; display:flex; gap:14px; align-items:center; text-align:left; padding:12px 16px; border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.03); color:var(--cream); font:inherit; line-height:1.35; cursor:pointer; transition:border-color .2s, background .2s }
.sch-card:hover { border-color:var(--pink); background:rgba(255,61,151,.06) }
.sch-card .t { flex:1; min-width:0 }
.sch-card .t span { display:block; font-size:.8rem; color:var(--muted); margin-top:3px }
.sch-card .t span.ok { color:var(--pink-2) }
.sch-logo { flex:none; width:44px; height:44px; border-radius:12px; display:grid; place-items:center; overflow:hidden; background:var(--plum); border:1px solid var(--line); font:italic 900 1.05rem/1 var(--display); color:var(--blush); letter-spacing:.02em }
.sch-logo img { width:100%; height:100%; object-fit:contain; background:#fff }
.sch-logo.big { width:84px; height:84px; border-radius:20px; font-size:1.8rem }
.sch-empty { color:var(--muted) }
.sch-dlg { width:min(640px,calc(100% - 32px)); max-height:calc(100% - 48px); padding:0; border:1px solid var(--line); border-radius:var(--r); background:var(--night); color:var(--cream) }
.sch-dlg::backdrop { background:rgba(10,2,6,.75); backdrop-filter:blur(4px) }
#sch-dlg-in { padding:30px; position:relative }
.sch-x { position:absolute; top:16px; right:16px; width:40px; height:40px; border-radius:50%; border:1px solid var(--line); background:transparent; color:var(--cream); font-size:1.3rem; cursor:pointer }
.sch-x:hover { border-color:var(--pink) }
.sch-hd { display:flex; gap:18px; align-items:center; padding-right:44px }
.sch-hd h2 { font:italic 900 clamp(1.6rem,4vw,2.1rem)/1.02 var(--display); text-transform:uppercase; margin:0 }
.sch-hd p { margin:6px 0 0; color:var(--muted); font-size:.9rem }
.sch-sec { margin-top:24px }
.sch-sec h3 { margin:0 0 10px; font-size:.75rem; letter-spacing:.14em; text-transform:uppercase; color:var(--pink) }
.sch-sec p { margin:0 }
.sch-tags { display:flex; flex-wrap:wrap; gap:6px; margin:0; padding:0; list-style:none }
.sch-tags li { padding:6px 12px; border:1px solid var(--line); border-radius:999px; font-size:.82rem; background:rgba(255,255,255,.03) }
.sch-void { padding:20px; border:1px dashed rgba(255,61,151,.5); border-radius:16px; background:rgba(255,61,151,.06) }
.sch-void b { display:block; font-size:1.05rem; margin-bottom:6px }
.sch-void p { color:var(--muted); margin:0 0 14px }
.sch-void .btn { padding:12px 20px; font-size:.9rem }
.sch-dlg a:not(.btn) { color:var(--pink-2) }
@media (max-width:520px) { .sch-grp ul { grid-template-columns:1fr } #sch-dlg-in { padding:22px } .sch-logo.big { width:64px; height:64px; font-size:1.4rem } }
.sch-edit-bt { padding:8px 16px; border:1px dashed var(--pink); border-radius:999px; background:transparent; color:var(--pink); font:700 .85rem var(--body); cursor:pointer }
.sch-edit-bt.on { background:var(--pink); color:#fff; border-style:solid }
.sch-edit-panel { position:absolute; top:12px; left:12px; z-index:5; width:min(340px,calc(100% - 70px)); background:var(--night); color:var(--cream); border:1px solid var(--line); border-radius:14px; padding:14px 16px; box-shadow:0 10px 30px rgba(0,0,0,.45); font-size:.9rem }
.sch-edit-panel b { display:block; margin-bottom:6px }
.sch-edit-panel p { margin:0 0 6px } .sch-edit-panel .m { color:var(--muted); font-size:.8rem }
.sch-edit-panel label { display:block; font-size:.8rem; color:var(--muted); margin:4px 0 6px }
.sch-edit-panel input { display:block; width:100%; margin-top:4px; padding:8px 10px; border-radius:8px; border:1px solid var(--line); background:rgba(255,255,255,.06); color:var(--cream); font:inherit }
.sch-edit-act { display:flex; gap:8px; justify-content:flex-end; margin-top:8px }
.sch-edit-act button { padding:7px 14px; border-radius:999px; border:1px solid var(--line); background:transparent; color:var(--cream); font:700 .85rem var(--body); cursor:pointer }
.sch-edit-act .ok { background:var(--pink); border-color:var(--pink); color:#fff }
.sch-edit-panel .use { margin-left:4px; padding:2px 10px; border-radius:999px; border:1px solid var(--pink); background:transparent; color:var(--pink); font:700 .75rem var(--body); cursor:pointer }
.sch-edit-panel .err { color:#ff8a8a; font-weight:700 }
.sch-pin { width:26px; height:26px; border-radius:50%; background:var(--pink); border:4px solid #fff; box-shadow:0 0 0 4px rgba(255,61,151,.35), 0 4px 12px rgba(0,0,0,.5); cursor:grab }
</style>
'''
SCH_JS = '''<script>
document.addEventListener("DOMContentLoaded", function () {
  var MAIL = "''' + CONTACT_MAIL + '''";
  var data = JSON.parse(document.getElementById("sch-data").textContent);
  var list = document.getElementById("sch-list"), q = document.getElementById("sch-q"),
      n = document.getElementById("sch-n"), empty = document.getElementById("sch-empty"), g = "",
      dlg = document.getElementById("sch-dlg"), din = document.getElementById("sch-dlg-in");
  var byId = {};
  function norm(s) { return s.normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase(); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s == null ? "" : s; return d.innerHTML; }
  var STOP = ["universite", "de", "du", "des", "la", "le", "les", "et", "en", "d", "l", "toulouse", "ut", "ufr", "ecole", "institut", "lycee", "faculte", "general", "generale", "technologique", "polyvalent", "professionnel", "prive", "superieur", "superieure", "nationale", "national", "pierre", "saint", "sainte", "site", "campus"];
  function initials(name) {
    var p = name.split(/[–(]/), base = p.length > 1 && p[0].length < 24 ? p[1] : p[0];
    var BAD = ["UT", "UFR", "UT2J", "INP"], seg = name.split("–").slice(1).join(" "), par = (name.match(/\\(([^)]*)\\)/) || [, ""])[1];
    var acr = [seg, par, name].map(function (x) { return (x.match(/\\b[A-Z][A-Z0-9]{1,7}\\b/g) || []).filter(function (a) { return BAD.indexOf(a) < 0; })[0]; }).filter(Boolean)[0];
    if (acr) return acr.length > 5 ? acr.slice(0, 4) : acr;
    var w = norm(base).replace(/[^a-z0-9 ]/g, " ").split(/\\s+/).filter(function (x) { return x && STOP.indexOf(x) < 0; });
    return ((w[0] || "?")[0] + (w[1] ? w[1][0] : "")).toUpperCase();
  }
  function logo(e, big) {
    var c = "sch-logo" + (big ? " big" : "");
    return e.i.logo ? '<span class="' + c + '"><img src="' + esc(e.i.logo) + '" alt="Logo ' + esc(e.n) + '" loading="lazy"></span>'
                    : '<span class="' + c + '" aria-hidden="true">' + esc(initials(e.n)) + "</span>";
  }
  data.forEach(function (e) { e.k = norm(e.n + " " + e.c + " " + e.g + " " + e.f.join(" ")); byId[e.id] = e; });
  var order = []; data.forEach(function (e) { if (order.indexOf(e.g) < 0) order.push(e.g); });
  order.sort(function (a, b) { return (a === "Universités" ? -1 : b === "Universités" ? 1 : 0); });
  function render() {
    var t = norm(q.value.trim()).split(/\\s+/).filter(Boolean), html = "", count = 0;
    order.forEach(function (grp) {
      if (g && grp !== g) return;
      var items = data.filter(function (e) { return e.g === grp && t.every(function (w) { return e.k.indexOf(w) >= 0; }); })
                      .sort(function (a, b) { return a.n.localeCompare(b.n, "fr"); });
      if (!items.length) return;
      count += items.length;
      html += '<div class="sch-grp"><h3>' + esc(grp) + ' <small style="font-size:.9rem;color:var(--muted)">(' + items.length + ')</small></h3><ul>' +
        items.map(function (e) {
          var ok = !!e.i.referent;
          return '<li><button type="button" class="sch-card" data-id="' + e.id + '">' + logo(e) +
            '<span class="t">' + esc(e.n) + '<span' + (ok ? ' class="ok">✓ Référent : ' + esc(e.i.referent) : ">" + esc(e.c)) + "</span></span></button></li>";
        }).join("") + "</ul></div>";
    });
    shown = data.filter(function (e) { return (!g || e.g === g) && t.every(function (w) { return e.k.indexOf(w) >= 0; }); });
    list.innerHTML = html; n.textContent = count; empty.hidden = count > 0 || view === "carte"; updateMap();
  }
  function open(e) {
    var i = e.i, h = '<button type="button" class="sch-x" aria-label="Fermer">×</button>' +
      '<div class="sch-hd">' + logo(e, true) + '<div><h2 id="sch-dlg-t">' + esc(e.n) + "</h2><p>" + esc([e.g, e.s, e.c].filter(Boolean).join(" · ")) + "</p></div></div>";
    if (i.referent || i.texte || i.instagram) {
      if (i.texte) h += '<div class="sch-sec"><p>' + esc(i.texte) + "</p></div>";
      if (i.referent) h += '<div class="sch-sec"><h3>Référent Stud’N Run</h3><p>' + esc(i.referent) + "</p></div>";
      if (i.instagram) { var ig = i.instagram.replace(/^@/, ""); h += '<div class="sch-sec"><h3>Instagram</h3><p><a href="https://instagram.com/' + encodeURIComponent(ig) + '" target="_blank" rel="noopener">@' + esc(ig) + "</a></p></div>"; }
    } else {
      var sub = encodeURIComponent("Référent Stud'N Run – " + e.n);
      h += '<div class="sch-sec sch-void"><b>Aucune info sur cette école pour l’instant.</b>' +
        "<p>Tu es au BDE, au BDS ou motivé pour représenter ton école&nbsp;? Envoie-nous le nom d’un référent et votre logo&nbsp;: on complète la fiche.</p>" +
        '<a class="btn" href="mailto:' + MAIL + "?subject=" + sub + '">Devenir référent <span class="arr">→</span></a></div>';
    }
    if (e.f.length) h += '<div class="sch-sec"><h3>Formations après le bac (Parcoursup)</h3><ul class="sch-tags">' + e.f.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + "</ul></div>";
    var adr = [e.a].concat((e.x2 || []).map(function (s) { return s.a; })).filter(Boolean);
    if (adr.length) h += '<div class="sch-sec"><h3>' + (adr.length > 1 ? "Sites" : "Adresse") + "</h3>" + adr.map(function (a) { return "<p>" + esc(a) + "</p>"; }).join("") + "</div>";
    if (e.w) h += '<div class="sch-sec"><h3>Site de l’école</h3><p><a href="' + esc(/^https?:/.test(e.w) ? e.w : "https://" + e.w) + '" target="_blank" rel="noopener">' + esc(e.w.replace(/^https?:\\/\\//, "").replace(/\\/$/, "")) + "</a></p></div>";
    din.innerHTML = h;
    din.querySelector(".sch-x").addEventListener("click", function () { dlg.close(); });
    dlg.showModal(); din.querySelector(".sch-x").focus();
  }
  list.addEventListener("click", function (ev) { var b = ev.target.closest(".sch-card"); if (b) open(byId[b.getAttribute("data-id")]); });
  dlg.addEventListener("click", function (ev) { if (ev.target === dlg) dlg.close(); });
  var view = "liste", map = null, mapReady = false, shown = data;
  var wrapMap = document.getElementById("sch-map-wrap");
  function geo() {
    var f = [];
    shown.forEach(function (e) {
      if (e.xy) f.push({ type: "Feature", properties: { id: e.id, n: e.n, ap: e.ap }, geometry: { type: "Point", coordinates: [e.xy[1], e.xy[0]] } });
      (e.x2 || []).forEach(function (s) { f.push({ type: "Feature", properties: { id: e.id, n: e.n, ap: 0 }, geometry: { type: "Point", coordinates: [s.xy[1], s.xy[0]] } }); });
    });
    return { type: "FeatureCollection", features: f };
  }
  function updateMap() { if (mapReady) map.getSource("ec").setData(geo()); }
  function loadLib(cb) {
    if (window.maplibregl) return cb();
    var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css"; document.head.appendChild(l);
    var sc = document.createElement("script"); sc.src = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"; sc.onload = cb; document.head.appendChild(sc);
  }
  function initMap() {
    map = new maplibregl.Map({ container: "sch-map", style: "https://tiles.openfreemap.org/styles/liberty", center: [1.444, 43.6], zoom: 11.2, attributionControl: { compact: true }, cooperativeGestures: true });
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    map.on("load", function () {
      map.addSource("ec", { type: "geojson", data: geo(), cluster: true, clusterRadius: 38, clusterMaxZoom: 15 });
      map.addLayer({ id: "cl", type: "circle", source: "ec", filter: ["has", "point_count"], paint: { "circle-color": "#ff3d97", "circle-opacity": .92, "circle-stroke-width": 3, "circle-stroke-color": "#ffc2de",
        "circle-radius": ["step", ["get", "point_count"], 16, 10, 21, 30, 27] } });
      map.addLayer({ id: "cl-n", type: "symbol", source: "ec", filter: ["has", "point_count"], layout: { "text-field": ["get", "point_count_abbreviated"], "text-size": 13, "text-font": ["Noto Sans Bold"] }, paint: { "text-color": "#fff" } });
      map.addLayer({ id: "pt", type: "circle", source: "ec", filter: ["!", ["has", "point_count"]], paint: {
        "circle-color": ["case", ["==", ["get", "ap"], 1], "#ffc2de", "#ff3d97"], "circle-radius": 8, "circle-stroke-width": 2.5, "circle-stroke-color": "#14040c" } });
      map.on("click", "cl", function (ev) {
        var f = map.queryRenderedFeatures(ev.point, { layers: ["cl"] })[0];
        map.getSource("ec").getClusterExpansionZoom(f.properties.cluster_id).then(function (z) { map.easeTo({ center: f.geometry.coordinates, zoom: z + .3 }); });
      });
      map.on("click", "pt", function (ev) { open(byId[ev.features[0].properties.id]); });
      var pop = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 12 });
      map.on("mouseenter", "pt", function (ev) { map.getCanvas().style.cursor = "pointer"; pop.setLngLat(ev.features[0].geometry.coordinates).setText(ev.features[0].properties.n).addTo(map); });
      map.on("mouseleave", "pt", function () { map.getCanvas().style.cursor = ""; pop.remove(); });
      map.on("mouseenter", "cl", function () { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", "cl", function () { map.getCanvas().style.cursor = ""; });
      mapReady = true; updateMap();
    });
  }
  function setView(v) {
    view = v;
    document.querySelectorAll(".sch-view button").forEach(function (b) { var on = b.getAttribute("data-v") === v; b.classList.toggle("on", on); b.setAttribute("aria-pressed", String(on)); });
    list.hidden = v !== "liste"; wrapMap.hidden = v !== "carte";
    if (v === "carte") { empty.hidden = true; if (!map) loadLib(initMap); else map.resize(); }
    else empty.hidden = shown.length > 0;
    try { history.replaceState(null, "", v === "carte" ? "#carte" : location.pathname); } catch (e) {}
  }
  document.querySelectorAll(".sch-view button").forEach(function (b) { b.addEventListener("click", function () { setView(b.getAttribute("data-v")); }); });
  q.addEventListener("input", render);
  document.querySelectorAll(".sch-filters .chip").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".sch-filters .chip").forEach(function (x) { x.classList.toggle("on", x === b); });
      g = b.getAttribute("data-g"); render();
    });
  });
  render();
  if (location.hash === "#carte") setView("carte");

  /* Mode édition des positions : n'apparaît que sur l'ordinateur de l'équipe, quand la page est servie par build/ecoles/editeur.py */
  if (!/^(localhost|127\\.0\\.0\\.1)$/.test(location.hostname)) return;
  fetch("/api/ping").then(function (r) { return r.ok ? r.json() : null; }).then(function (ok) { if (ok && ok.editeur) setupEdit(); }).catch(function () {});
  function setupEdit() {
    var edit = false, sel = null, selK = 0, mk = null, moved = null;
    /* site k d'une école : 0 = site principal, 1, 2… = autres sites (champ x2) */
    function sXY(e, k) { return k ? e.x2[k - 1].xy : e.xy; }
    function sA(e, k) { return k ? e.x2[k - 1].a : e.a; }
    function sN(e, k) { return e.x2 && e.x2.length ? e.n + " · site " + (k + 1) + "/" + (e.x2.length + 1) : e.n; }
    var bt = document.createElement("button"); bt.type = "button"; bt.className = "sch-edit-bt"; bt.textContent = "✎ Déplacer les points";
    document.querySelector(".sch-bar").appendChild(bt);
    var pn = document.createElement("div"); pn.className = "sch-edit-panel"; pn.hidden = true; wrapMap.style.position = "relative"; wrapMap.appendChild(pn);
    function eGeo() {
      var f = [];
      data.forEach(function (e) {
        [e.xy].concat((e.x2 || []).map(function (s) { return s.xy; })).forEach(function (xy, k) {
          if (xy && !(sel && e.id === sel.id && k === selK)) f.push({ type: "Feature", properties: { id: e.id, n: sN(e, k), k: k }, geometry: { type: "Point", coordinates: [xy[1], xy[0]] } });
        });
      });
      return { type: "FeatureCollection", features: f };
    }
    function layers() {
      if (map.getSource("ece")) return;
      map.addSource("ece", { type: "geojson", data: eGeo() });
      map.addLayer({ id: "pt-e", type: "circle", source: "ece", layout: { visibility: "none" }, paint: { "circle-color": "#ff3d97", "circle-radius": 7, "circle-stroke-width": 2, "circle-stroke-color": "#fff" } });
      map.addLayer({ id: "pt-e-n", type: "symbol", source: "ece", minzoom: 14, layout: { visibility: "none", "text-field": ["get", "n"], "text-size": 11, "text-offset": [0, 1.2], "text-anchor": "top", "text-font": ["Noto Sans Regular"], "text-max-width": 12 }, paint: { "text-color": "#14040c", "text-halo-color": "#fff", "text-halo-width": 1.5 } });
      map.on("click", "pt-e", function (ev) { var p = ev.features[0].properties; pick(byId[p.id], +p.k || 0); });
      map.on("mouseenter", "pt-e", function () { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", "pt-e", function () { map.getCanvas().style.cursor = ""; });
    }
    function refresh() { if (map.getSource("ece")) map.getSource("ece").setData(eGeo()); updateMap(); }
    function msg(h) { pn.innerHTML = h; pn.hidden = false; }
    function idle() { msg("<b>Mode édition</b><p>Clique sur une école pour la sélectionner, puis glisse son point à la bonne place.</p>"); }
    function toggle(on) {
      edit = on; bt.classList.toggle("on", on); bt.textContent = on ? "✓ Terminer l’édition" : "✎ Déplacer les points";
      if (on) setView("carte");
      var go = function () {
        layers();
        ["cl", "cl-n", "pt"].forEach(function (l) { map.setLayoutProperty(l, "visibility", on ? "none" : "visible"); });
        ["pt-e", "pt-e-n"].forEach(function (l) { map.setLayoutProperty(l, "visibility", on ? "visible" : "none"); });
        if (map.cooperativeGestures) map.cooperativeGestures[on ? "disable" : "enable"]();
        if (!on) cancel(); else idle();
        pn.hidden = !on;
      };
      if (mapReady) go(); else { var t = setInterval(function () { if (mapReady) { clearInterval(t); go(); } }, 150); }
    }
    bt.addEventListener("click", function () { toggle(!edit); });
    function cancel() { if (mk) mk.remove(); mk = null; sel = null; selK = 0; moved = null; if (map) refresh(); if (edit) idle(); }
    function pick(e, k) {
      k = k || 0; cancel(); sel = e; selK = k; refresh();
      var xy = sXY(e, k), ea = sA(e, k), nm = sN(e, k);
      var el = document.createElement("div"); el.className = "sch-pin";
      mk = new maplibregl.Marker({ element: el, draggable: true }).setLngLat([xy[1], xy[0]]).addTo(map);
      msg("<b>" + esc(nm) + "</b><p>Glisse le point rose à la bonne place.</p><p class=\\"m\\">Adresse actuelle : " + esc(ea || "aucune") + "</p>" +
          '<div class="sch-edit-act"><button type="button" class="x">Annuler</button></div>');
      pn.querySelector(".x").addEventListener("click", cancel);
      mk.on("dragend", function () {
        var p = mk.getLngLat(); moved = { lat: +p.lat.toFixed(6), lon: +p.lng.toFixed(6) };
        msg("<b>" + esc(nm) + "</b><p class=\\"m\\">Recherche de l’adresse…</p>");
        fetch("/api/reverse?lat=" + moved.lat + "&lon=" + moved.lon).then(function (r) { return r.json(); }).then(function (rv) {
          if (!sel || sel.id !== e.id || selK !== k) return;
          var dLat = (moved.lat - xy[0]) * 111320, dLon = (moved.lon - xy[1]) * 111320 * Math.cos(xy[0] * Math.PI / 180);
          var dist = Math.round(Math.sqrt(dLat * dLat + dLon * dLon));
          /* ancienne adresse gardée par défaut si elle existe et que le point a bougé de moins de 300 m (ou si aucune adresse n'est trouvée) */
          var keep = !!ea && (dist < 300 || !rv.adresse);
          moved.commune = keep ? e.c : (rv.commune || e.c);
          var sug = rv.adresse && keep && rv.adresse !== ea;
          msg("<b>" + esc(nm) + "</b><label>Adresse<input type=\\"text\\" class=\\"ad\\"></label>" +
              (sug ? '<p class="m">Adresse trouvée à cet endroit : ' + esc(rv.adresse) + ' <button type="button" class="use">utiliser</button></p>' : "") +
              "<p class=\\"m\\">Point déplacé de " + dist + " m · " + esc(moved.commune) + (keep ? " · ancienne adresse gardée" : (rv.distance > 60 ? " · adresse la plus proche à " + rv.distance + " m, vérifie-la" : "")) + "</p>" +
              '<div class="sch-edit-act"><button type="button" class="x">Annuler</button><button type="button" class="ok">Valider</button></div>');
          pn.querySelector(".ad").value = keep ? ea : (rv.adresse || "");
          if (sug) pn.querySelector(".use").addEventListener("click", function () { pn.querySelector(".ad").value = rv.adresse; moved.commune = rv.commune || e.c; this.parentNode.remove(); });
          pn.querySelector(".x").addEventListener("click", cancel);
          pn.querySelector(".ok").addEventListener("click", function () { save(e, k); });
        });
      });
    }
    function save(e, k) {
      var b = pn.querySelector(".ok"); b.disabled = true; b.textContent = "Enregistrement…";
      var body = { id: e.id, site: k, lat: moved.lat, lon: moved.lon, adresse: pn.querySelector(".ad").value.trim(), commune: moved.commune };
      fetch("/api/save", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); }).then(function (res) {
          if (!res.ok) { b.disabled = false; b.textContent = "Valider"; alertMsg(res.error || "Erreur"); return; }
          if (k) { e.x2[k - 1] = { xy: [body.lat, body.lon], a: body.adresse || null }; }
          else { e.xy = [body.lat, body.lon]; e.a = body.adresse || null; e.c = body.commune || e.c; e.ap = 0; }
          if (mk) mk.remove(); mk = null; sel = null; selK = 0; refresh();
          msg("<b>✓ Enregistré</b><p>" + esc(sN(e, k)) + "</p><p class=\\"m\\">" + esc(body.adresse || "") + " — Sheet et site mis à jour.</p>");
          setTimeout(function () { if (edit && !sel) idle(); }, 3500);
        }).catch(function () { b.disabled = false; b.textContent = "Valider"; alertMsg("Le serveur d’édition ne répond pas."); });
    }
    function alertMsg(t) { var p = document.createElement("p"); p.className = "err"; p.textContent = t; pn.appendChild(p); }
    var oldOpen = open;
    open = function (e) { if (edit) { if (mapReady) pick(e); return; } oldOpen(e); };
  }
});
</script>
'''

MAP_HEAD = '<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css">\n'
MAP_JS = '<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js" defer></script>\n<script src="parcours-3d.js" defer></script>\n'
D = "Stud’N Run, course étudiante à Toulouse : 5 et 10 km au départ de la Place Saint-Pierre."
PAGES = {
    "index.html": ("Stud’N Run · Course étudiante Toulouse", index, "", ""),
    "parcours.html": ("Parcours · Stud’N Run", parcours, MAP_HEAD, MAP_JS),
    "ecoles.html": ("Écoles invitées · Stud’N Run", ecoles, SCH_HEAD, SCH_JS),
    "horaires.html": ("Horaires · Stud’N Run", horaires, "", ""),
    "infos-pratiques.html": ("Infos pratiques · Stud’N Run", infos, "", ""),
    "inscriptions.html": ("Inscriptions · Stud’N Run", inscriptions, "", ""),
    "partenaires.html": ("Partenaires · Stud’N Run", partenaires, "", ""),
    "actualites.html": ("Actualités · Stud’N Run", actualites, "", ""),
    "benevoles.html": ("Bénévoles · Stud’N Run", benevoles, "", ""),
    "contact.html": ("Contact · Stud’N Run", contact, "", ""),
    "mentions-legales.html": ("Mentions légales · Stud’N Run", mentions, "", ""),
    "confidentialite.html": ("Confidentialité · Stud’N Run", confidentialite, "", ""),
    "association.html": ("Association · Stud’N Run", association, "", ""),
}
for slug, (t, body, h, s) in PAGES.items():
    (DIST / slug).write_text(page(slug, t, D, body, h, s))
print("ok", len(PAGES), "pages")

