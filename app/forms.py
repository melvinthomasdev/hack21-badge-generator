from django import forms

class ImageUploadForm(forms.Form):
    # name = forms.CharField(max_length=35,required=True)
    # college_name = forms.CharField(max_length=50,required=True)
    image = forms.FileField(required=True)
    class Meta:
        fields = ('name', 'image')