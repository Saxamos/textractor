import codecs
import os

import pyocr.builders
from PIL import Image
from wand.image import Image as Img

dir = os.path.dirname(__file__)
pdfPath = os.path.join(dir, '../data/raw/')
srcName = '314018'
jpgPath = os.path.join(dir, '../data/raw/img/')

with Img(filename=pdfPath + srcName + '.pdf', resolution=300) as img:
    img.compression_quality = 100
    for i, image in enumerate(img.sequence[0:4]):
        jpgName = srcName + str(i + 1) + '.jpg'
        Img(image).save(filename=jpgPath + jpgName)

tool = pyocr.get_available_tools()[0]
langs = tool.get_available_languages()
lang = langs[0]
for i in range(0, 4):
    jpgName = srcName + str(i + 1) + '.jpg'
    text = tool.image_to_string(Image.open(jpgPath + jpgName), lang=lang,
                                builder=pyocr.builders.TextBuilder())
    with codecs.open(pdfPath + srcName + '.txt', 'a', encoding='utf-8') as file:
        file.write(text)
