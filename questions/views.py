from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from.forms import QuestionForm, AnswerForm
from .models import Question
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'questions/index.html', {})

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            # return ("question", question_id=question.pk)
            return HttpResponseRedirect(reverse('question', args=(question.id,)))
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form' : form})

def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return HttpResponseRedirect(reverse('question', args=(question.id,)))
    else:
        form = AnswerForm()
        
    return render(request, 'questions/question.html', {'question': question, 'form' : form}, )