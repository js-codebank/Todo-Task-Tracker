from django.forms import ModelForm
from .models import TodoNote

class TodoForm(ModelForm):
    class Meta:
        model = TodoNote
        fields = ['title','description','category']
