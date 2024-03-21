from django.shortcuts import render
from flashcard.models import Challenge

# Create your views here.
def reports(request, id):
    challenge = Challenge.objects.get(id = id)
    hits = challenge.flashcards.filter(got_it_right = True).count()
    mistakes = challenge.flashcards.filter(got_it_right = False).count()
    data = [hits, mistakes]
    categories = challenge.category.all()
    categories_name = [i.name for i in categories]
    data2 = []
    for category in categories:
        data2.append(challenge.flashcards.filter(flashcard__category = category).filter(got_it_right = True).count())
    return render(request, 'report.html', {'challenge': challenge, 'data': data, 'categories': categories_name, 'data2': data2})