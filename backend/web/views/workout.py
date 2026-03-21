from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import random
from web.forms import CustomWorkoutForm
from api.models import Exercise, WorkoutSession, ExerciseSet, DailyLog, Recipe
from api.services.gamification import check_and_award_badges
from django.utils import timezone

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
    post_workout_meal = Recipe.objects.filter(category__in=['shake', 'snack']).order_by('?').first()
    if not post_workout_meal:
        post_workout_meal = Recipe.objects.order_by('?').first()
    
    return render(request, 'web/workout_session.html', {
        'sequence': sequence,
        'total_time': sum(s['duration'] for s in sequence) // 60,
        'post_workout_meal': post_workout_meal
    })

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
