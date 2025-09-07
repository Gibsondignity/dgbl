from django.contrib import admin
from .models import GameLevel, Game, GameSession, Quiz, Puzzle

# Register your models here.
admin.site.site_header = "DIGITAL GAME PLATFORM - ADMIN PANNEL"

admin.site.site_title = "Digital Game Platform Admin Portal"
admin.site.index_title = "Welcome to Digital Game Platform Admin Portal"


admin.site.register(GameLevel)
admin.site.register(Game)
admin.site.register(GameSession)
admin.site.register(Quiz)
admin.site.register(Puzzle)