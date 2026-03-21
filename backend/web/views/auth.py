from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from web.forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, CustomPasswordChangeForm
from api.models import User
from api.services.gamification import check_and_award_badges

def login_view(request):
    """
    Connexion utilisateur.
    Met à jour le streak à la connexion.
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Update Streak on Login
            if hasattr(user, 'stats'):
                user.stats.update_streak()
            return redirect('home')
        else:
            messages.error(request, _("Identifiants invalides."))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'web/login.html', {'form': form})

def logout_view(request):
    """
    Déconnexion utilisateur.
    """
    logout(request)
    return redirect('home')

def register_view(request):
    """
    Inscription nouvel utilisateur.
    Initialise les stats et le streak.
    Envoie un email de bienvenue.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Spécifier le backend d'authentification pour éviter l'erreur "multiple authentication backends"
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            # Init Streak
            if hasattr(user, 'stats'):
                user.stats.update_streak()
            
            # Send Welcome Email
            try:
                send_mail(
                    subject=_("Bienvenue sur FitWell ! 🚀"),
                    message=_("Salut %(username)s,\n\nBienvenue dans l'élite. Ton voyage vers l'optimisation commence maintenant.\n\nAccède à ton QG : %(url)s\n\nL'équipe FitWell") % {
                        'username': user.username,
                        'url': request.build_absolute_uri(reverse('dashboard'))
                    },
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
            except Exception:
                pass # Don't block registration if email fails

            messages.success(request, _("Bienvenue ! Ton compte a été créé avec succès."))
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'web/register.html', {'form': form})

@login_required(login_url='login')
def profile_view(request):
    # Update Streak on Profile Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/profile.html', {'user': request.user, 'plan': latest_plan})

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profil mis à jour avec succès."))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'web/edit_profile.html', {'form': form})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Votre mot de passe a été mis à jour avec succès.'))
            return redirect('profile')
        else:
            messages.error(request, _('Veuillez corriger les erreurs ci-dessous.'))
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'web/change_password.html', {
        'form': form
    })
