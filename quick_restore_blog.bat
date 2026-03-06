@echo off
REM Script de restauration rapide pour les articles de blog (Windows)
echo Restauration des articles de blog en cours...

if exist blog_backup.json (
    python backup_blog.py import
    if %errorlevel% equ 0 (
        echo [OK] Restauration reussie !
    ) else (
        echo [ERREUR] Erreur lors de la restauration
    )
) else (
    echo [ERREUR] Fichier blog_backup.json introuvable !
    echo Assurez-vous d'avoir sauvegarde les articles avant.
)

pause
