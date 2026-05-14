"""
Dashboard Admin custom (séparé de Django admin /admin/).

Accessible aux super-utilisateurs uniquement (is_superuser=True).
URL: /en/admin-panel/

Features:
- Liste tous les utilisateurs avec : last_login, last_login_ip, user_agent, login_count, sessions actives
- Toggle masquage (is_hidden)
- Suppression définitive
- Recherche + tri
- Stats temps réel (total users, actifs aujourd'hui, sessions ouvertes)
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db.models import Q
from datetime import timedelta
from api.models import User


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def _active_sessions_for_user(user_id: int) -> int:
    """Compte les sessions actives (non expirées) d'un utilisateur."""
    now = timezone.now()
    count = 0
    for s in Session.objects.filter(expire_date__gte=now):
        data = s.get_decoded()
        if str(data.get('_auth_user_id')) == str(user_id):
            count += 1
    return count


@user_passes_test(is_superuser, login_url='login')
def admin_panel(request):
    """Vue principale du dashboard admin custom."""
    q = request.GET.get('q', '').strip()
    show_hidden = request.GET.get('show_hidden') == '1'

    users_qs = User.objects.all().order_by('-last_login', '-date_joined')

    if not show_hidden:
        users_qs = users_qs.filter(is_hidden=False)

    if q:
        users_qs = users_qs.filter(
            Q(username__icontains=q) | Q(email__icontains=q) | Q(last_login_ip__icontains=q)
        )

    # Annoter chaque user avec ses sessions actives (calcul Python car Session est dans une autre DB logique)
    users = list(users_qs[:200])  # limite raisonnable
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    sessions_active = Session.objects.filter(expire_date__gte=now)
    active_user_ids = set()
    for s in sessions_active:
        uid = s.get_decoded().get('_auth_user_id')
        if uid:
            active_user_ids.add(int(uid))

    for u in users:
        u.is_online = u.id in active_user_ids
        u.active_sessions = _active_sessions_for_user(u.id) if u.is_online else 0

    # Stats globales
    stats = {
        'total': User.objects.count(),
        'active_today': User.objects.filter(last_login__gte=today_start).count(),
        'online_now': len(active_user_ids),
        'hidden': User.objects.filter(is_hidden=True).count(),
        'verified': User.objects.filter(is_verified=True).count(),
        'staff': User.objects.filter(is_staff=True).count(),
    }

    return render(request, 'web/admin_panel.html', {
        'users': users,
        'stats': stats,
        'q': q,
        'show_hidden': show_hidden,
    })


@user_passes_test(is_superuser, login_url='login')
def admin_toggle_hide(request, user_id: int):
    """Toggle is_hidden — masque ou réaffiche un utilisateur."""
    if request.method != 'POST':
        return redirect('admin_panel')
    target = get_object_or_404(User, id=user_id)
    if target.is_superuser and target != request.user:
        messages.error(request, _("Impossible de masquer un autre super-utilisateur."))
        return redirect('admin_panel')
    target.is_hidden = not target.is_hidden
    target.save(update_fields=['is_hidden'])
    state = _("masqué") if target.is_hidden else _("réaffiché")
    messages.success(request, _("L'utilisateur %(u)s a été %(s)s.") % {'u': target.username, 's': state})
    return redirect('admin_panel')


@user_passes_test(is_superuser, login_url='login')
def admin_delete_user(request, user_id: int):
    """Supprime définitivement un utilisateur (sauf super-users autres que soi-même)."""
    if request.method != 'POST':
        return redirect('admin_panel')
    target = get_object_or_404(User, id=user_id)
    if target.is_superuser and target != request.user:
        messages.error(request, _("Impossible de supprimer un autre super-utilisateur."))
        return redirect('admin_panel')
    if target == request.user:
        messages.error(request, _("Tu ne peux pas te supprimer toi-même via le dashboard admin. Utilise la page profil."))
        return redirect('admin_panel')
    username = target.username
    target.delete()
    messages.success(request, _("L'utilisateur %(u)s a été supprimé définitivement.") % {'u': username})
    return redirect('admin_panel')
