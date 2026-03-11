from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset Flow
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(
             template_name='web/password_reset_form.html',
             email_template_name='web/password_reset_email.html',
             form_class=CustomPasswordResetForm
         ), 
         name='password_reset'),
    path('reset_password/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='web/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='web/password_reset_confirm.html',
             form_class=CustomSetPasswordForm
         ), 
         name='password_reset_confirm'),
    path('reset_password/complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='web/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/like/', views.like_article, name='like_article'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Espace Membre
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('planner/', views.planner_view, name='planner'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('agenda/', views.custom_planner_view, name='custom_planner'),
    path('agenda/delete/<int:event_id>/', views.delete_custom_event, name='delete_custom_event'),
    path('agenda/complete/<int:event_id>/', views.complete_custom_event, name='complete_custom_event'),
    path('exercises/', views.exercise_library, name='exercise_library'),
    path('nutrition/', views.recipe_list, name='recipe_list'),
    path('nutrition/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('tools/', views.tools_view, name='tools'),
    
    # Pages Statiques
    path('legal/', views.legal_view, name='legal'),
]
