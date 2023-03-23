from django import forms
from .models import Document
from django.forms import FileInput

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
    
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget = FileInput(attrs={
                'id': 'file-upload',
                'class': 'input-file'
            })