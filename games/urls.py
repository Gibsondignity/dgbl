from django.urls import path
from . import views

urlpatterns = [
    path('game-list', views.game_list, name='game_list'),
    path('quiz-list', views.stem_quiz_list, name='quiz_list'),
    path('puzzle-game', views.puzzle_level_select, name='puzzle_game'),
    path('matching-game', views.matching_level_select, name='matching_game'),
    path('spelling-game', views.spelling_level_select, name='spelling_game'),

    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('game/submit/', views.submit_game, name='submit_game'),

    
    path('puzzle-game/<int:level_id>/', views.puzzle_game, name='puzzle_game_with_level'),
    path('matching-game/<int:level_id>/', views.matching_game, name='matching_game_with_level'),
    path('spelling-game/<int:level_id>/', views.spelling_game, name='spelling_game_with_level'),
    path('quiz/<str:category>/', views.quiz_level_select, name='quiz_category_detail'),
    path('quiz/<str:category>/<int:level_id>/', views.start_quiz, name='start_quiz_with_level'),
    path('puzzle/random/?#random-puzzle-fun-game/', views.get_random_puzzle, name='get_random_puzzle'),
    path('api/get-random-matching/?#random-matchin-fun-game', views.get_random_matching, name='get_random_matching'),
    path('api/get-random-spelling/?#random-spelling-fun-game', views.get_random_spelling, name='get_random_spelling'),
    
    path('my-scores', views.my_scores, name='my_scores'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/result/', views.game_result, name='game_result'),
    path('<int:game_id>/play/', views.play_game, name='game_play'),
]
