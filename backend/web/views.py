from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomAuthenticationForm, WellnessPlanForm, CommentForm, UserUpdateForm, CustomPasswordChangeForm, CustomEventForm
from api.models import User, Article, Category, UserStats, WellnessPlan, Comment, CustomEvent
from api.services import generate_wellness_plan

def home(request):
    latest_plan = None
    if request.user.is_authenticated:
        latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/home.html', {'plan': latest_plan})

def login_view(request):
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
    logout(request)
    return redirect('home')

def register_view(request):
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

def tools_view(request):
    # Update Streak on Tools Visit
    if hasattr(request.user, 'stats'):
        request.user.stats.update_streak()
        
    latest_plan = request.user.plans.order_by('-created_at').first()
    return render(request, 'web/tools.html', {'plan': latest_plan})

def legal_view(request):
    return render(request, 'web/legal.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

