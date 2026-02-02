# 📋 Instructions Rapides - Sauvegarder vos FAQ

## ✅ Méthode la plus simple (RECOMMANDÉE)

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

## 📦 Méthode alternative avec Django

### Sauvegarder
```bash
python manage.py dumpdata core.FAQ --indent 2 > faqs_backup.json
```

### Restaurer
```bash
python manage.py loaddata faqs_backup.json
```

---

## 🎯 Fichiers créés

- ✅ `faqs_backup.json` - Votre sauvegarde des FAQ
- ✅ `backup_faqs.py` - Script Python de sauvegarde/restauration
- ✅ `quick_backup.bat` - Script Windows pour sauvegarder
- ✅ `quick_restore.bat` - Script Windows pour restaurer
- ✅ `GUIDE_HEBERGEMENT.md` - Guide complet d'hébergement

---

## ⚠️ Important

1. **Copiez le fichier `faqs_backup.json`** sur votre serveur d'hébergement
2. **Après avoir fait les migrations** sur le serveur, restaurez les FAQ
3. **Les images uploadées** (dossier `media/`) doivent être copiées manuellement

---

## 🚀 Étapes complètes pour l'hébergement

1. **Sauvegarder** : `python backup_faqs.py export`
2. **Copier** le fichier `faqs_backup.json` sur le serveur
3. **Sur le serveur** : Installer Django et les dépendances
4. **Sur le serveur** : `python manage.py migrate`
5. **Sur le serveur** : `python backup_faqs.py import` (ou `python manage.py loaddata faqs_backup.json`)
6. **Copier** le dossier `media/` sur le serveur

---

## ✅ Votre sauvegarde est prête !

Le fichier `faqs_backup.json` contient toutes vos 21 FAQ. 
Vous pouvez le copier en toute sécurité sur votre serveur d'hébergement.
