@echo off
REM Script de sauvegarde rapide pour Windows
echo Sauvegarde des FAQ en cours...

python manage.py dumpdata core.FAQ --indent 2 > faqs_backup.json
if %errorlevel% equ 0 (
    echo ✅ Sauvegarde reussie : faqs_backup.json
) else (
    echo ❌ Erreur lors de la sauvegarde
    echo Utilisation du script Python alternatif...
    python backup_faqs.py export
)

pause
