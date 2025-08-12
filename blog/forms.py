from .models import *

from django import forms


class EditBlog(forms.ModelForm):
    
    class Meta:
        model = Blog
        exclude = ('author',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'    
class AddBlog(forms.ModelForm):
    
    class Meta:
        model = Blog
        exclude = ('author',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'    


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ('user',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'    
