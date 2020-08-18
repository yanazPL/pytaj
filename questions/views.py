from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from questions import common
from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required


def index(request):
    questions = Question.objects.order_by('-date')
    return render(request, 'questions/index.html', {'questions': questions})


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
    return render(request, 'questions/ask.html', {'form': form})


class QuestionDetail(FormMixin, SingleObjectMixin, ListView):
    template_name = 'questions/question.html'
    form_class = AnswerForm
    pk_url_kwarg = 'question_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Question.objects.all())
        return super().get(request, *args, **kwargs)

    def get_ordering(self):
        return self.request.GET.get('ordering', '-date')

    def get_queryset(self):
        queryset = self.object.answers.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
        queryset = queryset.order_by(*ordering)
        return queryset

    def form_valid(self, form):
        pass


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


class AnyVote(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            answer_id = request.POST.get('answer_id')
            if answer_id:
                answer = get_object_or_404(Answer, pk=answer_id)
                if self.votes_action(answer, request.user.id):
                    return JsonResponse({"valid": True}, status=200)
                else:
                    return JsonResponse({"valid": False}, status=200)
            else:
                return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({}, status=400)

    def votes_action(self, answer, user_id):
        pass


class Upvote(AnyVote):
    def votes_action(self, answer, user_id):
        answer.author.stats.karma += 1
        if common.votes_down_exists(answer, user_id):
            answer.auth.stats.karma += 1
        answer.author.stats.save()
        return answer.votes.up(user_id)


class Downvote(AnyVote):
    def votes_action(self, answer, user_id):
        answer.author.stats.karma -= 1
        if common.votes_up_exists(answer, user_id):
            answer.author.stats.karma -= 1
        answer.author.stats.save()
        return answer.votes.down(user_id)


class Unvote(AnyVote):
    def votes_action(self, answer, user_id):
        if common.votes_down_exists(answer, user_id):
            answer.author.stats.karma += 1
        elif common.votes_up_exists(answer, user_id):
            answer.author.stats.karma -= 1
        answer.author.stats.save()
        return answer.votes.delete(user_id)
        # TODO consider answer.sco


class Search(View):
    def get(self, request, *args, **kwargs):
        questions_list = Question.objects.order_by("-date")

        if 'q' in request.GET:
            questions_list = questions_list.filter(title__icontains=request.GET['q'])

        return render(request, 'questions/search.html', {'questions': questions_list})
