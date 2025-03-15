from django.forms import ModelForm, TextInput, Textarea, Select
from .models import Collection

class Create_Collection_Form(ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'lang', 'user']
        widgets = {
            'name':TextInput(attrs={'class':'form-input'}),
            'description':Textarea(attrs={'class':'form-input desc-input'}),
            'lang':Select(attrs={'class':'form-input form-select'}),
            'user':Select(attrs={'class':'form-input form-select'}),
            }