from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Avg, Sum, Count, F, Q
from datetime import timedelta
from web.forms import DailyLogForm
from api.models import DailyLog, WorkoutSession, User, ExerciseSet, Exercise

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
            request.user.stats.add_xp(20)
            messages.success(request, _("Journal mis à jour ! +20 XP"))
            return redirect('dashboard')
    else:
        form = DailyLogForm(instance=today_log)
        
    # Recent Activity / Stats (optimisé)
    week_logs = request.user.daily_logs.only('sleep_hours', 'water_liters', 'date').order_by('-date')[:7]
    avg_sleep = week_logs.aggregate(Avg('sleep_hours'))['sleep_hours__avg'] or 0
    avg_water = week_logs.aggregate(Avg('water_liters'))['water_liters__avg'] or 0
    
    # Chart Data (Last 30 days) - optimisé
    recent_logs = request.user.daily_logs.only('date', 'weight', 'sleep_hours', 'mood').order_by('-date')[:30]
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
def analytics_view(request):
    """
    Page analytics avancées avec tous les graphiques de progression.
    Calcule et prépare les données pour Chart.js.
    """
    user = request.user
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    # 1. GLOBAL STATS
    total_workouts = WorkoutSession.objects.filter(user=user, status='completed').count()
    
    global_stats = WorkoutSession.objects.filter(user=user, status='completed').aggregate(
        total_vol=Sum('total_volume'),
        total_time=Sum('duration_minutes')
    )
    total_volume = global_stats['total_vol'] or 0
    total_duration = global_stats['total_time'] or 0
    
    # Consistency Score
    logs_dates = set(DailyLog.objects.filter(user=user, date__gte=last_30_days).values_list('date', flat=True))
    workouts_dates = set(WorkoutSession.objects.filter(user=user, started_at__date__gte=last_30_days, status='completed').values_list('started_at__date', flat=True))
    active_days = len(logs_dates.union(workouts_dates))
    consistency_score = int((active_days / 30) * 100)
    
    if hasattr(user, 'stats') and user.stats.consistency_score != consistency_score:
        user.stats.consistency_score = consistency_score
        user.stats.save()

    # 2. WEIGHT PROGRESSION
    weight_logs = DailyLog.objects.filter(
        user=user, 
        weight__isnull=False,
        date__gte=last_30_days
    ).order_by('date')
    
    weight_dates = [log.date.strftime('%d/%m') for log in weight_logs]
    weight_values = [log.weight for log in weight_logs]

    # 3. VOLUME BY MUSCLE GROUP
    muscle_volume = ExerciseSet.objects.filter(
        session__user=user,
        session__status='completed'
    ).values('exercise__muscle_group').annotate(
        volume=Sum(F('weight') * F('reps'))
    ).order_by('-volume')
    
    muscle_labels_map = dict(Exercise.MUSCLE_CHOICES)
    muscle_labels = [muscle_labels_map.get(item['exercise__muscle_group'], item['exercise__muscle_group']) for item in muscle_volume]
    muscle_values = [item['volume'] for item in muscle_volume]

    # 4. PERSONAL RECORDS (PR)
    top_exercises_ids = ExerciseSet.objects.filter(
        session__user=user,
        session__status='completed'
    ).values('exercise').annotate(
        count=Count('id')
    ).order_by('-count')[:6].values_list('exercise', flat=True)
    
    personal_records = []
    for ex_id in top_exercises_ids:
        exercise = Exercise.objects.get(id=ex_id)
        max_weight = ExerciseSet.objects.filter(
            session__user=user, 
            exercise=exercise,
            session__status='completed'
        ).aggregate(Max('weight'))['weight__max'] or 0
        
        max_vol_set = ExerciseSet.objects.filter(
            session__user=user, 
            exercise=exercise,
            session__status='completed'
        ).annotate(
            vol=F('weight') * F('reps')
        ).order_by('-vol').first()
        max_volume = max_vol_set.vol if max_vol_set else 0
        
        personal_records.append({
            'exercise_name': exercise.name,
            'max_weight': max_weight,
            'max_volume': max_volume
        })

    # 5. WORKOUT FREQUENCY
    start_week = today - timedelta(days=6)
    workouts_this_week = WorkoutSession.objects.filter(
        user=user,
        started_at__date__gte=start_week,
        status='completed'
    ).count()
    
    rest_days = 7 - workouts_this_week
    frequency_labels = ['Entraînement', 'Repos']
    frequency_values = [workouts_this_week, rest_days]

    # 6. XP PROGRESSION
    xp_dates = []
    xp_values = []
    
    current_xp = user.stats.xp
    xp_dates.append(today.strftime('%d/%m'))
    xp_values.append(current_xp)
    
    if user.date_joined.date() > last_30_days:
        xp_dates.insert(0, user.date_joined.date().strftime('%d/%m'))
        xp_values.insert(0, 0)

    context = {
        'total_workouts': total_workouts,
        'total_volume': total_volume,
        'total_duration': total_duration,
        'consistency_score': consistency_score,
        'weight_dates': weight_dates,
        'weight_values': weight_values,
        'weight_data': len(weight_values) > 1,
        'muscle_labels': muscle_labels,
        'muscle_values': muscle_values,
        'muscle_volume_data': len(muscle_values) > 0,
        'personal_records': personal_records,
        'frequency_labels': frequency_labels,
        'frequency_values': frequency_values,
        'xp_dates': xp_dates,
        'xp_values': xp_values,
        'xp_progression': len(xp_values) > 1
    }
    
    return render(request, 'web/analytics.html', context)

@login_required(login_url='login')
def leaderboard_view(request):
    """
    Page de classement global des utilisateurs.
    """
    # Top 10 XP (optimisé avec only)
    top_xp = User.objects.select_related('stats').only('username', 'stats__xp', 'stats__level').order_by('-stats__xp')[:10]
    
    # Top 10 Streaks (optimisé avec only)
    top_streak = User.objects.select_related('stats').only('username', 'stats__current_streak', 'stats__level').order_by('-stats__current_streak')[:10]
    
    # Top 10 Workouts
    users_with_workouts = User.objects.annotate(
        workout_count=Count('workout_sessions', filter=Q(workout_sessions__status='completed')),
        total_volume=Sum('workout_sessions__total_volume', filter=Q(workout_sessions__status='completed'))
    ).filter(workout_count__gt=0).order_by('-workout_count')[:10]
    
    # User ranks (optimisé - seulement IDs)
    all_users_xp = list(User.objects.order_by('-stats__xp').values_list('id', flat=True))
    all_users_streak = list(User.objects.order_by('-stats__current_streak').values_list('id', flat=True))
    
    user_rank_xp = all_users_xp.index(request.user.id) + 1 if request.user.id in all_users_xp else 0
    user_rank_streak = all_users_streak.index(request.user.id) + 1 if request.user.id in all_users_streak else 0
    
    user_workouts = WorkoutSession.objects.filter(user=request.user, status='completed').count()
    users_workout_counts = list(User.objects.annotate(
        workout_count=Count('workout_sessions', filter=Q(workout_sessions__status='completed'))
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
