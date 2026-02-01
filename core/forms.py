from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulaire de contact."""
    BUDGET_CHOICES = [
        ('', 'Sélectionnez un budget'),
        ('< 500 000 FCFA', 'Moins de 500 000 FCFA'),
        ('500 000 - 1 000 000 FCFA', '500 000 - 1 000 000 FCFA'),
        ('1 000 000 - 2 000 000 FCFA', '1 000 000 - 2 000 000 FCFA'),
        ('2 000 000 - 5 000 000 FCFA', '2 000 000 - 5 000 000 FCFA'),
        ('> 5 000 000 FCFA', 'Plus de 5 000 000 FCFA'),
    ]

    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'budget'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom complet',
                'required': True,
                'autocomplete': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com',
                'required': True,
                'autocomplete': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+226 XX XX XX XX',
                'autocomplete': 'tel'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom de votre entreprise (optionnel)',
                'autocomplete': 'organization'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Décrivez votre projet en quelques mots...',
                'rows': 6,
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nom complet'
        self.fields['email'].label = 'Email'
        self.fields['phone'].label = 'Téléphone'
        self.fields['company'].label = 'Entreprise'
        self.fields['budget'].label = 'Budget estimé'
        self.fields['message'].label = 'Message'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Nettoyer le numéro de téléphone
            phone = phone.strip()
        return phone
