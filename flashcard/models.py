from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name
    
class Flashcard(models.Model):
    DIFFICULTE_CHOICES = (('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=100)
    response = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    difficulte = models.CharField(max_length=1, choices=DIFFICULTE_CHOICES)
    def __str__(self):
        return self.question
    @property
    def css_difficulte(self):
        if self.difficulte == 'F':
            return 'flashcard-facil'
        elif self.difficulte == 'M':
            return 'flashcard-medio'
        elif self.difficulte == 'D':
            return 'flashcard-dificil'

class FlashcardChallenge(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    answered = models.BooleanField(default=False)
    got_it_right = models.BooleanField(default=False)
    def __str__(self):
        return self.flashcard.question
    
class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    quantity_questions = models.IntegerField()
    difficulte = models.CharField(
    max_length=1, choices=Flashcard.DIFFICULTE_CHOICES
    )
    flashcards = models.ManyToManyField(FlashcardChallenge)
    def __str__(self):
        return self.title