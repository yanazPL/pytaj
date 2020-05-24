from django.forms import ModelForm
from questions.models import Question, Answer

# Create the form class.
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content']