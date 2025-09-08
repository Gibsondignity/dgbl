from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Game, QuizScore, Quiz, Puzzle, MatchingItem, SpellingItem, GameLevel, GameSession
from django.http import JsonResponse
import random
from django.utils import timezone


@login_required
def game_list(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    category = request.GET.get('category')
    level_id = request.GET.get('level')

    if category and level_id:
        games = Game.objects.filter(is_active=True, game_type=category, level_id=level_id)
        level_name = GameLevel.objects.get(id=level_id).name
    elif category:
        # Show level selection for the category
        levels = GameLevel.objects.all()
        return render(request, 'games/level_select.html', {
            'category': category,
            'levels': levels
        })
    else:
        games = None  # Show categories if no filter
        level_name = None

    return render(request, 'games/game_list.html', {
        'games': games,
        'category': category,
        'level_id': level_id,
        'level_name': level_name
    })


@login_required
def game_detail(request, game_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    game = get_object_or_404(Game, id=game_id)
    level_id = request.GET.get('level')
    return render(request, 'games/game_detail.html', {'game': game, 'level_id': level_id})



@login_required
def play_game(request, game_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    game = get_object_or_404(Game, id=game_id)
    level_id = request.GET.get('level')
    return render(request, 'games/play_game.html', {'game': game, 'level_id': level_id})



# STEM QUIZ CATEGORIES 
@login_required
def stem_quiz_list(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    return render(request, 'games/quiz/stem_quiz_list.html', {})

@login_required
def quiz_level_select(request, category):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    levels = GameLevel.objects.all()
    return render(request, 'games/quiz/quiz_level_select.html', {
        'category': category,
        'levels': levels
    })



@login_required
def submit_quiz(request):
    print(f"DEBUG: submit_quiz called with method: {request.method}")
    print(f"DEBUG: POST data keys: {list(request.POST.keys()) if request.POST else 'None'}")
    print(f"DEBUG: Session keys: {list(request.session.keys())}")
    print(f"DEBUG: quiz_questions in session: {request.session.get('quiz_questions', [])}")

    if request.method == 'POST':
        category = request.POST.get('category')
        question_ids = request.session.get('quiz_questions', [])

        print(f"DEBUG: category = {category}")
        print(f"DEBUG: question_ids = {question_ids}")

        # Debug: Check if session data exists
        if not question_ids:
            print("DEBUG: No questions in session, redirecting to quiz list")
            # If no questions in session, redirect back to quiz list
            return render(request, 'games/quiz/stem_quiz_list.html', {
                'error': 'Quiz session expired. Please start a new quiz.'
            })

        score = 0
        results = []

        for qid in question_ids:
            try:
                quiz = Quiz.objects.get(id=qid)
                selected = request.POST.get(f'q{quiz.id}')
                print(f"DEBUG: Question {qid}, selected = {selected}, correct = {quiz.correct_option}")
                is_correct = selected and selected == quiz.correct_option
                if is_correct:
                    score += 1
                results.append({
                    'question': quiz.question_text,
                    'selected': selected,
                    'correct': quiz.correct_option,
                    'correct_text': getattr(quiz, f'option_{quiz.correct_option.lower()}'),
                    'explanation': quiz.explanation,
                    'is_correct': is_correct
                })
            except Quiz.DoesNotExist:
                print(f"DEBUG: Quiz {qid} not found")
                continue

        # Get level from session
        level_id = request.session.get('quiz_level_id')
        level_name = None
        if level_id:
            try:
                level = GameLevel.objects.get(id=level_id)
                level_name = level.name
            except GameLevel.DoesNotExist:
                level_id = None

        # Save score with user
        try:
            QuizScore.objects.create(
                user=request.user,
                category=category,
                score=score,
                date_played=now()
            )
            print(f"DEBUG: Score saved successfully: {score}")
        except Exception as e:
            print(f"DEBUG: Error saving score: {e}")
            # Continue to show results even if save fails

        # Clear session data after successful submission
        if 'quiz_questions' in request.session:
            del request.session['quiz_questions']
        if 'quiz_level_id' in request.session:
            del request.session['quiz_level_id']
        if 'quiz_category' in request.session:
            del request.session['quiz_category']
        if 'quiz_start_time' in request.session:
            del request.session['quiz_start_time']

        print(f"DEBUG: Returning quiz results with score {score}/{len(question_ids)}")
        return render(request, 'games/quiz/quiz_result.html', {
            'score': score,
            'total': len(question_ids),
            'category': category,
            'results': results,
            'percentage': (score / len(question_ids)) * 100 if question_ids else 0,
            'level_name': level_name
        })
    else:
        print("DEBUG: Not a POST request, redirecting to quiz list")
        # If not POST, redirect to quiz list
        return render(request, 'games/quiz/stem_quiz_list.html', {})





def start_quiz(request, category, level_id):
    quizzes = list(Quiz.objects.filter(category__iexact=category, is_active=True, level_id=level_id))
    if not quizzes:
        # Fallback to all quizzes if no level-specific ones exist
        quizzes = list(Quiz.objects.filter(category__iexact=category, is_active=True))

    random.shuffle(quizzes)
    quizzes = quizzes[:10]

    request.session['quiz_category'] = category
    request.session['quiz_level_id'] = level_id
    request.session['quiz_start_time'] = str(timezone.now())
    request.session['quiz_questions'] = [q.id for q in quizzes]

    level_name = GameLevel.objects.get(id=level_id).name
    return render(request, 'games/quiz/quiz_play.html', {
        'quizzes': quizzes,
        'category': category,
        'level_id': level_id,
        'level_name': level_name
    })




@login_required
def my_scores(request):
    scores = QuizScore.objects.filter(user=request.user).order_by('-date_played')
    return render(request, 'games/quiz/my_scores.html', {'scores': scores})



@login_required
def puzzle_level_select(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    levels = GameLevel.objects.all()
    return render(request, 'games/puzzle_level_select.html', {'levels': levels})

@login_required
def puzzle_game(request, level_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    level_name = GameLevel.objects.get(id=level_id).name
    return render(request, 'puzzle/puzzle_play.html', {'level_id': level_id, 'level_name': level_name})



@login_required
def get_random_puzzle(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")

    level_id = request.GET.get('level')
    if level_id:
        puzzles = list(Puzzle.objects.filter(level_id=level_id))
    else:
        puzzles = list(Puzzle.objects.all())

    if not puzzles:
        return JsonResponse({"error": "No puzzles available for this level."})

    puzzle = random.choice(puzzles)

    data = {
        "type": puzzle.type,
        "question": puzzle.question,
        "answer": puzzle.answer,
        "image": puzzle.image.url if puzzle.image else None,
        "options": puzzle.options if puzzle.options else [],
        "explanation": puzzle.explanation
    }
    return JsonResponse(data)






@login_required
def matching_level_select(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    levels = GameLevel.objects.all()
    return render(request, 'games/matching_level_select.html', {'levels': levels})

@login_required
def matching_game(request, level_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    level_name = GameLevel.objects.get(id=level_id).name
    return render(request, 'matching/matching_game.html', {'level_id': level_id, 'level_name': level_name})

@login_required
def spelling_level_select(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    levels = GameLevel.objects.all()
    return render(request, 'games/spelling_level_select.html', {'levels': levels})

@login_required
def spelling_game(request, level_id):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")

    level_name = GameLevel.objects.get(id=level_id).name
    return render(request, 'spelling/spelling_game.html', {'level_id': level_id, 'level_name': level_name})



@login_required
def get_random_matching(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")

    level_id = request.GET.get('level')
    if level_id:
        items = list(MatchingItem.objects.filter(level_id=level_id))
    else:
        items = list(MatchingItem.objects.all())

    if not items:
        return JsonResponse({"error": "No matching items available for this level."})

    selected = random.sample(items, min(4, len(items)))  # pick 4 for example
    data = [{"term": i.term, "match": i.match, "image": i.image.url if i.image else None, "explanation": i.explanation} for i in selected]
    return JsonResponse({"items": data})


@login_required
def get_random_spelling(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")

    level_id = request.GET.get('level')
    if level_id:
        items = list(SpellingItem.objects.filter(level_id=level_id))
    else:
        items = list(SpellingItem.objects.all())

    if not items:
        return JsonResponse({"error": "No spelling items available for this level."})

    item = random.choice(items)
    return JsonResponse({
        "word": item.word,
        "image": item.image.url if item.image else None,
        "audio": item.audio.url if item.audio else None,
        "explanation": item.explanation
    })


@login_required
def submit_game(request):
    if request.user.user_type != 'student':
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        game_type = request.POST.get('game_type')
        score = int(request.POST.get('score', 0))
        level_id = request.POST.get('level_id')

        # Save to GameSession
        try:
            game = Game.objects.filter(game_type=game_type).first()  # Assuming there's a game for the type
            if not game:
                # Create a dummy game if not exists
                game = Game.objects.create(
                    title=f"{game_type} Game",
                    description=f"Auto-created {game_type} game",
                    game_type=game_type,
                    level_id=level_id,
                    created_by=request.user
                )
            GameSession.objects.create(
                player=request.user,
                game=game,
                score=score,
                played_at=now()
            )
            print(f"DEBUG: Game score saved: {score} for {game_type}")
        except Exception as e:
            print(f"DEBUG: Error saving game score: {e}")

        # For now, just return success, or redirect to results
        return JsonResponse({"success": True, "message": "Score saved!"})
    else:
        return JsonResponse({"error": "Invalid method"})