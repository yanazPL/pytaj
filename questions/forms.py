from django.forms import ModelForm
from questions.models import Question, Answer

# Create the form class.
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        labels = {'title' : 'Tytuł', 'content' : 'Treść'}

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content' : 'Treść'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'answer-form-content'})