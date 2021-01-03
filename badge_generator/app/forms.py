from django import forms

class ImageUploadForm(forms.Form):
    image = forms.FileField(required=True)
    name = forms.CharField(max_length=35,required=True)
    class Meta:
        fields = ('name', 'image')