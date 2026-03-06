# 🚀 Guide d'Installation en Production

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Serveur web (Nginx recommandé)
- Base de données (PostgreSQL recommandé pour production)

---

## 🔧 Installation

### 1. Cloner ou transférer le projet sur le serveur

```bash
cd /chemin/vers/votre/projet
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env
nano .env  # ou votre éditeur préféré
```

**Important :** Remplissez au minimum :
- `SECRET_KEY` (générez-en une nouvelle)
- `DEBUG=False`
- `ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com`
- `SITE_DOMAIN=https://votre-domaine.com`

### 5. Générer une SECRET_KEY

```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez le résultat dans votre fichier `.env` pour `SECRET_KEY`.

### 6. Appliquer les migrations

```bash
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 8. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 9. Restaurer vos données (FAQ, etc.)

```bash
# Si vous avez une sauvegarde
python manage.py loaddata faqs_backup.json

# OU utiliser le script
python backup_faqs.py import
```

### 10. Copier les fichiers médias

```bash
# Copier le dossier media/ sur le serveur
# Assurez-vous que les permissions sont correctes
chmod -R 755 media/
```

---

## 🌐 Configuration du serveur web (Nginx)

### Exemple de configuration Nginx

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    
    # Redirection HTTPS (recommandé)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com www.votre-domaine.com;
    
    # Certificat SSL
    ssl_certificate /chemin/vers/certificat.crt;
    ssl_certificate_key /chemin/vers/cle.privee.key;
    
    # Fichiers statiques
    location /static/ {
        alias /chemin/vers/projet/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Fichiers médias
    location /media/ {
        alias /chemin/vers/projet/media/;
        expires 7d;
    }
    
    # Proxy vers Gunicorn
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

---

## 🔄 Configuration de Gunicorn

### Créer un fichier `gunicorn_config.py`

```python
# gunicorn_config.py
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
preload_app = True
```

### Lancer Gunicorn

```bash
# Test
gunicorn siraweb.wsgi:application --config gunicorn_config.py

# En production avec systemd (voir ci-dessous)
```

---

## 🔧 Service Systemd (Linux)

### Créer `/etc/systemd/system/fasoweb.service`

```ini
[Unit]
Description=FASOWEB Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/chemin/vers/votre/projet
Environment="PATH=/chemin/vers/venv/bin"
ExecStart=/chemin/vers/venv/bin/gunicorn \
    --config /chemin/vers/projet/gunicorn_config.py \
    siraweb.wsgi:application

Restart=always

[Install]
WantedBy=multi-user.target
```

### Activer et démarrer le service

```bash
sudo systemctl daemon-reload
sudo systemctl enable fasoweb
sudo systemctl start fasoweb
sudo systemctl status fasoweb
```

---

## 📊 Vérifications post-installation

### 1. Vérifier que le site fonctionne

```bash
curl http://localhost:8000
```

### 2. Vérifier les fichiers statiques

```bash
curl http://localhost:8000/static/css/main.css
```

### 3. Vérifier les médias

```bash
curl http://localhost:8000/media/logo.png
```

### 4. Vérifier les logs

```bash
# Logs Gunicorn
sudo journalctl -u fasoweb -f

# Logs Nginx
sudo tail -f /var/log/nginx/error.log
```

---

## 🔒 Sécurité

### Checklist de sécurité

- [ ] `DEBUG=False` dans `.env`
- [ ] `SECRET_KEY` unique et sécurisée
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] SSL/HTTPS activé
- [ ] Permissions des fichiers correctes (755 pour dossiers, 644 pour fichiers)
- [ ] Fichier `.env` non accessible publiquement
- [ ] Base de données avec mot de passe fort
- [ ] Firewall configuré
- [ ] Mises à jour système régulières

---

## 🔄 Mises à jour

### Processus de mise à jour

```bash
# 1. Activer l'environnement virtuel
source venv/bin/activate

# 2. Récupérer les dernières modifications
git pull  # ou transférer les fichiers

# 3. Installer les nouvelles dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 6. Redémarrer Gunicorn
sudo systemctl restart fasoweb
```

---

## 📝 Commandes utiles

```bash
# Voir les logs en temps réel
sudo journalctl -u fasoweb -f

# Redémarrer le service
sudo systemctl restart fasoweb

# Vérifier le statut
sudo systemctl status fasoweb

# Tester la configuration Nginx
sudo nginx -t

# Recharger Nginx
sudo systemctl reload nginx
```

---

## 🆘 Dépannage

### Le site ne charge pas

1. Vérifier que Gunicorn tourne : `sudo systemctl status fasoweb`
2. Vérifier les logs : `sudo journalctl -u fasoweb -n 50`
3. Vérifier Nginx : `sudo nginx -t`
4. Vérifier les permissions des fichiers

### Erreur 502 Bad Gateway

- Gunicorn n'est probablement pas démarré
- Vérifier le port dans la configuration Nginx
- Vérifier les logs Gunicorn

### Fichiers statiques non chargés

- Vérifier `STATIC_ROOT` dans `settings.py`
- Vérifier que `collectstatic` a été exécuté
- Vérifier les permissions du dossier `staticfiles/`

---

## 📞 Support

Pour toute question, consultez :
- `GUIDE_HEBERGEMENT.md` - Guide complet d'hébergement
- `INSTRUCTIONS_SAUVEGARDE.md` - Instructions de sauvegarde
- Documentation Django : https://docs.djangoproject.com/
