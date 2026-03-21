from .static import home, tools_view, legal_view, custom_404, custom_500
from .auth import login_view, logout_view, register_view, profile_view, edit_profile, change_password
from .dashboard import dashboard_view, analytics_view, leaderboard_view
from .planner import planner_view, custom_planner_view, delete_custom_event, complete_custom_event
from .content import exercise_library, recipe_list, recipe_detail, blog_list, article_detail, delete_comment, like_article
from .workout import workout_setup_view, workout_session_view, complete_workout, start_workout, workout_session, add_set_to_session, complete_workout_session, workout_history, workout_detail
from .onboarding import onboarding_welcome, onboarding_step1, onboarding_step2, onboarding_step3
