# Guide d'Hébergement - Sauvegarder et Restaurer les Données

## 📦 Méthode 1 : Sauvegarde avec Django dumpdata (RECOMMANDÉ)

### Étape 1 : Sauvegarder les données AVANT l'hébergement

```bash
# Sauvegarder TOUTES les données (FAQ, Services, Portfolio, etc.)
python manage.py dumpdata core.FAQ core.Service core.Portfolio core.Technology core.AnonymousCTA core.WhatsAppConfig core.CompanyStats --indent 2 > backup_data.json

# OU sauvegarder uniquement les FAQ
python manage.py dumpdata core.FAQ --indent 2 > backup_faqs.json

# Sauvegarder TOUTES les données de l'application core
python manage.py dumpdata core --indent 2 > backup_all_core.json
```

### Étape 2 : Après l'hébergement, restaurer les données

```bash
# Restaurer les données sauvegardées
python manage.py loaddata backup_data.json

# OU restaurer uniquement les FAQ
python manage.py loaddata backup_faqs.json
```

---

## 📦 Méthode 2 : Sauvegarde de la base de données SQLite complète

### Étape 1 : Sauvegarder la base de données

```bash
# Copier le fichier de base de données
cp db.sqlite3 db_backup.sqlite3

# OU créer une archive
tar -czf backup_database.tar.gz db.sqlite3
```

### Étape 2 : Restaurer sur le serveur

```bash
# Copier le fichier sur le serveur
scp db_backup.sqlite3 user@serveur:/chemin/vers/projet/

# OU restaurer depuis l'archive
tar -xzf backup_database.tar.gz
```

---

## 📦 Méthode 3 : Export/Import via l'admin Django

### Étape 1 : Exporter depuis l'admin Django

1. Aller sur `/admin/core/faq/`
2. Sélectionner toutes les FAQ
3. Choisir "Exporter" (si plugin installé) ou utiliser la méthode 1

---

## 🚀 Guide complet d'hébergement

### Préparation avant l'hébergement

#### 1. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

#### 2. Créer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Créer un superutilisateur (si nécessaire)
```bash
python manage.py createsuperuser
```

#### 4. Sauvegarder les données
```bash
# Sauvegarder toutes les données importantes
python manage.py dumpdata core.FAQ core.Service core.Portfolio core.Technology core.AnonymousCTA core.WhatsAppConfig core.CompanyStats --indent 2 > backup_data.json

# Sauvegarder aussi les médias (images uploadées)
# Les fichiers dans media/ doivent être copiés manuellement
```

---

### Déploiement sur le serveur

#### 1. Transférer les fichiers
```bash
# Transférer le code source
scp -r * user@serveur:/chemin/vers/projet/

# Transférer les médias
scp -r media/ user@serveur:/chemin/vers/projet/media/

# Transférer la sauvegarde des données
scp backup_data.json user@serveur:/chemin/vers/projet/
```

#### 2. Sur le serveur, installer les dépendances
```bash
pip install -r requirements.txt
```

#### 3. Configurer les variables d'environnement
```bash
# Créer un fichier .env avec :
SECRET_KEY=votre_secret_key
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
SITE_DOMAIN=https://votre-domaine.com
```

#### 4. Appliquer les migrations
```bash
python manage.py migrate
```

#### 5. Restaurer les données
```bash
python manage.py loaddata backup_data.json
```

#### 6. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

#### 7. Créer un superutilisateur (si nécessaire)
```bash
python manage.py createsuperuser
```

---

## 🔧 Scripts de sauvegarde automatique

### Script de sauvegarde (backup.sh)

```bash
#!/bin/bash
# backup.sh - Script de sauvegarde automatique

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# Sauvegarder les données
python manage.py dumpdata core --indent 2 > $BACKUP_DIR/backup_$DATE.json

# Sauvegarder la base de données
cp db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3

# Sauvegarder les médias
tar -czf $BACKUP_DIR/media_$DATE.tar.gz media/

echo "Sauvegarde terminée : $BACKUP_DIR/backup_$DATE.json"
```

### Script de restauration (restore.sh)

```bash
#!/bin/bash
# restore.sh - Script de restauration

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh backup_YYYYMMDD_HHMMSS.json"
    exit 1
fi

BACKUP_FILE=$1

# Restaurer les données
python manage.py loaddata $BACKUP_FILE

echo "Restauration terminée depuis : $BACKUP_FILE"
```

---

## 📋 Checklist avant hébergement

- [ ] Sauvegarder toutes les FAQ : `python manage.py dumpdata core.FAQ > backup_faqs.json`
- [ ] Sauvegarder tous les services : `python manage.py dumpdata core.Service > backup_services.json`
- [ ] Sauvegarder le portfolio : `python manage.py dumpdata core.Portfolio > backup_portfolio.json`
- [ ] Sauvegarder les technologies : `python manage.py dumpdata core.Technology > backup_technologies.json`
- [ ] Sauvegarder les configurations : `python manage.py dumpdata core.AnonymousCTA core.WhatsAppConfig core.CompanyStats > backup_configs.json`
- [ ] Copier le dossier `media/` (images uploadées)
- [ ] Vérifier que `DEBUG=False` en production
- [ ] Configurer `ALLOWED_HOSTS` avec votre domaine
- [ ] Configurer le serveur web (Nginx/Apache)
- [ ] Configurer SSL/HTTPS
- [ ] Tester la restauration des données sur un environnement de test

---

## 🎯 Méthode rapide pour garder UNIQUEMENT les FAQ

### 1. Exporter les FAQ
```bash
python manage.py dumpdata core.FAQ --indent 2 > faqs_backup.json
```

### 2. Après l'hébergement, restaurer
```bash
python manage.py loaddata faqs_backup.json
```

**C'est tout !** Vos FAQ seront restaurées exactement comme avant.

---

## ⚠️ Notes importantes

1. **Les fichiers médias** (images uploadées) doivent être copiés manuellement du dossier `media/` local vers le serveur.

2. **Les migrations** doivent être appliquées AVANT de restaurer les données :
   ```bash
   python manage.py migrate
   python manage.py loaddata backup_data.json
   ```

3. **En production**, utilisez une base de données PostgreSQL ou MySQL au lieu de SQLite pour de meilleures performances.

4. **Sécurité** : Ne jamais commiter les fichiers de sauvegarde contenant des données sensibles dans Git.

---

## 🔄 Migration vers PostgreSQL (Recommandé pour production)

### 1. Installer PostgreSQL
```bash
sudo apt-get install postgresql postgresql-contrib
```

### 2. Créer la base de données
```sql
CREATE DATABASE siraweb_db;
CREATE USER siraweb_user WITH PASSWORD 'mot_de_passe_securise';
GRANT ALL PRIVILEGES ON DATABASE siraweb_db TO siraweb_user;
```

### 3. Modifier settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'siraweb_db',
        'USER': 'siraweb_user',
        'PASSWORD': 'mot_de_passe_securise',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Migrer les données
```bash
# Depuis SQLite vers PostgreSQL
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
# Changer la base de données dans settings.py
python manage.py migrate
python manage.py loaddata data.json
```

---

## 📞 Support

Si vous avez des questions ou des problèmes lors de l'hébergement, vérifiez :
- Les logs Django : `python manage.py runserver` en mode DEBUG
- Les logs du serveur web (Nginx/Apache)
- Les permissions des fichiers et dossiers
- La configuration de la base de données
