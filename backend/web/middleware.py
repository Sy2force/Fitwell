from django.shortcuts import redirect
from django.urls import resolve, Resolver404

class OnboardingMiddleware:
    """
    Middleware pour rediriger les utilisateurs non-onboardés vers le flow d'onboarding.
    Utilise les noms d'URL pour être robuste face à l'i18n.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Noms d'URL qui ne nécessitent pas l'onboarding
        self.exempt_url_names = [
            'home',
            'login',
            'register',
            'logout',
            'password_reset',
            'password_reset_done',
            'password_reset_confirm',
            'password_reset_complete',
            'legal',
            'onboarding_welcome',
            'onboarding_step1',
            'onboarding_step2',
            'onboarding_step3',
            'set_language', # For i18n switcher
        ]
        
        # Préfixes de chemin toujours exemptés (Admin, API, Static)
        self.exempt_prefixes = [
            '/admin/',
            '/api/',
            '/static/',
            '/media/',
            '/i18n/',
        ]
    
    def __call__(self, request):
        # Vérifier si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Vérifier si l'utilisateur n'est pas onboardé
            if not request.user.is_onboarded:
                path = request.path_info
                
                # 1. Check Prefixes
                if any(path.startswith(prefix) for prefix in self.exempt_prefixes):
                    return self.get_response(request)
                
                # 2. Check URL Name
                try:
                    resolver_match = resolve(path)
                    url_name = resolver_match.url_name
                    
                    if url_name in self.exempt_url_names:
                        return self.get_response(request)
                        
                except Resolver404:
                    pass # 404s will be handled by Django later
                
                # Si on est ici, c'est que l'URL est protégée et l'user non onboardé
                return redirect('onboarding_welcome')
        
        response = self.get_response(request)
        return response
