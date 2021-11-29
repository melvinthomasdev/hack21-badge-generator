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
template_url = root + staticfiles_storage.url(r'img\aisywlc.png')
fontname_url = root + staticfiles_storage.url(r'fonts\Roboto-Regular.ttf')
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

def get_fontsize(image, txt,fraction=1.7):
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
                name = " ".join(form.cleaned_data.get('name').title().split())
                # college_name = " ".join(form.cleaned_data.get('college_name').title().split())
                # context['img'] = src_img
                #width, height
                thumbimg = Image.open(src_img)
                img_width, img_height = thumbimg.size
                if thumbimg.width > thumbimg.height:
                    reqht = 209
                    reqwd = int((thumbimg.width/thumbimg.height)*209)
                if thumbimg.width < thumbimg.height:
                    reqwd = 209
                    reqht = int((thumbimg.height/thumbimg.width)*209)
                if thumbimg.width == thumbimg.height:
                    reqwd = reqht = 209

                thumbimg = thumbimg.resize((reqwd, reqht))
                width, height = thumbimg.size
                left = (width - 209)/2
                top = (height - 209)/2
                right = (width + 209)/2
                bottom = (height + 209)/2
                thumbimg = thumbimg.crop((left, top, right, bottom))
                # im_square = crop_max_square(thumbimg).resize((reqwd, reqwd), Image.LANCZOS)
                # thumbimg = mask_circle_transparent(im_square, 0)
                # thumbimg.save('circle.png')
                # thumbimg = Image.open('circle.png')
                # thumbimg.save(response, 'png')
                thumbimg = thumbimg.resize((209, 209))
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
                position = (320, 558) #(y, x)
                image_copy.paste(thumbimg, position, thumbimg)
                draw = ImageDraw.Draw(image_copy)
                # name = "john".title()



                name_fontsize = get_fontsize(thumbimg, name)
                name_fontsize = 38 if name_fontsize>38 else name_fontsize
                # name_fontsize=300
                print('font size',name_fontsize)
                # (x, y) = (79,970)
                # if name_fontsize<25:
                #     name_fontsize = get_fontsize(thumbimg, name, 1.7)
                #     print("After adjusting:", name_fontsize)
                    # (x, y) = (79, 970)
                font = ImageFont.truetype(fontname_url, size=name_fontsize)
                color = 'rgb(000,032,077)' # black color
                strip_width, strip_height = 445, 33
                name_label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
                draw = ImageDraw.Draw(name_label)
                name_label.putalpha(1)
                draw = ImageDraw.Draw(name_label)
                text_width, text_height = draw.textsize(name, font)
                position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                draw.text(position, name, color, font=font)
                name_position = (200,788)
                image_copy.paste(name_label, name_position, name_label)



                # college_name_fontsize = get_fontsize(thumbimg, college_name)
                # college_name_fontsize = 45 if college_name_fontsize>45 else college_name_fontsize
                # print('font size',college_name_fontsize)
                # # (x, y) = (79,970)
                # if college_name_fontsize<50:
                #     college_name_fontsize = get_fontsize(thumbimg, name, 2.3)
                #     print("After adjusting:", college_name_fontsize)
                #     # (x, y) = (79, 970)
                # font = ImageFont.truetype(fontname_url, size=college_name_fontsize)
                # color = 'rgb(000,000,000)' # white color
                # strip_width, strip_height = 822, 74
                # college_name_label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
                # draw = ImageDraw.Draw(college_name_label)
                # college_name_label.putalpha(1)
                # draw = ImageDraw.Draw(college_name_label)
                # text_width, text_height = draw.textsize(college_name, font)
                # position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                # draw.text(position, college_name, color, font=font)
                # college_name_position = (152,1446)
                # image_copy.paste(college_name_label, college_name_position, college_name_label)


                # image_copy.save('pasted_image.png')
                # response['Content-Disposition'] = 'attachment; filename=%s.png' % name
                response['Content-Disposition'] = 'attachment; filename=%s.png' % "IEEEXtreme Badge"
                image_copy.save(response, 'png')
                return response
        else:
            context['form'] = form
    else:
        context['form'] = ImageUploadForm()
    return render(request, 'index.html', context)
