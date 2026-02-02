@echo off
REM Script de restauration rapide pour Windows
echo Restauration des FAQ en cours...

if exist faqs_backup.json (
    python manage.py loaddata faqs_backup.json
    if %errorlevel% equ 0 (
        echo ✅ Restauration reussie !
    ) else (
        echo ❌ Erreur lors de la restauration
        echo Utilisation du script Python alternatif...
        python backup_faqs.py import
    )
) else (
    echo ❌ Fichier faqs_backup.json introuvable !
    echo Assurez-vous d'avoir sauvegarde les FAQ avant.
)

pause
