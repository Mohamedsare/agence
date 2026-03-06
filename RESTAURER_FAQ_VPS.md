# 🔄 Comment restaurer les FAQ sur le VPS

Vous avez déjà hébergé l'application mais les FAQ ne sont pas encore restaurées. Voici **3 méthodes** pour les récupérer :

---

## ✅ Méthode 1 : Utiliser la commande Django (PLUS SIMPLE - RECOMMANDÉ)

Cette méthode crée automatiquement toutes les 21 FAQ par défaut.

### Sur votre VPS, connectez-vous en SSH :

```bash
# Se connecter au VPS
ssh user@votre-serveur.com

# Aller dans le dossier du projet
cd /chemin/vers/votre/projet

# Activer l'environnement virtuel (si vous en avez un)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Lancer la commande pour créer les FAQ
python manage.py create_faqs
```

**C'est tout !** Les 21 FAQ seront créées automatiquement.

---

## ✅ Méthode 2 : Si vous avez le fichier `faqs_backup.json` localement

### Étape 1 : Transférer le fichier sur le VPS

**Depuis votre machine locale :**

```bash
# Transférer le fichier faqs_backup.json vers le VPS
scp faqs_backup.json user@votre-serveur.com:/chemin/vers/votre/projet/
```

**OU** utilisez un client FTP/SFTP (FileZilla, WinSCP, etc.) pour transférer le fichier.

### Étape 2 : Restaurer sur le VPS

**Sur le VPS :**

```bash
# Se connecter au VPS
ssh user@votre-serveur.com

# Aller dans le dossier du projet
cd /chemin/vers/votre/projet

# Activer l'environnement virtuel
source venv/bin/activate

# Restaurer les FAQ
python manage.py loaddata faqs_backup.json

# OU utiliser le script Python
python backup_faqs.py import
```

---

## ✅ Méthode 3 : Créer les FAQ via l'admin Django

### Étape 1 : Accéder à l'admin

1. Allez sur : `https://votre-domaine.com/admin/`
2. Connectez-vous avec votre compte superutilisateur

### Étape 2 : Créer les FAQ manuellement

1. Cliquez sur **"FAQs"** dans la section **"CORE"**
2. Cliquez sur **"Ajouter FAQ"**
3. Remplissez les champs :
   - **Question** : La question
   - **Réponse** : La réponse
   - **Ordre d'affichage** : Numéro d'ordre (1, 2, 3, etc.)
   - **Actif** : Cochez la case
4. Cliquez sur **"Enregistrer"**
5. Répétez pour chaque FAQ

**Note :** Cette méthode est longue si vous avez beaucoup de FAQ.

---

## 🎯 Méthode recommandée : Commande Django

**La méthode la plus rapide et simple est la Méthode 1** :

```bash
# Sur le VPS
cd /chemin/vers/votre/projet
source venv/bin/activate  # Si vous avez un venv
python manage.py create_faqs
```

Cette commande :
- ✅ Crée automatiquement les 21 FAQ par défaut
- ✅ Ne supprime pas les FAQ existantes (mise à jour si elles existent)
- ✅ Fonctionne même si vous n'avez pas de sauvegarde

---

## 🔍 Vérifier que les FAQ sont créées

### Option 1 : Via l'admin Django

1. Allez sur : `https://votre-domaine.com/admin/core/faq/`
2. Vous devriez voir la liste des FAQ

### Option 2 : Via le site

1. Allez sur : `https://votre-domaine.com/#faq`
2. La section FAQ devrait être visible avec toutes les questions

### Option 3 : Via la ligne de commande

```bash
# Sur le VPS
python manage.py shell

# Dans le shell Python
from core.models import FAQ
print(f"Nombre de FAQ : {FAQ.objects.count()}")
# Devrait afficher : Nombre de FAQ : 21
```

---

## 🆘 Problèmes courants

### Erreur : "Command not found: python"

**Solution :** Utilisez `python3` au lieu de `python`

```bash
python3 manage.py create_faqs
```

### Erreur : "No module named 'django'"

**Solution :** Activez votre environnement virtuel

```bash
source venv/bin/activate
# ou
source /chemin/vers/venv/bin/activate
```

### Erreur : "ModuleNotFoundError: No module named 'core'"

**Solution :** Assurez-vous d'être dans le bon répertoire

```bash
cd /chemin/vers/votre/projet
# Le dossier doit contenir manage.py
ls manage.py  # Doit afficher manage.py
```

### Les FAQ ne s'affichent pas sur le site

**Vérifications :**

1. Les FAQ sont-elles actives dans l'admin ?
   - Allez sur `/admin/core/faq/`
   - Vérifiez que la colonne "Actif" est cochée

2. Le cache est-il vidé ?
   ```bash
   python manage.py clear_cache  # Si vous avez un cache
   ```

3. Redémarrez Gunicorn :
   ```bash
   sudo systemctl restart fasoweb
   # ou
   sudo systemctl restart gunicorn
   ```

---

## 📋 Checklist rapide

- [ ] Connecté au VPS via SSH
- [ ] Dans le bon répertoire du projet
- [ ] Environnement virtuel activé (si nécessaire)
- [ ] Commande exécutée : `python manage.py create_faqs`
- [ ] Vérifié dans l'admin : `/admin/core/faq/`
- [ ] Vérifié sur le site : `/#faq`

---

## ✅ Résumé - Commande unique

**Sur votre VPS, exécutez simplement :**

```bash
cd /chemin/vers/votre/projet && source venv/bin/activate && python manage.py create_faqs
```

**C'est tout !** Vos FAQ seront créées en quelques secondes.

---

## 📞 Besoin d'aide ?

Si vous rencontrez des problèmes :

1. Vérifiez les logs Django : `tail -f /var/log/django/error.log`
2. Vérifiez les logs Gunicorn : `sudo journalctl -u fasoweb -f`
3. Vérifiez que les migrations sont appliquées : `python manage.py migrate`
