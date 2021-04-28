from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from PIL import Image, ImageDraw, ImageFont
import os

from .forms import ImageUploadForm

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(root)
template_url = root + staticfiles_storage.url('img/sight.jpg')
fontname_url = root + staticfiles_storage.url('fonts/Montserrat-Regular.ttf')
template = Image.open(template_url)

def generate_badge(src):
    thumbimg = Image.open('timg.jpg')
    reqht = 592
    reqwd = int((thumbimg.width/thumbimg.height)*592)
    thumbimg = thumbimg.resize((reqwd, reqht))
    width, height = thumbimg.size
    left = (width - 468)/2
    top = (height - 592)/2
    right = (width + 468)/2
    bottom = (height + 592)/2
    thumbimg = thumbimg.crop((left, top, right, bottom))
    print(thumbimg.size)
    image_copy = template.copy()
    position = (298, 282)
    image_copy.paste(thumbimg, position)
    image_copy.save('pasted_image.png')

def get_fontsize(image, txt,fraction=1.0):
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
                reqht = 592
                reqwd = int((thumbimg.width/thumbimg.height)*592)
                thumbimg = thumbimg.resize((reqwd, reqht))
                width, height = thumbimg.size
                left = (width - 468)/2
                top = (height - 592)/2
                right = (width + 468)/2
                bottom = (height + 592)/2
                thumbimg = thumbimg.crop((left, top, right, bottom))
                print(thumbimg.size)
                image_copy = template.copy()
                image_copy.convert("RGBA")
                position = (298, 282)
                image_copy.paste(thumbimg, position)
                draw = ImageDraw.Draw(image_copy)
                # name = "john".title()
                fontsize = get_fontsize(thumbimg, name)
                fontsize = 80 if fontsize>80 else fontsize
                print('font size',fontsize)
                (x, y) = (79,970)
                if fontsize<35:
                    fontsize = get_fontsize(thumbimg, name, 1.3)
                    print("After adjusting:", fontsize)
                    (x, y) = (79, 970)
                font = ImageFont.truetype(fontname_url, size=fontsize)
                color = 'rgb(255,255,255)' # white color
                strip_width, strip_height = 482, 105
                label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
                draw = ImageDraw.Draw(label)
                label.putalpha(1)
                draw = ImageDraw.Draw(label)
                text_width, text_height = draw.textsize(name, font)
                position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                draw.text(position, name, color, font=font)
                name_position = (329,970)
                image_copy.paste(label, name_position, label)
                image_copy.save('pasted_image.png')
                response['Content-Disposition'] = 'attachment; filename=%s.png' % name
                image_copy.save(response, 'png')
                return response
        else:
            context['form'] = form
    else:
        context['form'] = ImageUploadForm()
    return render(request, 'index.html', context)







# from django.shortcuts import render
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.http import HttpResponse
# from wsgiref.util import FileWrapper

# from PIL import Image, ImageDraw, ImageFont
# import os

# from .forms import ImageUploadForm

# root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(root)
# template_url = root + staticfiles_storage.url('img/template.png')
# fontname_url = root + staticfiles_storage.url('fonts/Product-Sans-Bold.ttf')
# template = Image.open(template_url)

# def generate_badge(src):
#     thumbimg = Image.open('timg.jpg')
#     reqht = 480
#     reqwd = int((thumbimg.width/thumbimg.height)*480)
#     thumbimg = thumbimg.resize((reqwd, reqht))
#     width, height = thumbimg.size
#     left = (width - 360)/2
#     top = (height - 480)/2
#     right = (width + 360)/2
#     bottom = (height + 480)/2
#     thumbimg = thumbimg.crop((left, top, right, bottom))
#     print(thumbimg.size)
#     image_copy = template.copy()
#     position = (144, 401)
#     image_copy.paste(thumbimg, position)
#     image_copy.save('pasted_image.png')

# def get_fontsize(image, txt,fraction=1.0):
#     fontsize = 1  # starting font size

#     # portion of image width you want text width to be
#     img_fraction = float(fraction)

#     font = ImageFont.truetype(fontname_url, fontsize)
#     while font.getsize(txt)[0] < img_fraction*image.size[0]:
#         # iterate until the text size is just larger than the criteria
#         fontsize += 1
#         font = ImageFont.truetype(fontname_url, fontsize)

#     # optionally de-increment to be sure it is less than criteria
#     fontsize -= 1
#     font = ImageFont.truetype(fontname_url, fontsize)
#     return fontsize

# def index_view(request):
#     context = {}
#     response = HttpResponse(content_type='image/png')
#     # filename = 'proud_volunteer'
#     if request.POST:
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             if request.FILES:
#                 src_img = request.FILES.get("image")
#                 name = form.cleaned_data.get('name').title()
#                 # context['img'] = src_img
#                 thumbimg = Image.open(src_img)
#                 reqht = 480
#                 reqwd = int((thumbimg.width/thumbimg.height)*480)
#                 thumbimg = thumbimg.resize((reqwd, reqht))
#                 width, height = thumbimg.size
#                 left = (width - 360)/2
#                 top = (height - 480)/2
#                 right = (width + 360)/2
#                 bottom = (height + 480)/2
#                 thumbimg = thumbimg.crop((left, top, right, bottom))
#                 print(thumbimg.size)
#                 image_copy = template.copy()
#                 image_copy.convert("RGBA")
#                 position = (144, 401)
#                 image_copy.paste(thumbimg, position)
#                 draw = ImageDraw.Draw(image_copy)
#                 # name = "john".title()
#                 fontsize = get_fontsize(thumbimg, name)
#                 fontsize = 80 if fontsize>80 else fontsize
#                 print('font size',fontsize)
#                 (x, y) = (140,920)
#                 if fontsize<35:
#                     fontsize = get_fontsize(thumbimg, name, 1.3)
#                     print("After adjusting:", fontsize)
#                     (x, y) = (83, 892)
#                 font = ImageFont.truetype(fontname_url, size=fontsize)
#                 color = 'rgb(255,255,255)' # white color
#                 strip_width, strip_height = 482, 105
#                 label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
#                 draw = ImageDraw.Draw(label)
#                 label.putalpha(1)
#                 draw = ImageDraw.Draw(label)
#                 text_width, text_height = draw.textsize(name, font)
#                 position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
#                 draw.text(position, name, color, font=font)
#                 name_position = (83,892)
#                 image_copy.paste(label, name_position, label)
#                 image_copy.save('pasted_image.png')
#                 response['Content-Disposition'] = 'attachment; filename=%s.png' % name
#                 image_copy.save(response, 'png')
#                 return response
#         else:
#             context['form'] = form
#     else:
#         context['form'] = ImageUploadForm()
#     return render(request, 'index.html', context)






