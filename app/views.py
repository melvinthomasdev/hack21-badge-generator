from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
# import numpy as np

from .forms import ImageUploadForm

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root)
template_url = root + staticfiles_storage.url("img\spar.jpg")
fontname_url = root + staticfiles_storage.url('fonts\Lobster_1_4.otf')
# circle_image_url = root
template = Image.open(template_url)

# def generate_badge(src):
#     thumbimg = Image.open('timg.jpg')
#     reqht = 592
#     reqwd = int((thumbimg.width/thumbimg.height)*592)
#     thumbimg = thumbimg.resize((reqwd, reqht))
#     width, height = thumbimg.size
#     left = (width - 468)/2
#     top = (height - 592)/2
#     right = (width + 468)/2
#     bottom = (height + 592)/2
#     thumbimg = thumbimg.crop((left, top, right, bottom))
    
#     print(thumbimg.size)
#     image_copy = template.copy()
#     position = (298, 282)
#     image_copy.paste(thumbimg, position)
#     image_copy.save('pasted_image.png')

def get_fontsize(image, txt,fraction=2.0):
    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = float(fraction)

    font = ImageFont.truetype(fontname_url, fontsize)
    while font.getsize(txt)[0] < img_fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(fontname_url, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(fontname_url, fontsize)
    return fontsize

def index_view(request):
    context = {}
    response = HttpResponse(content_type='image/png')
    # filename = 'proud_volunteer'
    if request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                src_img = request.FILES.get("image")
                name = form.cleaned_data.get('name').title()
                # context['img'] = src_img
                thumbimg = Image.open(src_img)
                reqht = 262
                reqwd = int((thumbimg.width/thumbimg.height)*262)
                thumbimg = thumbimg.resize((reqwd, reqht))
                width, height = thumbimg.size
                left = (width - 262)/2
                top = (height - 262)/2
                right = (width + 262)/2
                bottom = (height + 262)/2
                thumbimg = thumbimg.crop((left, top, right, bottom))
                # im_square = crop_max_square(thumbimg).resize((reqwd, reqwd), Image.LANCZOS)
                # thumbimg = mask_circle_transparent(im_square, 0)
                # thumbimg.save('circle.png')
                # thumbimg = Image.open('circle.png')
                # thumbimg.save(response, 'png')
                thumbimg = thumbimg.resize((262, 262))
                bigsize = (thumbimg.size[0] * 3, thumbimg.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask) 
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(thumbimg.size, Image.ANTIALIAS)
                thumbimg.putalpha(mask)
                output = ImageOps.fit(thumbimg, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                # output.save('output.png')
                print(thumbimg.size)
                image_copy = template.copy()
                image_copy.convert("RGBA")
                position = (315, 260)
                image_copy.paste(thumbimg, position, thumbimg)
                draw = ImageDraw.Draw(image_copy)
                # name = "john".title()
                fontsize = get_fontsize(thumbimg, name)
                fontsize = 80 if fontsize>80 else fontsize
                print('font size',fontsize)
                # (x, y) = (79,970)
                if fontsize<40:
                    fontsize = get_fontsize(thumbimg, name, 2.3)
                    print("After adjusting:", fontsize)
                    # (x, y) = (79, 970)
                font = ImageFont.truetype(fontname_url, size=fontsize)
                color = 'rgb(000,000,000)' # white color
                strip_width, strip_height = 875, 100
                label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
                draw = ImageDraw.Draw(label)
                label.putalpha(1)
                draw = ImageDraw.Draw(label)
                text_width, text_height = draw.textsize(name, font)
                position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                draw.text(position, name, color, font=font)
                name_position = (0,622)
                image_copy.paste(label, name_position, label)
                # image_copy.save('pasted_image.png')
                response['Content-Disposition'] = 'attachment; filename=%s.png' % name
                image_copy.save(response, 'png')
                return response
        else:
            context['form'] = form
    else:
        context['form'] = ImageUploadForm()
    return render(request, 'index.html', context)


