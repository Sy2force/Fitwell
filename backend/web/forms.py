from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.utils.translation import gettext_lazy as _
from api.models import User, WellnessPlan, Comment, CustomEvent, DailyLog

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['water_liters', 'sleep_hours', 'mood', 'weight', 'notes']
        widgets = {
            'water_liters': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '2.5'}),
            'sleep_hours': forms.NumberInput(attrs={'step': '0.5', 'placeholder': '7.5'}),
            'mood': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10', 'class': 'w-full'}),
            'weight': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'kg'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Notes sur la journée...')}),
        }
        labels = {
            'water_liters': _('Eau (L)'),
            'sleep_hours': _('Sommeil (h)'),
            'mood': _('Humeur (1-10)'),
            'weight': _('Poids (kg)'),
            'notes': _('Journal de bord'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white focus:border-energy focus:outline-none dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white'
        for field_name, field in self.fields.items():
            if field_name != 'mood': # Range input styling is different usually
                field.widget.attrs.update({'class': common_classes})

class CustomEventForm(forms.ModelForm):
    class Meta:
        model = CustomEvent
        fields = ['title', 'event_type', 'day_of_week', 'start_time', 'end_time', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Ex: Séance Pecs, Réunion Projet X')}),
            'day_of_week': forms.Select(choices=[
                ('monday', _('Lundi')),
                ('tuesday', _('Mardi')),
                ('wednesday', _('Mercredi')),
                ('thursday', _('Jeudi')),
                ('friday', _('Vendredi')),
                ('saturday', _('Samedi')),
                ('sunday', _('Dimanche')),
            ]),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'title': _('Titre de l\'activité'),
            'event_type': _('Type'),
            'day_of_week': _('Jour'),
            'start_time': _('Début'),
            'end_time': _('Fin'),
            'priority': _('Priorité'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white focus:border-energy focus:outline-none dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white'
        for field in self.fields.values():
            field.widget.attrs.update({'class': common_classes})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-energy focus:outline-none focus:ring-1 focus:ring-energy transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
            })
            if field_name == 'username':
                field.widget.attrs['placeholder'] = _("Nom d'utilisateur")
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = _("adresse@email.com")

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
            })
        self.fields['username'].widget.attrs['placeholder'] = _("Nom d'utilisateur / Email")
        self.fields['password'].widget.attrs['placeholder'] = _("Mot de passe")

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
                'placeholder': _('votre@email.com')
            })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
            })

class WellnessPlanForm(forms.ModelForm):
    class Meta:
        model = WellnessPlan
        fields = ['age', 'gender', 'height', 'weight', 'goal', 'activity_level']
        labels = {
            'age': _('Âge'),
            'gender': _('Genre'),
            'height': _('Taille'),
            'weight': _('Poids'),
            'goal': _('Objectif'),
            'activity_level': _("Niveau d'activité"),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definition des classes communes
        common_classes = 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white focus:border-energy focus:outline-none dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white'
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': common_classes})
            
        # Placeholders specifiques
        self.fields['height'].widget.attrs['placeholder'] = 'cm'
        self.fields['weight'].widget.attrs['placeholder'] = 'kg'

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and height <= 0:
            raise forms.ValidationError(_("La taille doit être supérieure à 0."))
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight <= 0:
            raise forms.ValidationError(_("Le poids doit être supérieur à 0."))
        return weight
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age <= 0:
            raise forms.ValidationError(_("L'âge doit être supérieur à 0."))
        return age

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 border border-white/10 p-4 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
                'rows': 4,
                'placeholder': _('Partagez votre analyse...')
            })
        }
        labels = {
            'content': _('Votre Commentaire')
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'bio', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
                'placeholder': _('votre@email.com')
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
                'rows': 3,
                'placeholder': _('Parlez-nous de vos objectifs...')
            }),
            'avatar': forms.TextInput(attrs={
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
                'placeholder': _('URL de votre image')
            })
        }
        labels = {
            'email': _('Email'),
            'bio': _('Biographie'),
            'avatar': _('Avatar (URL)'),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-gray-900 border border-white/10 p-3 rounded text-white placeholder-gray-500 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors dark:bg-black/30 dark:border-white/10 bg-white border-gray-300 text-gray-900 dark:text-white',
            })