# from django.shortcuts import render
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.http import HttpResponse
# from wsgiref.util import FileWrapper

# from PIL import Image, ImageDraw, ImageFont
# import os

# from .forms import ImageUploadForm



# # def generate_badge(src):
# #     thumbimg = Image.open('timg.jpg')
# #     reqht = 480
# #     reqwd = int((thumbimg.width/thumbimg.height)*480)
# #     thumbimg = thumbimg.resize((reqwd, reqht))
# #     width, height = thumbimg.size
# #     left = (width - 360)/2
# #     top = (height - 480)/2
# #     right = (width + 360)/2
# #     bottom = (height + 480)/2
# #     thumbimg = thumbimg.crop((left, top, right, bottom))
# #     print(thumbimg.size)
# #     image_copy = template.copy()
# #     position = (144, 401)
# #     image_copy.paste(thumbimg, position)
# #     image_copy.save('pasted_image.png')

# # def get_fontsize(image, txt,fraction=1.0):
# #     fontsize = 1  # starting font size

# #     # portion of image width you want text width to be
# #     img_fraction = float(fraction)

# #     font = ImageFont.truetype(fontname_url, fontsize)
# #     while font.getsize(txt)[0] < img_fraction*image.size[0]:
# #         # iterate until the text size is just larger than the criteria
# #         fontsize += 1
# #         font = ImageFont.truetype(fontname_url, fontsize)

# #     # optionally de-increment to be sure it is less than criteria
# #     fontsize -= 1
# #     font = ImageFont.truetype(fontname_url, fontsize)
# #     return fontsize


# root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(root)
# template_url = root + staticfiles_storage.url('img/sight.jpg')
# fontname_url = root + staticfiles_storage.url('fonts/Montserrat-Regular.ttf')
# template = Image.open(template_url)


# def get_fontsize(image, txt,fraction=1.0):
#     fontsize = 1  # starting font size
#     # portion of image width you want text width to be
#     img_fraction = float(fraction)
#     font = ImageFont.truetype('Montserrat-Regular.ttf', fontsize)
#     while font.getsize(txt)[0] < img_fraction*image.size[0]:
#         # iterate until the text size is just larger than the criteria
#         fontsize += 1
#         font = ImageFont.truetype('Montserrat-Regular.ttf', fontsize)

#     fontsize = 80 if fontsize>80 else fontsize
#     if fontsize<35:
#         fontsize = get_fontsize(image, txt, 1.4)
#     return fontsize

# def create_label(text, hacker_img):
#     fontsize = get_fontsize(hacker_img, text)
#     font = ImageFont.truetype('Montserrat-Regular.ttf', size=fontsize)
#     color = 'rgb(255,255,255)' # Red Color
#     strip_width, strip_height = 900, 80
#     text_label = Image.new("RGBA", (strip_width,strip_height), (0,0,0,0))
#     draw = ImageDraw.Draw(text_label)
#     text_width, text_height = draw.textsize(text, font)
#     position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
#     draw.text(position, text, color, font=font)
#     return text_label





# def index_view(request):
#     context = {}
#     response = HttpResponse(content_type='image/png')
#     # filename = 'proud_volunteer'
#     if request.POST:
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             if request.FILES:
#                 src_img = request.FILES.get("image")
#                 name = form.cleaned_data.get('name').title()
#                 # context['img'] = src_img
#                 hacker_img = Image.open(src_img)
#                 reqht = 592  #446
#                 reqwd = int((hacker_img.width / hacker_img.height) * 592)
#                 hacker_img = hacker_img.resize((reqwd, reqht))
#                 print(hacker_img.size)

#                 width, height = hacker_img.size
#                 left = (width - 468) / 2
#                 top = (height - 592) / 2
#                 right = (width + 468) / 2
#                 bottom = (height + 592) / 2
#                 hacker_img = hacker_img.crop((left, top, right, bottom))

#                 template_copy = template.copy()
#                 # position= (336,210)
#                 position = (298, 282)  #topleft corner
#                 template_copy.paste(hacker_img, position)

#                 # name = input("Enter Your Name:").title()
#                 name_label = create_label(name, hacker_img)
#                 name_position = (79, 970)
#                 template_copy.paste(name_label, name_position, name_label)
#                 template_copy.save('output.png')
#                 # image_copy.save('pasted_image.png')
#                 response['Content-Disposition'] = 'attachment; filename=%s.png' % name
#                 template_copy.save(response, 'png')
#                 return response
#         else:
#             context['form'] = form
#     else:
#         context['form'] = ImageUploadForm()
#     return render(request, 'index.html', context)

