from django.urls import path
from . import views

urlpatterns = [
    path('game-list', views.game_list, name='game_list'),
    path('quiz-list', views.stem_quiz_list, name='quiz_list'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/play/', views.play_game, name='game_play'),
]
