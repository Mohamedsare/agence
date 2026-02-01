Tu es un Senior Full-Stack Engineer + UI/UX Designer (20 ans d’expertise) + SEO Technical Lead.
Ta mission : générer un projet complet Django (templates) pour le site web ultra-moderne 2026 d’une agence web au Burkina Faso nommée “SiraWeb”.

Objectif :
- Site vitrine premium “waouh”, mobile-first, ultra soigné (niveau agence internationale).
- Animations et effets scroll partout, mais performance-friendly (60 fps, pas de jank).
- SEO on-page + technique : être #1 sur “agence web Burkina Faso”, “création site web Ouagadougou”, “SEO Ouagadougou”, “agence web Bobo-Dioulasso”, “référencement naturel Burkina”, etc.
- Tech : Django + Django Templates + HTML/CSS/JS vanilla (AUCUN framework CSS).
- Code propre, structuré, maintenable, accessible, rapide.

Contraintes fortes :
1) Pas de Tailwind, pas de Bootstrap, pas de framework CSS.
2) JS vanilla uniquement (IntersectionObserver, requestAnimationFrame, passive listeners, etc.).
3) Animations scroll “waouh” : reveal, parallax léger, sticky sections, progress indicator, magnetic buttons, smooth anchor scroll, etc. MAIS avec fallback “prefers-reduced-motion”.
4) Mobile-first : design impeccable sur 360px, puis tablette, desktop.
5) SEO technique : meta, OpenGraph, Twitter cards, canonical, sitemap.xml, robots.txt, schema.org (LocalBusiness/Organization/Service), pages “services” optimisées.
6) Performance : lazy-load images, responsive images, preconnect fonts, CSS critical minimal, JS modulaire, minifier friendly.
7) Accessibilité : contrastes, focus visible, navigation clavier, aria, headings cohérents.

Livrables attendus :
- Un projet Django complet exécutable en local, avec un README précis.
- Une app principale “core” (ou “web”) contenant pages, templates, static, forms.
- Un design system maison (tokens CSS, composants réutilisables).
- Pages :
  - Accueil
  - Services (page liste) + pages détails :
      * Création de site vitrine
      * Site e-commerce
      * Site institutionnel
      * Landing pages
      * Refonte UI/UX
      * SEO naturel
      * SEA (Google Ads)
      * Maintenance & hébergement
  - Agence (menu) :
      * À propos
      * Équipe
  - Contact (formulaire)
  - Blog ( recommandé SEO) :
      * Liste des articles
      * Détail article (slug)
      * Catégories/Tags simples
- Composants UI :
  - Navbar ultra moderne (desktop + mobile drawer) avec sous-menu “Agence”.
  - Hero section “waouh” (gradient, noise subtil, spotlight, animated shapes légères).
  - Sections services en cartes premium (hover, tilt léger, micro-interactions).
  - Section “Process” (timeline / steps).
  - Section “Portfolio / Réalisations” (même si fictif au départ, structure prête).
  - Section “Testimonials” (slider vanilla).
  - Footer complet (contacts, liens, réseaux).
  -Retours client
  -Nos partenaires
- SEO local :
  - Données de localisation (Ouagadougou, Bobo-Dioulasso), textes optimisés sans bourrage de mots-clés.
  - Une page “SEO Ouagadougou” et “SEO Bobo-Dioulasso” (landing pages locales) si pertinent.
- Fonctionnalités Django :
  - Vues class-based ou function-based propres.
  - URLs propres, slugs.
  - Formulaire contact (nom, email, téléphone, entreprise, budget, message) avec validation.
  - Envoi email (console backend par défaut) + messages Django.
  - Modèles Blog (Article, Category, Tag) + admin.
  - Context processors si nécessaire (navigation).
- Fichiers techniques :
  - sitemap.xml dynamique (Django sitemap framework)
  - robots.txt
  - pages 404/500 stylées
  - manifest.json (PWA light) + favicon placeholders
  - security headers basiques (dans Django settings + exemples Nginx dans README)
