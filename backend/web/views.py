from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Q
from django.db import models
from .forms import CustomUserCreationForm, CustomAuthenticationForm, WellnessPlanForm, CommentForm, UserUpdateForm, CustomPasswordChangeForm, CustomEventForm, DailyLogForm, CustomWorkoutForm
from api.models import User, Article, Category, UserStats, WellnessPlan, Comment, CustomEvent, Exercise, DailyLog, Recipe, WorkoutSession, ExerciseSet
from api.services import generate_wellness_plan

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
def dashboard_view(request):
    """
    Tableau de bord principal de l'utilisateur.
    Gère :
    - Le journal quotidien (Daily Log)
    - Les statistiques rapides (Sommeil, Eau)
    - Les graphiques de progression (Poids, Humeur, Sommeil)
    - L'agenda du jour
    """
    # Update Streak
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    today_log, created = DailyLog.objects.get_or_create(user=request.user, date=timezone.now().date())
    
    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=today_log)
        if form.is_valid():
            form.save()
            # XP Reward for logging (once per day fully)
            # Simple logic: Give XP every save for now, or check delta. 
            # Better: Just give small XP for updating.
            request.user.stats.add_xp(20)
            messages.success(request, _("Journal mis à jour ! +20 XP"))
            return redirect('dashboard')
    else:
        form = DailyLogForm(instance=today_log)
        
    # Recent Activity / Stats
    week_logs = request.user.daily_logs.order_by('-date')[:7]
    avg_sleep = week_logs.aggregate(Avg('sleep_hours'))['sleep_hours__avg'] or 0
    avg_water = week_logs.aggregate(Avg('water_liters'))['water_liters__avg'] or 0
    
    # Chart Data (Last 30 days)
    # Fetch most recent 30 logs, then reverse to chronological order
    recent_logs = request.user.daily_logs.order_by('-date')[:30]
    chart_logs = sorted(recent_logs, key=lambda x: x.date)
    
    chart_dates = [log.date.strftime('%d/%m') for log in chart_logs]
    chart_weight = [log.weight for log in chart_logs if log.weight]
    chart_sleep = [log.sleep_hours for log in chart_logs]
    chart_mood = [log.mood for log in chart_logs]
    
    # Today's Agenda
    today_events = request.user.custom_events.filter(
        day_of_week=timezone.now().strftime('%A').lower()
    ).order_by('start_time')
    
    return render(request, 'web/dashboard.html', {
        'form': form,
        'user': request.user,
        'avg_sleep': round(avg_sleep, 1),
        'avg_water': round(avg_water, 1),
        'today_events': today_events,
        'chart_dates': chart_dates,
        'chart_weight': chart_weight,
        'chart_sleep': chart_sleep,
        'chart_mood': chart_mood,
    })

@login_required(login_url='login')
def exercise_library(request):
    """
    Bibliothèque d'exercices.
    Permet de filtrer par groupe musculaire.
    """
    exercises = Exercise.objects.all()
    
    muscle = request.GET.get('muscle')
    if muscle:
        exercises = exercises.filter(muscle_group=muscle)
        
    return render(request, 'web/exercise_library.html', {
        'exercises': exercises,
        'current_muscle': muscle,
        'muscle_choices': Exercise.MUSCLE_CHOICES
    })

@login_required(login_url='login')
def recipe_list(request):
    """
    Liste des recettes de nutrition.
    Filtrage par catégorie (petit-déj, dîner...) et difficulté.
    """
    recipes = Recipe.objects.all()
    
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    if category:
        recipes = recipes.filter(category=category)
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
        
    return render(request, 'web/recipe_list.html', {
        'recipes': recipes,
        'current_category': category,
        'current_difficulty': difficulty,
        'category_choices': Recipe.CATEGORY_CHOICES
    })

