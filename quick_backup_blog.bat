@echo off
REM Script de sauvegarde rapide pour les articles de blog (Windows)
echo Sauvegarde des articles de blog en cours...

python backup_blog.py export
if %errorlevel% equ 0 (
    echo [OK] Sauvegarde reussie : blog_backup.json
) else (
    echo [ERREUR] Erreur lors de la sauvegarde
)

pause
