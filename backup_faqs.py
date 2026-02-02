#!/usr/bin/env python
"""
Script de sauvegarde/restauration des FAQ
Usage:
    python backup_faqs.py export    # Exporter les FAQ
    python backup_faqs.py import    # Importer les FAQ
"""
import os
import sys
import django
import json
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siraweb.settings')
django.setup()

from core.models import FAQ


def export_faqs():
    """Exporter toutes les FAQ vers un fichier JSON."""
    faqs = FAQ.objects.all()
    data = []
    
    for faq in faqs:
        data.append({
            'question': faq.question,
            'answer': faq.answer,
            'order': faq.order,
            'active': faq.active,
        })
    
    output_file = BASE_DIR / 'faqs_backup.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] {len(data)} FAQ(s) exportee(s) vers {output_file}")
    return output_file


def import_faqs():
    """Importer les FAQ depuis un fichier JSON."""
    input_file = BASE_DIR / 'faqs_backup.json'
    
    if not input_file.exists():
        print(f"[ERREUR] Fichier {input_file} introuvable!")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    imported = 0
    updated = 0
    
    for faq_data in data:
        faq, created = FAQ.objects.update_or_create(
            question=faq_data['question'],
            defaults={
                'answer': faq_data['answer'],
                'order': faq_data.get('order', 0),
                'active': faq_data.get('active', True),
            }
        )
        
        if created:
            imported += 1
            print(f"[OK] FAQ creee: {faq.question}")
        else:
            updated += 1
            print(f"[UPDATE] FAQ mise a jour: {faq.question}")
    
    print(f"\n[SUCCESS] Termine ! {imported} creee(s), {updated} mise(s) a jour.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python backup_faqs.py [export|import]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        export_faqs()
    elif command == 'import':
        import_faqs()
    else:
        print("Commande invalide. Utilisez 'export' ou 'import'")
        sys.exit(1)
