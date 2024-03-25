from django import forms

from .models import Blog
from ckeditor.fields import RichTextField

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)
    rating = forms.ChoiceField(label="Rating", choices=[(i, str(i)) for i in range(1, 6)], required=False)


class AddBlogForm(forms.ModelForm):
    description = RichTextField()
    
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "banner",
            "description"
        )