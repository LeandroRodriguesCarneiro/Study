from django.shortcuts import render, redirect
from .models import Category, Flashcard, Challenge, FlashcardChallenge
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse, Http404

# Create your views here.
def new_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    
    if request.method == 'GET':
        categorys = Category.objects.all()
        difficultes = Flashcard.DIFFICULTE_CHOICES
        flashcards = Flashcard.objects.filter(user = request.user)
        category_filter = request.GET.get('categoria')
        difficulte_filter = request.GET.get('dificuldade')
        if category_filter:
            flashcards = flashcards.filter(category__id = category_filter)
        if difficulte_filter:
            flashcards = flashcards.filter(difficulte = difficulte_filter)
        return render(request, 'new_flashcard.html', {'categorys': categorys, 'difficultes': difficultes, 'flashcards': flashcards})
    
    elif request.method == 'POST':
        question = request.POST.get('pergunta')
        response = request.POST.get('resposta')
        category = request.POST.get('categoria')
        difficulte = request.POST.get('dificuldade')

        if len(question.strip()) == 0 or len(response.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha os campos de pergunta e resposta')
            return redirect('/flashcard/new_flashcard/')
        
        flashcard = Flashcard(
            user = request.user,
            question = question,
            response = response,
            category_id = category,
            difficulte = difficulte
        )

        flashcard.save()
        messages.add_message(request, constants.SUCCESS, 'Flashcard cadastrado com sucesso')
        return redirect('/flashcard/new_flashcard')

def delete_flashcard(request, id):
    flashcard = Flashcard.objects.get(id = id, user = request.user)
    flashcard.delete()
    messages.add_message(request, constants.SUCCESS, 'flashcard deletado com sucesso')
    return redirect('/flashcard/new_flashcard')

def start_challenge(request):
    if request.method == 'GET':
        categorys = Category.objects.all()
        difficultes = Flashcard.DIFFICULTE_CHOICES
        return render(request, 'start_challenge.html', {'categorys': categorys, 'difficultes': difficultes})
    elif request.method == "POST":
        title = request.POST.get('titulo')
        categorys = request.POST.getlist('categoria')
        difficulte = request.POST.get('dificuldade')
        quantity_questions = request.POST.get('qtd_perguntas')
        challenge = Challenge(
            user = request.user,
            title = title,
            difficulte = difficulte,
            quantity_questions = quantity_questions
        )
        print(challenge.difficulte)
        challenge.save()

        challenge.category.add(*categorys)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(difficulte=difficulte)
            .filter(category_id__in=categorys)
            .order_by('?')
        )
        
        if flashcards.count() < int(quantity_questions):
            messages.add_message(request, constants.WARNING, 'nao tem essa quantidade de flashcards')
            return redirect('/flashcard/start_challenge')
        
        flashcards = flashcards[:int(quantity_questions)]
        for f in flashcards:
            flashcard_challenge = FlashcardChallenge(
                flashcard = f
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)
        
        challenge.save()
        return redirect('/flashcard/list_challenge/')
    
def list_challenge(request):
    challenges = Challenge.objects.filter(user=request.user)
    categorys = Category.objects.all()
    difficultes = Flashcard.DIFFICULTE_CHOICES
    category_filter = request.GET.get('categoria')
    difficulte_filter = request.GET.get('dificuldade')
    if category_filter:
        challenges = challenges.filter(category__in=category_filter)
    if difficulte_filter:
        challenges = challenges.filter(difficulte = difficulte_filter)
    return render(
        request,
        'list_challenge.html',
        {
            'challenges': challenges,
            'categorys': categorys,
            'difficultes': difficultes
        },
    )

def challenge(request, id):
    challenge = Challenge.objects.get(id = id)
    if not challenge.user == request.user:
        raise Http404()
    if request.method == 'GET':
        categories = challenge.flashcards.values_list('flashcard__category__name', flat=True).distinct()
        got_it_right = challenge.flashcards.filter(answered = True).filter(got_it_right = True).count()
        miss = challenge.flashcards.filter(answered = True).filter(got_it_right = False).count()
        missing = challenge.flashcards.filter(answered = False).count()
        return render(request, 'challenge.html', {'challenge':challenge, 'got_it_right': got_it_right, 
                                                  'miss': miss, 'missing': missing, 'categories': categories})

def to_respond_flashcard(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    got_it_right = request.GET.get('acertou')
    challenge_id = request.GET.get('desafio_id')

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()

    flashcard_challenge.answered = True
    flashcard_challenge.got_it_right = True if got_it_right == '1' else False
    flashcard_challenge.save()
    return redirect(f'/flashcard/challenge/{challenge_id}')