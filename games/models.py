from django.db import models

# Create your models here.
# games/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone


User = get_user_model()

class GameCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# games/models.py
class Game(models.Model):
    GAME_TYPES = [
        ('quiz', 'Multiple Choice Quiz'),
        ('spelling', 'Spelling Game'),
        ('matching', 'Matching Pairs Game'),
        ('puzzle', 'Drag-and-Drop Puzzle'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(GameCategory, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, default='quiz')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='games/thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title


class GameSession(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)




class Quiz(models.Model):
    QUIZ_CATEGORIES = [
        ('Science', 'Science'),
        ('Math', 'Math'),
        ('Technology', 'Technology'),
        ('Engineering', 'Engineering'),
    ]
    title = models.CharField(max_length=200, null=True)
    category = models.CharField(choices=QUIZ_CATEGORIES, max_length=100, null=True)
    question_text = models.TextField(null=True)
    image = models.ImageField(upload_to='quiz_images/', null=True, blank=True)  # 👈 Add this line
    option_a = models.CharField(max_length=200, null=True)
    option_b = models.CharField(max_length=200, null=True)
    option_c = models.CharField(max_length=200, null=True)
    option_d = models.CharField(max_length=200, null=True)
    correct_option = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')], null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.category}"
    


class QuizScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    score = models.IntegerField()
    date_played = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.score}"
    




# models.py
class Puzzle(models.Model):
    PUZZLE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )
    type = models.CharField(max_length=10, choices=PUZZLE_TYPES)
    question = models.TextField()
    answer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='puzzles/', blank=True, null=True)
    options = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.question[:50]}..."


class MatchingItem(models.Model):
    category = models.CharField(max_length=50)  #
    term = models.CharField(max_length=100)     #
    match = models.CharField(max_length=100)    #
    image = models.ImageField(upload_to='matching/', blank=True, null=True)

    def __str__(self):
        return f"{self.term} ↔ {self.match}"
    


class SpellingItem(models.Model):
    word = models.CharField(max_length=100)
    image = models.ImageField(upload_to='spelling/', blank=True, null=True)
    audio = models.FileField(upload_to='spelling_audio/', blank=True, null=True)

    def __str__(self):
        return self.word
