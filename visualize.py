import json
from PIL import Image, ImageDraw
import os
import pathlib
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ExifTags
import numpy as np

font = font_manager.FontProperties(family='sans-serif', weight='bold')
file = font_manager.findfont(font)

home = pathlib.Path.home()

with open('./coco_json/sote_mammo_emk.json', 'r') as f:
    datastore = json.load(f)

id2cat = {_id : cat for cat, _id in datastore['cat2id'].items()}

for ind, img in enumerate(datastore['images']):
    image_id = img['id']

    print(image_id, end=' ')

    bboxes = []
    for ann in datastore['annotations']:
        if ann['image_id'] == image_id:
            bboxes.append((ann['bbox'], id2cat[ann['category_id']]))

    from PIL import Image, ImageFont, ImageDraw, ImageEnhance

    try:
        image=Image.open(img['path'])

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        
        exif = image._getexif()

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)

        image.save(filepath)
        image.close()
    except (AttributeError, KeyError, IndexError, TypeError) as e:
        # cases: image don't have getexi
        pass

    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype(file, 32, encoding="unic")

    height, width = image.size

    for bbox, cat in bboxes:
        draw.rectangle(((bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])), outline=255, width=8)
        draw.text((bbox[0], bbox[1]), cat, font=fnt, fill=(255), stroke_width=1)

        crop_mean = np.array(image.crop((bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]))).mean()

    if crop_mean < 100:
        image.save('./validation_pictures/%s' % f'{ind:03d}_HIBA_' + img['path'].split('/')[-1], "PNG")
    else:
        image.save('./validation_pictures/%s' % f'{ind:03d}_' + img['path'].split('/')[-1], "PNG")

    del draw
    del image

    if (ind + 1) % 100 == 0:
        print("%d images are processed." % (ind + 1))
        break