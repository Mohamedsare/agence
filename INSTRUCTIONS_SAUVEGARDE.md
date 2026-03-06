# 📋 Instructions Rapides - Sauvegarder vos Données

## 📝 Sauvegarder les FAQ

### 1. Sauvegarder vos FAQ (AVANT l'hébergement)

**Double-cliquez sur :** `quick_backup.bat`

**OU** dans le terminal :
```bash
python backup_faqs.py export
```

Cela créera le fichier `faqs_backup.json` avec toutes vos FAQ.

---

### 2. Restaurer vos FAQ (APRÈS l'hébergement)

**Double-cliquez sur :** `quick_restore.bat`

**OU** dans le terminal :
```bash
python backup_faqs.py import
```

Cela restaurera toutes vos FAQ depuis `faqs_backup.json`.

---

## 📝 Sauvegarder les Articles de Blog

### 1. Sauvegarder vos articles (AVANT l'hébergement)

**Double-cliquez sur :** `quick_backup_blog.bat`

**OU** dans le terminal :
```bash
python backup_blog.py export
```

Cela créera le fichier `blog_backup.json` avec tous vos articles, catégories et tags.

---

### 2. Restaurer vos articles (APRÈS l'hébergement)

**Double-cliquez sur :** `quick_restore_blog.bat`

**OU** dans le terminal :
```bash
python backup_blog.py import
```

Cela restaurera tous vos articles, catégories et tags depuis `blog_backup.json`.

---

## 📦 Méthode alternative avec Django

### Sauvegarder les FAQ
```bash
python manage.py dumpdata core.FAQ --indent 2 > faqs_backup.json
```

### Restaurer les FAQ
```bash
python manage.py loaddata faqs_backup.json
```

### Sauvegarder les articles de blog
```bash
python manage.py dumpdata core.Article core.Category core.Tag --indent 2 > blog_backup.json
```

### Restaurer les articles de blog
```bash
python manage.py loaddata blog_backup.json
```

---

## 🎯 Fichiers créés

### Pour les FAQ
- ✅ `faqs_backup.json` - Votre sauvegarde des FAQ
- ✅ `backup_faqs.py` - Script Python de sauvegarde/restauration
- ✅ `quick_backup.bat` - Script Windows pour sauvegarder les FAQ
- ✅ `quick_restore.bat` - Script Windows pour restaurer les FAQ

### Pour les Articles de Blog
- ✅ `blog_backup.json` - Votre sauvegarde des articles
- ✅ `backup_blog.py` - Script Python de sauvegarde/restauration
- ✅ `quick_backup_blog.bat` - Script Windows pour sauvegarder les articles
- ✅ `quick_restore_blog.bat` - Script Windows pour restaurer les articles

### Guides
- ✅ `GUIDE_HEBERGEMENT.md` - Guide complet d'hébergement
- ✅ `RESTAURER_FAQ_VPS.md` - Guide pour restaurer les FAQ sur le VPS
- ✅ `RESTAURER_BLOG_VPS.md` - Guide pour restaurer les articles sur le VPS

---

## ⚠️ Important

1. **Copiez le fichier `faqs_backup.json`** sur votre serveur d'hébergement
2. **Après avoir fait les migrations** sur le serveur, restaurez les FAQ
3. **Les images uploadées** (dossier `media/`) doivent être copiées manuellement

---

## 🚀 Étapes complètes pour l'hébergement

### Pour les FAQ
1. **Sauvegarder** : `python backup_faqs.py export`
2. **Copier** le fichier `faqs_backup.json` sur le serveur
3. **Sur le serveur** : `python backup_faqs.py import` (ou `python manage.py loaddata faqs_backup.json`)

### Pour les Articles de Blog
1. **Sauvegarder** : `python backup_blog.py export`
2. **Copier** le fichier `blog_backup.json` sur le serveur
3. **Sur le serveur** : `python backup_blog.py import` (ou `python manage.py loaddata blog_backup.json`)

### Étapes générales
1. **Sur le serveur** : Installer Django et les dépendances
2. **Sur le serveur** : `python manage.py migrate`
3. **Sur le serveur** : Restaurer les données (FAQ et/ou articles)
4. **Copier** le dossier `media/` sur le serveur

---

## ✅ Vos sauvegardes sont prêtes !

- Le fichier `faqs_backup.json` contient toutes vos FAQ.
- Le fichier `blog_backup.json` contient tous vos articles, catégories et tags.

Vous pouvez les copier en toute sécurité sur votre serveur d'hébergement.

---

## 🚀 Restauration rapide sur le VPS

### Méthode la plus simple (RECOMMANDÉE)

**Sur le VPS, utilisez les commandes Django :**

```bash
# Créer les FAQ automatiquement
python manage.py create_faqs

# Créer les articles de blog automatiquement
python manage.py create_blog_articles
```

Ces commandes créent automatiquement les données par défaut sans avoir besoin de fichiers de sauvegarde !