- Qualité :
  - HTML sémantique (header/main/section/footer)
  - Une architecture CSS moderne : variables CSS, clamp(), fluid typography, grid/flex, container queries si utile.
  - Animations : IntersectionObserver + classes CSS, et quelques modules JS (navigation, slider, scroll progress, parallax léger).
  - Aucun code mort. Nommage clair. Commentaires utiles.

Branding SiraWeb (à intégrer) :
- Nom : SiraWeb
- Positionnement : Agence Web au Burkina Faso – sites sur mesure, coût maîtrisé, SEO-friendly, interfaces modernes 2026.
- Ton :  crédible, orienté résultats.
- Palette proposée (tu peux l’améliorer) :
    --color-primary:  #F1F5F9;   
    --color-secondary:  #0F172A;     
    --color-accent: #F97316; 
    -- cree le reste logiquement
- Typo :
  - Utiliser des polices web sûres ou Google Fonts (ex: Plus Jakarta Sans / Inter) mais optimiser performance (preconnect, display=swap).
- Microcopy à produire (en français) : titres, sous-titres, CTA, descriptions de services, FAQ, etc.

Structure du projet :
- siraw eb/ (project)
- core/ (app)
- templates/ (base, partials, pages)
- static/ (css, js, images)
- media/ (si besoin)
- manage.py

Exigences de navigation :
- Menu : Accueil, Services, Agence (dropdown : À propos, 
-Le NavBar Confondut avec le hero background slider, et le navbar doit avoir un
Équipe), Contact
- CTA button “Demander un devis” visible.
- Mobile menu : drawer plein écran avec animations.

Exigences design (ultra moderne 2026) :
- Layout : grandes respirations, grilles cohérentes, coins arrondis premium, ombres soft.
- Effets : 
  - smooth anchor scrolling
  - scroll reveal (fade+translate)
  - parallax léger sur shapes dans hero
  - sticky progress bar (haut de page)
  - underline animée sur liens
  - boutons “magnetic” léger sur desktop
  - cards hover tilt léger (CSS transform) desktop only
- Respecter prefers-reduced-motion : si activé, désactiver animations lourdes.

SEO détaillé :
- Chaque page : title unique (60-65 chars), meta description (150-160), H1 unique, H2/H3 structurés.
- OpenGraph + Twitter meta.
- Canonical.
- Schema JSON-LD :
  - Organization/LocalBusiness (SiraWeb)
  - Service pour pages services
  - BlogPosting pour articles
- Contenu :
  - Accueil cible “Agence web Burkina Faso” + localités.
  - Services pages avec sections “Pour qui”, “Livrables”, “Délais”, “FAQ”, “CTA”.
  - Ajoute des FAQ avec balisage FAQPage schema si pertinent.
- Performance SEO :
  - images optimisées (width/height, loading=lazy)
  - pas de CLS (réserver dimensions)
  - minifier-friendly

Ce que tu dois produire maintenant :
1) Générer tous les fichiers (Django settings, urls, templates, static, models blog, forms contact, sitemaps, robots).
2) Remplir le contenu texte en français (professionnel, pas générique, orienté résultats au Burkina).
3) Implémenter toutes les animations en JS vanilla (modules) + CSS.
4) Fournir README : installation, runserver, création superuser, structure, et checklist SEO + déploiement (Gunicorn+Nginx).
5) Prévoir données de démonstration (fixtures ou simple script) pour 6 articles blog.

Règles de génération :
- Donne du code complet, pas des extraits.
- Assure-toi que le projet démarre sans erreur.
- Utilise Django 4.2+ ou 5.x.
- Utilise un fichier .env optionnel (SECRET_KEY, DEBUG, ALLOWED_HOSTS) + python-decouple si tu veux, sinon simple settings.
- Respecte l’architecture propre : base.html + partials (navbar, footer).
- Tous les liens fonctionnent (urls).
- Ajoute des tests minimalistes si possible (smoke tests).
- Le design doit être vraiment premium.

À la fin :
- Liste les commandes pour exécuter.
- Donne une checklist “qualité” (SEO, perf, accessibilité) et comment vérifier (Lighthouse, etc.)

Commence maintenant en créant l’arborescence et les fichiers.
