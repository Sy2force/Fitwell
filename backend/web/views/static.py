from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.models import WellnessPlan

def home(request):
    """
    Page d'accueil du site.
    Affiche le dernier plan généré si l'utilisateur est connecté.
    """
    latest_plan = None
    if request.user.is_authenticated:
        latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/home.html', {'plan': latest_plan})

@login_required(login_url='login')
def tools_view(request):
    # Update Streak on Tools Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = None
    if request.user.is_authenticated:
        latest_plan = request.user.plans.order_by('-created_at').first()
        
    return render(request, 'web/tools.html', {'plan': latest_plan})

def legal_view(request):
    """
    Page des mentions légales et conditions d'utilisation.
    """
    return render(request, 'web/legal.html')


def about_view(request):
    """
    Page "À propos" : mission, valeurs, histoire de FitWell.
    """
    return render(request, 'web/about.html')

def custom_404(request, exception):
    """
    Page d'erreur 404 personnalisée (Page non trouvée).
    """
    return render(request, '404.html', status=404)

def custom_500(request):
    """
    Page d'erreur 500 personnalisée (Erreur serveur).
    """
    return render(request, '500.html', status=500)
