from django.db import models

# Create your models here.
# games/models.py

from django.db import models
from django.contrib.auth import get_user_model

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
    category = models.CharField(choices=QUIZ_CATEGORIES, max_length=100, null=True)  # or use CharField if no model
    question_text = models.TextField(null=True)
    option_a = models.CharField(max_length=200, null=True)
    option_b = models.CharField(max_length=200, null=True)
    option_c = models.CharField(max_length=200, null=True)
    option_d = models.CharField(max_length=200, null=True)
    correct_option = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')], null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.category}"