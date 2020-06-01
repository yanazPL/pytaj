from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect, HttpResponse
from.forms import QuestionForm, AnswerForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required

def index(request):
    questions = Question.objects.order_by('-date')
    return render(request, 'questions/index.html', {'questions' : questions})

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return HttpResponseRedirect(reverse('question', args=(question.id,)))
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form' : form})

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm()
        
    return render(request, 'questions/question.html', {'question': question, 'form' : form},)

@login_required
def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(request.POST) if request.method == 'POST' else AnswerForm()
    if form.is_valid():
        answer = form.save(commit=False)
        answer.author = request.user
        answer.question = question
        answer.save()
    return HttpResponseRedirect(reverse('question', args=(question.id,)))

def upvote(request):
    if request.is_ajax and request.method == "POST":
        answer_id = request.POST.get('answer_id')
        if answer_id:
            answer = get_object_or_404(Answer, pk=answer_id)
            answer.votes.up(request.user.id)
            return HttpResponse("w drugim ifie")
        return HttpResponse("w pierwszym ifie")
    else:
        return HttpResponse("poza ifami")
        
        
