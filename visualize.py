import json
from PIL import Image, ImageDraw
import os
import pathlib
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

font = font_manager.FontProperties(family='sans-serif', weight='bold')
file = font_manager.findfont(font)

home = pathlib.Path.home()

with open('./coco_json/sote_mammo_emk.json', 'r') as f:
    datastore = json.load(f)

id2cat = {_id : cat for cat, _id in datastore['cat2id'].items()}

for ind, img in enumerate(datastore['images']):
    image_id = img['id']

    bboxes = []
    for ann in datastore['annotations']:
        if ann['image_id'] == image_id:
            bboxes.append((ann['bbox'], id2cat[ann['category_id']]))

    from PIL import Image, ImageFont, ImageDraw, ImageEnhance

    source_img = Image.open(img['path'])

    draw = ImageDraw.Draw(source_img)
    fnt = ImageFont.truetype(file, 32, encoding="unic")

    for bbox, cat in bboxes:
        draw.rectangle(((bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])), outline=255)
        draw.text((bbox[0], bbox[1]), cat, font=fnt, fill=(255), stroke_width=1)

    source_img.save('./validation_pictures/%s' % f'{ind:03d}_' + img['path'].split('/')[-1], "PNG")

    del draw
    del source_img

    if (ind + 1) % 150 == 0:
        print("%d images are processed." % (ind + 1))
        break