@login_required(login_url='login')
def recipe_detail(request, recipe_id):
    """
    Détail d'une recette avec calcul des pourcentages de macros.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Calculate Macro Percentages
    # 1g Protein = 4kcal, 1g Carb = 4kcal, 1g Fat = 9kcal
    cal_protein = recipe.protein_g * 4
    cal_carbs = recipe.carbs_g * 4
    cal_fats = recipe.fats_g * 9
    
    total_cal_calc = cal_protein + cal_carbs + cal_fats
    
    context = {
        'recipe': recipe,
        'pct_protein': 0,
        'pct_carbs': 0,
        'pct_fats': 0
    }
    
    if total_cal_calc > 0:
        context['pct_protein'] = int((cal_protein / total_cal_calc) * 100)
        context['pct_carbs'] = int((cal_carbs / total_cal_calc) * 100)
        context['pct_fats'] = int((cal_fats / total_cal_calc) * 100)
        
    return render(request, 'web/recipe_detail.html', context)

@login_required(login_url='login')
def workout_setup_view(request):
    """
    Page de configuration avant de lancer une séance.
    Permet de choisir les exercices et la durée.
    """
    form = CustomWorkoutForm()
    return render(request, 'web/workout_setup.html', {'form': form})

@login_required(login_url='login')
def workout_session_view(request):
    """
    Coach Tactique (Session d'entraînement).
    Génère une séquence d'exercices (Échauffement -> Exos -> Repos -> Retour au calme).
    Si aucun exercice n'est sélectionné, l'IA en choisit selon le profil.
    """
    # Logic to build a session
    
    # Defaults
    work_duration = 45
    rest_duration = 15
    selected_exercises_objs = []
    
    # 1. Check if we have data from Setup (POST)
    if request.method == 'POST':
        form = CustomWorkoutForm(request.POST)
        if form.is_valid():
            selected_exercises_objs = list(form.cleaned_data['exercises'])
            work_duration = form.cleaned_data['work_duration']
            rest_duration = form.cleaned_data['rest_duration']
    
    # 2. If no exercises selected (GET or empty POST), fallback to auto-gen logic
    if not selected_exercises_objs:
        # 1. Get User Level/Plan
        user_level = 'beginner'
        if hasattr(request.user, 'stats') and request.user.stats.level > 5:
            user_level = 'intermediate'
        if hasattr(request.user, 'stats') and request.user.stats.level > 15:
            user_level = 'advanced'
            
        # 2. Select Exercises & Sequence Strategy
        # Try to match with latest plan goal if exists
        latest_plan = request.user.plans.order_by('-created_at').first()
        goal = latest_plan.goal if latest_plan else 'maintenance'
        
        # Filter exercises by level first
        base_exercises = Exercise.objects.filter(difficulty=user_level)
        if not base_exercises.exists():
            base_exercises = Exercise.objects.all()
            
        # Strategy based on Goal
        if goal == 'weight_loss':
            # High intensity, focus on Cardio/Full Body/Legs
            work_duration = 40
            rest_duration = 10
            priority_groups = ['cardio', 'full', 'legs', 'abs']
            candidates = base_exercises.filter(muscle_group__in=priority_groups)
            # Fallback if not enough specific ones
            if candidates.count() < 5:
                candidates = base_exercises
        elif goal == 'muscle_gain':
            # Hypertrophy, focus on Upper/Lower split elements
            work_duration = 50
            rest_duration = 20
            priority_groups = ['chest', 'back', 'legs', 'shoulders']
            candidates = base_exercises.filter(muscle_group__in=priority_groups)
            if candidates.count() < 5:
                candidates = base_exercises
        else: # maintenance
            candidates = base_exercises

        # Select 5 exercises
        candidate_list = list(candidates)
        if len(candidate_list) > 5:
            selected_exercises_objs = random.sample(candidate_list, 5)
        else:
            selected_exercises_objs = candidate_list
        
    # Build Sequence
    # Format: {'type': 'exercise|rest|warmup', 'name': '', 'duration': seconds, 'description': ''}
    sequence = []
    
    # Warmup
    sequence.append({
        'type': 'warmup',
        'name': _("Échauffement articulaire"),
        'duration': 60,
        'description': _("Rotations des bras, poignets, chevilles et hanches.")
    })
    
    for ex in selected_exercises_objs:
        # Exercise
        sequence.append({
            'type': 'exercise',
            'name': ex.name,
            'duration': work_duration,
            'description': ex.description,
            'image': ex.image_url or ''
        })
        # Rest
        sequence.append({
            'type': 'rest',
            'name': _("Récupération"),
            'duration': rest_duration,
            'description': _("Respirez profondément. Préparez-vous pour la suite.")
        })
        
    # Cooldown
    sequence.append({
        'type': 'cooldown',
        'name': _("Retour au calme"),
        'duration': 60,
        'description': _("Étirements légers et respiration.")
    })
    
    # Post-Workout Nutrition Recommendation
    # Select a Shake or Snack, preferably high protein
    post_workout_meal = Recipe.objects.filter(category__in=['shake', 'snack']).order_by('?').first()
    if not post_workout_meal:
        post_workout_meal = Recipe.objects.order_by('?').first()
    
    return render(request, 'web/workout_session.html', {
        'sequence': sequence,
        'total_time': sum(s['duration'] for s in sequence) // 60,
        'post_workout_meal': post_workout_meal
    })

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
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'web/register.html', {'form': form})

def blog_list(request):
    """
    Liste des articles de blog.
    Supporte la recherche textuelle et le filtrage par catégorie.
    """
    # Update Streak if reading blog
    if request.user.is_authenticated and hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    articles = Article.objects.filter(is_published=True)
    categories = Category.objects.all()
    
    # Search
    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query) | articles.filter(content__icontains=query)
        
    # Filter by Category
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        
    articles = articles.order_by('-created_at').distinct()
    
    return render(request, 'web/blog_list.html', {
        'articles': articles,
        'categories': categories,
        'current_category': category_slug,
        'search_query': query
    })

def article_detail(request, slug):
    """
    Lecture d'un article complet.
    Permet de liker et de commenter.
    Affiche des articles similaires en bas de page.
    """
    # Update Streak if reading article
    if request.user.is_authenticated and hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    article = get_object_or_404(Article, slug=slug, is_published=True)
    comments = article.comments.order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, _("Commentaire ajouté."))
            return redirect('article_detail', slug=slug)
    else:
        form = CommentForm()
        
    is_liked = False
    if request.user.is_authenticated:
        is_liked = article.likes.filter(id=request.user.id).exists()
        
    # Related Articles (Same Category, Exclude Current, Limit 3)
    related_articles = []
    if article.category:
        related_articles = Article.objects.filter(
            category=article.category, 
            is_published=True
        ).exclude(id=article.id).order_by('-created_at')[:3]
        
    return render(request, 'web/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'related_articles': related_articles
    })

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Ensure user is the author of the comment
    if request.user == comment.author:
        article_slug = comment.article.slug
        comment.delete()
        messages.success(request, _("Commentaire supprimé."))
        return redirect('article_detail', slug=article_slug)
    else:
        messages.error(request, _("Vous n'êtes pas autorisé à supprimer ce commentaire."))
        return redirect('article_detail', slug=comment.article.slug)

@login_required(login_url='login')
def like_article(request, slug):
    # Like action also counts for streak
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    article = get_object_or_404(Article, slug=slug)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article_detail', slug=slug)

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

@login_required(login_url='login')
def planner_view(request):
    # Update Streak on Planner Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    plans = request.user.plans.order_by('-created_at')
    latest_plan = plans.first()
    
    if request.method == 'POST':
        form = WellnessPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            
            # Génération du plan via le service
            workout, nutrition, score = generate_wellness_plan(
                plan.age, plan.gender, plan.height, plan.weight, plan.goal, plan.activity_level
            )
            
            plan.workout_plan = workout
            plan.nutrition_plan = nutrition
            plan.save()
            
            # Mise à jour des stats utilisateur
            if hasattr(request.user, 'stats'):
                request.user.stats.health_score = score
                
                # Update breakdown scores from analysis
                if 'analysis' in workout and 'breakdown' in workout['analysis']:
                    breakdown = workout['analysis']['breakdown']
                    request.user.stats.fitness_score = breakdown.get('fitness', 0)
                    request.user.stats.recovery_score = breakdown.get('recovery', 0)
                    request.user.stats.lifestyle_score = breakdown.get('lifestyle', 0)
                    request.user.stats.consistency_score = breakdown.get('consistency', 0)
                
                # Gamification: +100 XP for taking action
                request.user.stats.xp += 100
                # Level Up Logic: Every 500 XP is a level
                request.user.stats.level = 1 + (request.user.stats.xp // 500)
                
                # Update Streak (Explicit update on action)
                request.user.stats.update_streak()
                
                request.user.stats.save()
                
            messages.success(request, _(f"Plan généré ! +100 XP (Niveau {request.user.stats.level})"))
            return redirect('planner')
    else:
        if latest_plan:
            # Pre-fill form with latest plan data
            initial_data = {
                'age': latest_plan.age,
                'gender': latest_plan.gender,
                'height': latest_plan.height,
                'weight': latest_plan.weight,
                'goal': latest_plan.goal,
                'activity_level': latest_plan.activity_level,
            }
            form = WellnessPlanForm(initial=initial_data)
        else:
            form = WellnessPlanForm()

    return render(request, 'web/planner.html', {'plan': latest_plan, 'plans': plans, 'form': form})


@login_required(login_url='login')
def custom_planner_view(request):
    # Update Streak
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    events = request.user.custom_events.order_by('start_time')
    
    # Organize by day for the template
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekly_events = {day: [] for day in days}
    for event in events:
        if event.day_of_week in weekly_events:
            weekly_events[event.day_of_week].append(event)
            
    if request.method == 'POST':
        form = CustomEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, _("Activité ajoutée au planning !"))
            return redirect('custom_planner')
    else:
        form = CustomEventForm()
        
    return render(request, 'web/custom_planner.html', {
        'form': form,
        'weekly_events': weekly_events,
        'days': days
    })

@login_required(login_url='login')
def delete_custom_event(request, event_id):
    event = get_object_or_404(CustomEvent, id=event_id, user=request.user)
    event.delete()
    messages.success(request, _("Activité supprimée."))
    return redirect('custom_planner')

@login_required(login_url='login')
@require_POST
def complete_custom_event(request, event_id):
    event = get_object_or_404(CustomEvent, id=event_id, user=request.user)
    
    if not event.is_completed:
        event.is_completed = True
        event.save()
        
        # Gamification Logic
        xp_gain = 50 # Base XP
        if event.priority == 'high':
            xp_gain = 100
        elif event.priority == 'medium':
            xp_gain = 75
            
        request.user.stats.add_xp(xp_gain)
        
        return JsonResponse({
            'status': 'success',
            'xp_gain': xp_gain,
            'new_xp': request.user.stats.xp,
            'new_level': request.user.stats.level,
            'message': _("Tâche complétée ! +%(xp)s XP") % {'xp': xp_gain}
        })
        
    return JsonResponse({'status': 'already_completed'})

@login_required(login_url='login')
def tools_view(request):
    # Update Streak on Tools Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = None
    # We can assume user is authenticated due to decorator, but keeping check is harmless or we can simplify.
    # request.user.plans access requires authenticated user essentially.
    latest_plan = request.user.plans.order_by('-created_at').first()
        
    return render(request, 'web/tools.html', {'plan': latest_plan})

def legal_view(request):
    """
    Page des mentions légales et conditions d'utilisation.
    """
    return render(request, 'web/legal.html')

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


@login_required(login_url='login')
@require_POST
def complete_workout(request):
    """
    API endpoint to record a completed workout session.
    Awards XP, updates streak, and logs entry in DailyLog.
    """
    # 1. Award XP and Update Streak
    xp_gain = 100
    if hasattr(request.user, 'stats'):
        request.user.stats.add_xp(xp_gain)
        request.user.stats.update_streak()
    
    # 2. Add entry to Daily Log
    today_log, created = DailyLog.objects.get_or_create(user=request.user, date=timezone.now().date())
    timestamp = timezone.now().strftime("%H:%M")
    log_entry = f"[{timestamp}] { _('Séance Coach IA terminée') } (+{xp_gain} XP)"
    
    if today_log.notes:
        today_log.notes += f"\n{log_entry}"
    else:
        today_log.notes = log_entry
    today_log.save()
    
    return JsonResponse({
        'status': 'success',
        'xp_gain': xp_gain,
        'new_xp': request.user.stats.xp,
        'new_level': request.user.stats.level,
        'message': _("Mission accomplie ! +%(xp)s XP") % {'xp': xp_gain}
    })

# -----------------------------------------------------------------------------
# WORKOUT TRACKING
# -----------------------------------------------------------------------------
@login_required(login_url='login')
def start_workout(request):
    """
    Page pour démarrer une nouvelle séance d'entraînement.
    Vérifie qu'il n'y a pas de session active avant de créer une nouvelle.
    """
    active_session = WorkoutSession.objects.filter(user=request.user, status='active').first()
    
    if active_session:
        messages.warning(request, _("Vous avez déjà une séance en cours. Terminez-la d'abord."))
        return redirect('workout_session_detail', session_id=active_session.id)
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        session = WorkoutSession.objects.create(user=request.user, notes=notes)
        messages.success(request, _("Séance démarrée ! Bon entraînement ! 💪"))
        return redirect('workout_session_detail', session_id=session.id)
    
    latest_plan = request.user.plans.order_by('-created_at').first()
    suggested_exercises = Exercise.objects.all()[:6]
    
    return render(request, 'web/workout/start.html', {
        'suggested_exercises': suggested_exercises,
        'latest_plan': latest_plan
    })

@login_required(login_url='login')
def workout_session(request, session_id):
    """
    Page de la séance en cours.
    Affiche le timer, les exercices effectués et permet d'ajouter des sets.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        messages.warning(request, _("Cette séance est déjà terminée."))
        return redirect('workout_history')
    
    exercises = Exercise.objects.all().order_by('muscle_group', 'name')
    
    sets_by_exercise = {}
    for exercise_set in session.sets.select_related('exercise').order_by('created_at'):
        ex_name = exercise_set.exercise.name
        if ex_name not in sets_by_exercise:
            sets_by_exercise[ex_name] = []
        sets_by_exercise[ex_name].append(exercise_set)
    
    return render(request, 'web/workout/session.html', {
        'session': session,
        'exercises': exercises,
        'sets_by_exercise': sets_by_exercise,
        'total_sets': session.sets.count()
    })

@login_required(login_url='login')
@require_POST
def add_set_to_session(request, session_id):
    """
    API endpoint pour ajouter un set à une session active (Ajax).
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        return JsonResponse({'error': 'Session non active'}, status=400)
    
    try:
        exercise_id = int(request.POST.get('exercise_id'))
        reps = int(request.POST.get('reps'))
        weight = float(request.POST.get('weight'))
        rest_seconds = int(request.POST.get('rest_seconds', 60))
        notes = request.POST.get('notes', '')
        
        exercise = get_object_or_404(Exercise, id=exercise_id)
        
        last_set = session.sets.filter(exercise=exercise).order_by('-set_number').first()
        set_number = (last_set.set_number + 1) if last_set else 1
        
        exercise_set = ExerciseSet.objects.create(
            session=session,
            exercise=exercise,
            set_number=set_number,
            reps=reps,
            weight=weight,
            rest_seconds=rest_seconds,
            notes=notes
        )
        
        return JsonResponse({
            'status': 'success',
            'set': {
                'id': exercise_set.id,
                'exercise_name': exercise.name,
                'set_number': set_number,
                'reps': reps,
                'weight': weight,
                'volume': exercise_set.volume,
                'rest_seconds': rest_seconds
            },
            'total_sets': session.sets.count()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required(login_url='login')
@require_POST
def complete_workout_session(request, session_id):
    """
    Terminer une séance d'entraînement.
    Calcule les stats et attribue l'XP.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    if session.status != 'active':
        return JsonResponse({'error': 'Session déjà terminée'}, status=400)
    
    session.complete_session()
    
    from api.services_badges import check_and_award_badges
    new_badges = check_and_award_badges(request.user)
    
    xp_earned = 50 + (session.duration_minutes // 10) * 10
    
    return JsonResponse({
        'status': 'success',
        'message': _("Séance terminée avec succès ! 🎉"),
        'xp_earned': xp_earned,
        'duration_minutes': session.duration_minutes,
        'total_volume': round(session.total_volume, 2),
        'total_sets': session.sets.count(),
        'redirect_url': '/workout/history/'
    })

@login_required(login_url='login')
def workout_history(request):
    """
    Historique des séances d'entraînement.
    Affiche toutes les sessions complétées avec statistiques.
    """
    sessions = WorkoutSession.objects.filter(
        user=request.user,
        status='completed'
    ).prefetch_related('sets__exercise').order_by('-started_at')
    
    # Calculate overall stats
    total_sessions = sessions.count()
    total_volume = sum(s.total_volume for s in sessions)
    total_duration = sum(s.duration_minutes for s in sessions)
    
    # Recent sessions for charts (last 10)
    recent_sessions = sessions[:10]
    chart_dates = [s.started_at.strftime('%d/%m') for s in reversed(list(recent_sessions))]
    chart_volume = [s.total_volume for s in reversed(list(recent_sessions))]
    chart_duration = [s.duration_minutes for s in reversed(list(recent_sessions))]
    
    return render(request, 'web/workout/history.html', {
        'sessions': sessions[:20],  # Show last 20 sessions
        'total_sessions': total_sessions,
        'total_volume': round(total_volume, 2),
        'total_duration': total_duration,
        'avg_duration': round(total_duration / total_sessions, 2) if total_sessions > 0 else 0,
        'avg_volume': round(total_volume / total_sessions, 2) if total_sessions > 0 else 0,
        'chart_dates': chart_dates,
        'chart_volume': chart_volume,
        'chart_duration': chart_duration
    })

@login_required(login_url='login')
def workout_detail(request, session_id):
    """
    Détails d'une séance spécifique.
    """
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    
    # Group sets by exercise
    sets_by_exercise = {}
    for exercise_set in session.sets.select_related('exercise').order_by('created_at'):
        ex_name = exercise_set.exercise.name
        if ex_name not in sets_by_exercise:
            sets_by_exercise[ex_name] = {
                'exercise': exercise_set.exercise,
                'sets': [],
                'total_volume': 0
            }
        sets_by_exercise[ex_name]['sets'].append(exercise_set)
        sets_by_exercise[ex_name]['total_volume'] += exercise_set.volume
    
    return render(request, 'web/workout/detail.html', {
        'session': session,
        'sets_by_exercise': sets_by_exercise
    })

@login_required(login_url='login')
def analytics_view(request):
    """
    Page analytics avancées avec tous les graphiques de progression.
    """
    from django.db.models import Max, Sum, Count
    from datetime import timedelta
    
    # Global workout stats
    completed_sessions = WorkoutSession.objects.filter(user=request.user, status='completed')
    total_workouts = completed_sessions.count()
    total_volume = sum(s.total_volume for s in completed_sessions)
    total_duration = sum(s.duration_minutes for s in completed_sessions)
    
    # Weight progression (from daily logs)
    weight_logs = request.user.daily_logs.filter(weight__isnull=False).order_by('date')[:30]
    weight_dates = [log.date.strftime('%d/%m') for log in weight_logs]
    weight_values = [log.weight for log in weight_logs]
    
    # Volume by muscle group
    muscle_volume = {}
    for session in completed_sessions:
        for exercise_set in session.sets.select_related('exercise'):
            muscle = exercise_set.exercise.get_muscle_group_display()
            if muscle not in muscle_volume:
                muscle_volume[muscle] = 0
            muscle_volume[muscle] += exercise_set.volume
    
    muscle_labels = list(muscle_volume.keys())
    muscle_values = list(muscle_volume.values())
    
    # Personal Records (PR) - Max weight per exercise
    personal_records = []
    all_sets = ExerciseSet.objects.filter(session__user=request.user, session__status='completed').select_related('exercise')
    
    exercises_with_sets = {}
    for exercise_set in all_sets:
        ex_name = exercise_set.exercise.name
        if ex_name not in exercises_with_sets:
            exercises_with_sets[ex_name] = []
        exercises_with_sets[ex_name].append(exercise_set)
    
    for ex_name, sets in exercises_with_sets.items():
        max_weight = max(s.weight for s in sets)
        max_volume = max(s.volume for s in sets)
        personal_records.append({
            'exercise_name': ex_name,
            'max_weight': max_weight,
            'max_volume': max_volume
        })
    
    personal_records = sorted(personal_records, key=lambda x: x['max_weight'], reverse=True)[:10]
    
    # Workout frequency (last 7 days)
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    frequency_data = {}
    for day in last_7_days:
        day_name = day.strftime('%A')
        count = completed_sessions.filter(started_at__date=day).count()
        if day_name not in frequency_data:
            frequency_data[day_name] = 0
        frequency_data[day_name] += count
    
    frequency_labels = list(frequency_data.keys())
    frequency_values = list(frequency_data.values())
    
    # Consistency score (workouts in last 30 days / expected)
    last_30_days = completed_sessions.filter(started_at__gte=today - timedelta(days=30)).count()
    expected_workouts = 12
    consistency_score = min(int((last_30_days / expected_workouts) * 100), 100)
    
    # XP progression (if we track it historically - for now use current)
    xp_progression = True
    xp_dates = ['Semaine 1', 'Semaine 2', 'Semaine 3', 'Semaine 4']
    xp_values = [request.user.stats.xp // 4, request.user.stats.xp // 2, request.user.stats.xp * 3 // 4, request.user.stats.xp]
    
    return render(request, 'web/analytics.html', {
        'total_workouts': total_workouts,
        'total_volume': total_volume,
        'total_duration': total_duration,
        'weight_data': len(weight_dates) > 0,
        'weight_dates': weight_dates,
        'weight_values': weight_values,
        'muscle_volume_data': len(muscle_labels) > 0,
        'muscle_labels': muscle_labels,
        'muscle_values': muscle_values,
        'personal_records': personal_records,
        'frequency_labels': frequency_labels,
        'frequency_values': frequency_values,
        'consistency_score': consistency_score,
        'xp_progression': xp_progression,
        'xp_dates': xp_dates,
        'xp_values': xp_values
    })

# -----------------------------------------------------------------------------
# ONBOARDING
# -----------------------------------------------------------------------------
@login_required(login_url='login')
def onboarding_welcome(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    return render(request, 'web/onboarding/welcome.html')

@login_required(login_url='login')
def onboarding_step1(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        request.session['onboarding_goal'] = request.POST.get('goal')
        return redirect('onboarding_step2')
    
    return render(request, 'web/onboarding/step1_goal.html')

@login_required(login_url='login')
def onboarding_step2(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        request.session['onboarding_activity'] = request.POST.get('activity_level')
        return redirect('onboarding_step3')
    
    return render(request, 'web/onboarding/step2_level.html')

@login_required(login_url='login')
def onboarding_step3(request):
    if request.user.is_onboarded:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from api.services import generate_wellness_plan
        from api.services_badges import check_and_award_badges
        
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = int(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        goal = request.session.get('onboarding_goal', 'maintenance')
        activity_level = request.session.get('onboarding_activity', 'moderate')
        
        workout_plan, nutrition_plan, health_score = generate_wellness_plan(
            age=age, gender=gender, height=height, weight=weight,
            goal=goal, activity_level=activity_level
        )
        
        plan = WellnessPlan.objects.create(
            user=request.user,
            age=age, gender=gender, height=height, weight=weight,
            goal=goal, activity_level=activity_level,
            workout_plan=workout_plan,
            nutrition_plan=nutrition_plan
        )
        
        if hasattr(request.user, 'stats'):
            request.user.stats.health_score = health_score['total']
            request.user.stats.fitness_score = health_score['fitness']
            request.user.stats.recovery_score = health_score['recovery']
            request.user.stats.lifestyle_score = health_score['lifestyle']
            request.user.stats.add_xp(50)
            request.user.stats.update_streak()
            request.user.stats.save()
        
        from api.services_badges import check_and_award_badges
        new_badges = check_and_award_badges(request.user)
        
        request.user.is_onboarded = True
        request.user.save()
        
        request.session.pop('onboarding_goal', None)
        request.session.pop('onboarding_activity', None)
        
        return render(request, 'web/onboarding/complete.html', {
            'plan': plan,
            'new_badges': new_badges
        })
    
    return render(request, 'web/onboarding/step3_data.html')

# -----------------------------------------------------------------------------
# LEADERBOARD
# -----------------------------------------------------------------------------
@login_required(login_url='login')
def leaderboard_view(request):
    """
    Page de classement global des utilisateurs.
    """
    from django.db.models import Count, Sum
    
    # Top 10 XP
    top_xp = User.objects.select_related('stats').order_by('-stats__xp')[:10]
    
    # Top 10 Streaks
    top_streak = User.objects.select_related('stats').order_by('-stats__current_streak')[:10]
    
    # Top 10 Workouts (count + volume)
    users_with_workouts = User.objects.annotate(
        workout_count=Count('workout_sessions', filter=models.Q(workout_sessions__status='completed')),
        total_volume=Sum('workout_sessions__total_volume', filter=models.Q(workout_sessions__status='completed'))
    ).filter(workout_count__gt=0).order_by('-workout_count')[:10]
    
    # User ranks
    all_users_xp = list(User.objects.select_related('stats').order_by('-stats__xp').values_list('id', flat=True))
    all_users_streak = list(User.objects.select_related('stats').order_by('-stats__current_streak').values_list('id', flat=True))
    
    user_rank_xp = all_users_xp.index(request.user.id) + 1 if request.user.id in all_users_xp else 0
    user_rank_streak = all_users_streak.index(request.user.id) + 1 if request.user.id in all_users_streak else 0
    
    user_workouts = WorkoutSession.objects.filter(user=request.user, status='completed').count()
    users_workout_counts = list(User.objects.annotate(
        workout_count=Count('workout_sessions', filter=models.Q(workout_sessions__status='completed'))
    ).filter(workout_count__gte=user_workouts).values_list('id', flat=True))
    user_rank_workouts = len(users_workout_counts)
    
    return render(request, 'web/leaderboard.html', {
        'top_xp': top_xp,
        'top_streak': top_streak,
        'top_workouts': users_with_workouts,
        'user_rank_xp': user_rank_xp,
        'user_rank_streak': user_rank_streak,
        'user_rank_workouts': user_rank_workouts
    })
