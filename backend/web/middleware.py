from django.shortcuts import redirect
from django.urls import reverse

class OnboardingMiddleware:
    """
    Middleware pour rediriger les utilisateurs non-onboardés vers le flow d'onboarding.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs qui ne nécessitent pas l'onboarding
        self.exempt_urls = [
            '/',
            '/login/',
            '/register/',
            '/logout/',
            '/onboarding/',
            '/static/',
            '/media/',
            '/admin/',
            '/api/',
            '/reset_password/',
            '/legal/',
            '/blog/',
            '/article/',
        ]
    
    def __call__(self, request):
        # Vérifier si l'utilisateur est authentifié
        if request.user.is_authenticated:
            # Vérifier si l'utilisateur n'est pas onboardé
            if not request.user.is_onboarded:
                # Vérifier si l'URL actuelle n'est pas exemptée
                path = request.path
                is_exempt = any(path.startswith(url) for url in self.exempt_urls)
                
                if not is_exempt:
                    # Rediriger vers l'onboarding
                    return redirect('onboarding_welcome')
        
        response = self.get_response(request)
        return response
