from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from PIL import Image
import os

from .forms import ImageUploadForm

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root)
template_url = root + staticfiles_storage.url('img/template.png')
template = Image.open(template_url)

def generate_badge(src):
    thumbimg = Image.open('timg.jpg')
    reqht = 480
    reqwd = int((thumbimg.width/thumbimg.height)*480)
    thumbimg = thumbimg.resize((reqwd, reqht))
    width, height = thumbimg.size
    left = (width - 360)/2
    top = (height - 480)/2
    right = (width + 360)/2
    bottom = (height + 480)/2
    thumbimg = thumbimg.crop((left, top, right, bottom))
    print(thumbimg.size)
    image_copy = template.copy()
    position = (144, 401)
    image_copy.paste(thumbimg, position)
    image_copy.save('pasted_image.jpg')

def index_view(request):
    context = {}
    response = HttpResponse(content_type='image/png')
    filename = 'proud_volunteer'
    if request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                src_img = request.FILES.get("image")
                # context['img'] = src_img
                thumbimg = Image.open(src_img)
                reqht = 480
                reqwd = int((thumbimg.width/thumbimg.height)*480)
                thumbimg = thumbimg.resize((reqwd, reqht))
                width, height = thumbimg.size
                left = (width - 360)/2
                top = (height - 480)/2
                right = (width + 360)/2
                bottom = (height + 480)/2
                thumbimg = thumbimg.crop((left, top, right, bottom))
                print(thumbimg.size)
                image_copy = template.copy()
                position = (144, 401)
                image_copy.paste(thumbimg, position)
                # image_copy.save('pasted_image.jpg')
                response['Content-Disposition'] = 'attachment; filename=%s.png' % filename
                image_copy.save(response, 'png') # will call response.write()
                return response
        else:
            context['form'] = form
    else:
        context['form'] = ImageUploadForm()
    return render(request, 'index.html', context)




# response = HttpResponse(FileWrapper(myfile.getvalue()), content_type='application/zip')
# response['Content-Disposition'] = 'attachment; filename=myfile.zip'
# return response