from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Game, QuizScore, Quiz, Puzzle, MatchingItem, SpellingItem
from django.http import JsonResponse
import random
from django.utils import timezone


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



@login_required
def submit_quiz(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        question_ids = request.session.get('quiz_questions', [])
        score = 0

        for qid in question_ids:
            quiz = Quiz.objects.get(id=qid)
            selected = request.POST.get(f'q{quiz.id}')
            if selected and selected == quiz.correct_option:
                score += 1

        # Save score with user
        QuizScore.objects.create(
            user=request.user,
            category=category,
            score=score,
            date_played=now()
        )

        return render(request, 'games/quiz/quiz_result.html', {
            'score': score,
            'total': len(question_ids),
            'category': category
        })





def start_quiz(request, category):
    quizzes = list(Quiz.objects.filter(category__iexact=category, is_active=True))
    random.shuffle(quizzes)
    quizzes = quizzes[:10]

    request.session['quiz_category'] = category
    request.session['quiz_start_time'] = str(timezone.now())
    request.session['quiz_questions'] = [q.id for q in quizzes]

    return render(request, 'games/quiz/quiz_play.html', {'quizzes': quizzes, 'category': category})




@login_required
def my_scores(request):
    scores = QuizScore.objects.filter(user=request.user).order_by('-date_played')
    return render(request, 'games/quiz/my_scores.html', {'scores': scores})



@login_required
def puzzle_game(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    return render(request, 'puzzle/puzzle_play.html', {})



@login_required
def get_random_puzzle(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")
    
    puzzles = Puzzle.objects.all()
    if not puzzles:
        return JsonResponse({"error": "No puzzles available."})

    puzzle = random.choice(puzzles)

    data = {
        "type": puzzle.type,
        "question": puzzle.question,
        "answer": puzzle.answer,
        "image": puzzle.image.url if puzzle.image else None,
        "options": puzzle.options if puzzle.options else []
    }
    return JsonResponse(data)






def matching_game(request):
    return render(request, 'matching/matching_game.html')

def spelling_game(request):
    return render(request, 'spelling/spelling_game.html')



@login_required
def get_random_matching(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")
    
    items = list(MatchingItem.objects.all())
    if not items:
        return JsonResponse({"error": "No matching items available."})
    
    selected = random.sample(items, min(4, len(items)))  # pick 4 for example
    data = [{"term": i.term, "match": i.match, "image": i.image.url if i.image else None} for i in selected]
    return JsonResponse({"items": data})


@login_required
def get_random_spelling(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")
    
    items = SpellingItem.objects.all()
    if not items:
        return JsonResponse({"error": "No spelling items available."})
    
    item = random.choice(items)
    return JsonResponse({
        "word": item.word,
        "image": item.image.url if item.image else None,
        "audio": item.audio.url if item.audio else None
    })