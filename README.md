# SiraWeb - Agence Web Burkina Faso

Site web ultra-moderne 2026 pour l'agence web SiraWeb au Burkina Faso. Projet Django avec templates, design premium, animations performantes et SEO optimisé.

## 🚀 Caractéristiques

- **Design Premium 2026** : Interface moderne, mobile-first, animations fluides
- **Performance** : Optimisé pour 60fps, lazy loading, code modulaire
- **SEO Technique** : Meta tags, OpenGraph, Schema.org, sitemap dynamique
- **Accessibilité** : Navigation clavier, ARIA, contrastes WCAG
- **Animations** : Scroll reveal, parallax léger, magnetic buttons, smooth scroll
- **Vanilla JS** : Aucune dépendance JavaScript, code optimisé
- **CSS Moderne** : Variables CSS, fluid typography, grid/flex

## 📋 Prérequis

- Python 3.10+
- pip
- virtualenv (recommandé)

## 🛠️ Installation

### 1. Cloner le projet

```bash
cd agence
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configuration de l'environnement

Créez un fichier `.env` à la racine du projet (copiez `.env.example` si disponible) :

```env
SECRET_KEY=votre-secret-key-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SITE_DOMAIN=http://localhost:8000
```

Générez une SECRET_KEY avec :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Migrations de la base de données

```bash
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 8. Charger les données de démonstration (optionnel)

```bash
python manage.py loaddata fixtures/initial_data.json
```

Ou créez manuellement des données via l'admin Django.

### 9. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 10. Lancer le serveur de développement

```bash
python manage.py runserver
```

Le site sera accessible sur `http://localhost:8000`

L'interface d'administration Django sera accessible sur `http://localhost:8000/admin`

## 📁 Structure du Projet

```
siraweb/
├── core/                    # Application principale
│   ├── models.py           # Modèles (Article, Service, Contact, etc.)
│   ├── views.py            # Vues
│   ├── urls.py             # URLs de l'app
│   ├── forms.py            # Formulaires
│   ├── admin.py            # Configuration admin Django
│   ├── sitemaps.py         # Sitemaps dynamiques
│   └── context_processors.py
├── siraweb/                 # Configuration du projet
│   ├── settings.py         # Paramètres Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI config
├── templates/               # Templates HTML
│   ├── base.html           # Template de base
│   ├── partials/           # Partials (navbar, footer)
│   └── core/               # Templates des pages
├── static/                  # Fichiers statiques
│   ├── css/
│   │   └── main.css        # Stylesheet principal
│   ├── js/
│   │   └── main.js         # JavaScript principal
│   └── images/             # Images
├── media/                   # Fichiers uploadés (créé automatiquement)
├── manage.py
├── requirements.txt
└── README.md
```

## 🎨 Pages Disponibles

- **Accueil** (`/`) : Hero avec slider, services, processus, portfolio, témoignages
- **Services** (`/services/`) : Liste des services
- **Détail Service** (`/services/<slug>/`) : Page détaillée pour chaque service
- **À Propos** (`/agence/`) : Présentation de l'agence
- **Équipe** (`/agence/equipe/`) : Présentation de l'équipe
- **Contact** (`/contact/`) : Formulaire de contact
- **Blog** (`/blog/`) : Liste des articles
- **Détail Article** (`/blog/<slug>/`) : Article de blog
- **SEO Ouagadougou** (`/seo-ouagadougou/`) : Landing page SEO locale
- **SEO Bobo-Dioulasso** (`/seo-bobo-dioulasso/`) : Landing page SEO locale

## 🔧 Configuration Admin

Accédez à l'admin Django pour gérer :

- **Articles** : Créer, modifier, publier des articles de blog
- **Services** : Gérer les services proposés
- **Messages de contact** : Voir et gérer les messages reçus
- **Équipe** : Ajouter des membres de l'équipe
- **Témoignages** : Gérer les témoignages clients
- **Partenaires** : Ajouter des logos de partenaires
- **Catégories & Tags** : Gérer les catégories et tags du blog

## 📝 Créer des Données de Démonstration

### Via l'Admin Django

1. Connectez-vous à `/admin`
2. Créez des **Services** (8 services prévus dans les choix)
3. Créez des **Articles** de blog avec catégories et tags
4. Ajoutez des **Membres de l'équipe**
5. Ajoutez des **Témoignages** clients
6. Ajoutez des **Partenaires**

### Via le Shell Django

```bash
python manage.py shell
```

Exemple pour créer un service :

