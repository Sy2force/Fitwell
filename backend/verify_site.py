import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

TESTS = [
    {
        "page": "Home",
        "url_en": "/en/",
        "url_fr": "/fr/",
        "check_en": "Human Performance",
        "check_fr": "Performance Humaine"
    },
    {
        "page": "Login",
        "url_en": "/en/login/",
        "url_fr": "/fr/login/",
        "check_en": "Secure Terminal Access",
        "check_fr": "Accès Terminal Sécurisé"
    },
    {
        "page": "Register",
        "url_en": "/en/register/",
        "url_fr": "/fr/register/",
        "check_en": "Begin Your Legacy",
        "check_fr": "Commencez Votre Héritage"
    },
    {
        "page": "Blog",
        "url_en": "/en/blog/",
        "url_fr": "/fr/blog/",
        "check_en": "Knowledge base",
        "check_fr": "Base de connaissances"
    },
    {
        "page": "Legal",
        "url_en": "/en/legal/",
        "url_fr": "/fr/legal/",
        "check_en": "Terms of use",
        "check_fr": "Conditions d'utilisation"
    }
]

def run_verification():
    print("🚀 Démarrage de la vérification approfondie FitWell...\n")
    all_passed = True

    for test in TESTS:
        print(f"🔹 Vérification de la page : {test['page']}")
        
        # English Check
        try:
            r_en = requests.get(f"{BASE_URL}{test['url_en']}")
            if r_en.status_code == 200 and test['check_en'] in r_en.text:
                print(f"  ✅ EN: OK ({test['check_en']})")
            else:
                print(f"  ❌ EN: ÉCHEC (Attendu: '{test['check_en']}')")
                all_passed = False
        except Exception as e:
            print(f"  ❌ EN: Erreur connexion ({e})")
            all_passed = False

        # French Check
        try:
            r_fr = requests.get(f"{BASE_URL}{test['url_fr']}")
            if r_fr.status_code == 200 and test['check_fr'] in r_fr.text:
                print(f"  ✅ FR: OK ({test['check_fr']})")
            else:
                print(f"  ❌ FR: ÉCHEC (Attendu: '{test['check_fr']}')")
                all_passed = False
        except Exception as e:
            print(f"  ❌ FR: Erreur connexion ({e})")
            all_passed = False
            
        print("")

    if all_passed:
        print("✨ TME : TOUS LES SYSTÈMES SONT OPÉRATIONNELS ET TRADUITS. ✨")
        sys.exit(0)
    else:
        print("⚠️  ATTENTION : Certains tests ont échoué.")
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
