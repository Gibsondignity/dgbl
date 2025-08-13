from django.urls import path
from . import views

urlpatterns = [
    path('game-list', views.game_list, name='game_list'),
    path('quiz-list', views.stem_quiz_list, name='quiz_list'),
    path('puzzle-game', views.puzzle_game, name='puzzle_game'),
    path('matching-game', views.matching_game, name='matching_game'),
    path('spelling-game', views.spelling_game, name='spelling_game'),
    path('quiz/<str:category>?#quiz-category-game/', views.start_quiz, name='quiz_category_detail'),
    path('puzzle/random/?#random-puzzle-fun-game/', views.get_random_puzzle, name='get_random_puzzle'),
    path('api/get-random-matching/?#random-matchin-fun-game', views.get_random_matching, name='get_random_matching'),
    path('api/get-random-spelling/?#random-spelling-fun-game', views.get_random_spelling, name='get_random_spelling'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('my-scores', views.my_scores, name='my_scores'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('<int:game_id>/play/', views.play_game, name='game_play'),
]