```python
from core.models import Service

service = Service.objects.create(
    name='vitrine',
    short_description='Création de sites vitrine modernes et performants',
    full_description='Description complète du service...',
    meta_title='Création de Site Vitrine - SiraWeb',
    meta_description='Service de création de sites vitrine au Burkina Faso',
    order=1,
    active=True
)
```

## 🚀 Déploiement en Production

### 1. Configuration Production

Modifiez `.env` :

```env
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
SECRET_KEY=votre-secret-key-production
SITE_DOMAIN=https://votre-domaine.com
```

### 2. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 3. Configuration serveur web (Nginx + Gunicorn)

#### Installation Gunicorn

```bash
pip install gunicorn
```

#### Fichier Gunicorn (`gunicorn_config.py`)

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
```

#### Lancer Gunicorn

```bash
gunicorn -c gunicorn_config.py siraweb.wsgi:application
```

#### Configuration Nginx (`/etc/nginx/sites-available/siraweb`)

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    # Redirection HTTPS (optionnel)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Static files
    location /static/ {
        alias /path/to/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/project/media/;
        expires 7d;
    }

    # Django app
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 4. Systemd Service (optionnel)

Créez `/etc/systemd/system/siraweb.service` :

```ini
[Unit]
Description=SiraWeb Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py siraweb.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer le service :

```bash
sudo systemctl enable siraweb
sudo systemctl start siraweb
```

## ✅ Checklist Qualité

### SEO

- [ ] Vérifier les meta titles (60-65 caractères)
- [ ] Vérifier les meta descriptions (150-160 caractères)
- [ ] Tester le sitemap.xml : `/sitemap.xml`
- [ ] Vérifier robots.txt : `/robots.txt`
- [ ] Valider les Schema.org JSON-LD (Google Rich Results Test)
- [ ] Vérifier les balises OpenGraph (Facebook Debugger)
- [ ] Vérifier les Twitter Cards (Twitter Card Validator)
- [ ] Tester les URLs canoniques
- [ ] Vérifier les H1 uniques sur chaque page
- [ ] Optimiser les images (compression, alt text, dimensions)

### Performance

- [ ] Test Lighthouse (score > 90)
  ```bash
  # Chrome DevTools > Lighthouse
  # Ou en ligne : PageSpeed Insights
  ```
- [ ] Vérifier le lazy loading des images
- [ ] Minifier CSS/JS (optionnel, pour production)
- [ ] Optimiser les fonts (preconnect, display=swap)
- [ ] Vérifier les Core Web Vitals
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1

### Accessibilité

- [ ] Test avec lecteur d'écran (NVDA/JAWS)
- [ ] Navigation au clavier (Tab, Enter, Esc)
- [ ] Vérifier les contrastes (WCAG AA minimum)
- [ ] Tester avec `prefers-reduced-motion`
- [ ] Vérifier les attributs ARIA
- [ ] Tester les formulaires (labels, erreurs)

### Fonctionnalités

- [ ] Tester le formulaire de contact
- [ ] Vérifier l'envoi d'emails (console backend en dev)
- [ ] Tester la navigation mobile (drawer menu)
- [ ] Vérifier les animations (scroll reveal, parallax)
- [ ] Tester le slider de témoignages
- [ ] Vérifier la pagination du blog
- [ ] Tester les pages 404 et 500

### Responsive

- [ ] Tester sur mobile (360px, 375px, 414px)
- [ ] Tester sur tablette (768px, 1024px)
- [ ] Tester sur desktop (1280px, 1920px)
- [ ] Vérifier le menu mobile
- [ ] Tester l'affichage des grilles

## 🧪 Tests

### Tests basiques (smoke tests)

```bash
python manage.py test core
```

### Tests manuels recommandés

1. Créer un article de blog et vérifier l'affichage
2. Envoyer un message de contact
3. Tester toutes les pages
4. Vérifier les liens internes
5. Tester sur différents navigateurs

## 📚 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [W3C Validator](https://validator.w3.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Schema.org](https://schema.org/)

## 🐛 Dépannage

### Erreur "No module named 'decouple'"

```bash
pip install python-decouple
```

### Erreur de migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### Fichiers statiques non chargés

```bash
python manage.py collectstatic --noinput
```

Vérifiez que `STATIC_URL` et `STATIC_ROOT` sont correctement configurés dans `settings.py`.

### Erreur 404 sur les pages

Vérifiez que toutes les URLs sont correctement configurées dans `core/urls.py` et `siraweb/urls.py`.

## 📄 Licence

Ce projet est propriétaire de SiraWeb.

## 👥 Support

Pour toute question ou problème, contactez l'équipe SiraWeb.

---

**Développé avec ❤️ pour SiraWeb - Agence Web Burkina Faso**
