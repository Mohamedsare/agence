# 🔄 Comment restaurer les articles de blog sur le VPS

Vous avez déjà hébergé l'application mais les articles de blog ne sont pas encore restaurés. Voici **3 méthodes** pour les récupérer :

---

## ✅ Méthode 1 : Utiliser la commande Django (PLUS SIMPLE - RECOMMANDÉ)

Cette méthode crée automatiquement des articles de blog par défaut avec catégories et tags.

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

# Lancer la commande pour créer les articles de blog
python manage.py create_blog_articles
```

**C'est tout !** Les articles, catégories et tags seront créés automatiquement.

---

## ✅ Méthode 2 : Si vous avez le fichier `blog_backup.json` localement

### Étape 1 : Transférer le fichier sur le VPS

**Depuis votre machine locale :**

```bash
# Transférer le fichier blog_backup.json vers le VPS
scp blog_backup.json user@votre-serveur.com:/chemin/vers/votre/projet/
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

# Restaurer les articles de blog
python backup_blog.py import

# OU utiliser Django dumpdata
python manage.py loaddata blog_backup.json
```

---

## ✅ Méthode 3 : Créer les articles via l'admin Django

### Étape 1 : Accéder à l'admin

1. Allez sur : `https://votre-domaine.com/admin/`
2. Connectez-vous avec votre compte superutilisateur

### Étape 2 : Créer les catégories et tags

1. Cliquez sur **"Catégories"** dans la section **"CORE"**
2. Créez vos catégories (ex: "Développement Web", "SEO", etc.)
3. Cliquez sur **"Tags"** et créez vos tags

### Étape 3 : Créer les articles

1. Cliquez sur **"Articles"** dans la section **"CORE"**
2. Cliquez sur **"Ajouter Article"**
3. Remplissez les champs :
   - **Titre** : Le titre de l'article
   - **Extrait** : Un court résumé
   - **Contenu** : Le contenu complet de l'article
   - **Catégorie** : Sélectionnez une catégorie
   - **Tags** : Sélectionnez les tags
   - **Publié** : Cochez pour publier l'article
   - **Meta titre** et **Meta description** : Pour le SEO
4. Cliquez sur **"Enregistrer"**
5. Répétez pour chaque article

**Note :** Cette méthode est longue si vous avez beaucoup d'articles.

---

## 🎯 Méthode recommandée : Commande Django

**La méthode la plus rapide et simple est la Méthode 1** :

```bash
# Sur le VPS
cd /chemin/vers/votre/projet
source venv/bin/activate  # Si vous avez un venv
python manage.py create_blog_articles
```

Cette commande :
- ✅ Crée automatiquement des catégories par défaut
- ✅ Crée automatiquement des tags par défaut
- ✅ Crée automatiquement 5 articles de blog par défaut
- ✅ Ne supprime pas les articles existants (mise à jour si ils existent)

---

## 🔍 Vérifier que les articles sont créés

### Option 1 : Via l'admin Django

1. Allez sur : `https://votre-domaine.com/admin/core/article/`
2. Vous devriez voir la liste des articles

### Option 2 : Via le site

1. Allez sur : `https://votre-domaine.com/blog/`
2. La page blog devrait afficher les articles publiés

### Option 3 : Via la ligne de commande

```bash
# Sur le VPS
python manage.py shell

# Dans le shell Python
from core.models import Article, Category, Tag
print(f"Nombre d'articles : {Article.objects.count()}")
print(f"Nombre de catégories : {Category.objects.count()}")
print(f"Nombre de tags : {Tag.objects.count()}")
```

---

## 🆘 Problèmes courants

### Erreur : "Command not found: python"

**Solution :** Utilisez `python3` au lieu de `python`

```bash
python3 manage.py create_blog_articles
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

### Les articles ne s'affichent pas sur le site

**Vérifications :**

1. Les articles sont-ils publiés dans l'admin ?
   - Allez sur `/admin/core/article/`
   - Vérifiez que la colonne "Publié" est cochée

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

### Erreur lors de l'import : "Category does not exist"

**Solution :** Assurez-vous que les catégories sont créées avant les articles. La commande `create_blog_articles` gère cela automatiquement.

---

## 📋 Checklist rapide

- [ ] Connecté au VPS via SSH
- [ ] Dans le bon répertoire du projet
- [ ] Environnement virtuel activé (si nécessaire)
- [ ] Commande exécutée : `python manage.py create_blog_articles`
- [ ] Vérifié dans l'admin : `/admin/core/article/`
- [ ] Vérifié sur le site : `/blog/`

---

## ✅ Résumé - Commande unique

**Sur votre VPS, exécutez simplement :**

```bash
cd /chemin/vers/votre/projet && source venv/bin/activate && python manage.py create_blog_articles
```

**C'est tout !** Vos articles de blog seront créés en quelques secondes.

---

## 📝 Articles créés par défaut

La commande `create_blog_articles` crée automatiquement :

**Catégories :**
- Développement Web
- SEO & Référencement
- Conseils & Astuces
- Actualités

**Tags :**
- Django, Python, SEO, Web Design, E-commerce, Responsive, Performance, Sécurité, Burkina Faso, Afrique

**Articles (5 articles) :**
1. Pourquoi avoir un site web est essentiel pour votre entreprise au Burkina Faso
2. Les 5 erreurs à éviter lors de la création de votre site web
3. Comment améliorer votre référencement naturel (SEO) au Burkina Faso
4. Django vs WordPress : Quel CMS choisir pour votre site web ?
5. FASOWEB lance son nouveau site web : Découvrez nos services

---

## 📞 Besoin d'aide ?

Si vous rencontrez des problèmes :

1. Vérifiez les logs Django : `tail -f /var/log/django/error.log`
2. Vérifiez les logs Gunicorn : `sudo journalctl -u fasoweb -f`
3. Vérifiez que les migrations sont appliquées : `python manage.py migrate`
