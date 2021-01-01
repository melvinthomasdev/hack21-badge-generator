from django import forms

class ImageUploadForm(forms.Form):
    image = forms.FileField(required=True)
    class Meta:
        fields = ('image')