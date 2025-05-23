from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Game

@login_required
def game_list(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    category = request.GET.get('category')
    if category:
        games = Game.objects.filter(is_active=True, game_type=category)
    else:
        games = None  # Show categories if no filter
    
    return render(request, 'games/game_list.html', {'games': games, 'category': category})




@login_required
def game_detail(request, game_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'games/game_detail.html', {'game': game})



@login_required
def play_game(request, game_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'games/play_game.html', {'game': game})






# STEM QUIZ CATEGORIES 
@login_required
def stem_quiz_list(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    return render(request, 'games/quiz/stem_quiz_list.html', {})