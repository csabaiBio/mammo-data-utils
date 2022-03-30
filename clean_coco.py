import json
from PIL import Image, ImageDraw
import os
import pathlib
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ExifTags
import numpy as np
import copy
from tqdm import tqdm

with open('./coco_json/sote_mammo_emk.json', 'r') as f:
    datastore = json.load(f)

id2cat = {_id : cat for cat, _id in datastore['cat2id'].items()}

cleaned_datastore = copy.deepcopy(datastore)
cleaned_datastore['images'] = []
cleaned_datastore['annotations'] = []

for img in tqdm(datastore['images']):
    image_id = img['id']

    bboxes = []
    annotations = []
    for ann in datastore['annotations']:
        if ann['image_id'] == image_id:
            annotations.append(ann)
            bboxes.append((ann['bbox'], id2cat[ann['category_id']]))

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
        # cases: image don't have exif
        pass

    height, width = image.size

    valid_bbox_indices = []

    for ind, (bbox, cat) in enumerate(bboxes):
        crop_mean = np.array(image.crop((bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]))).mean()

        if crop_mean < 80:
            pass
        else:
            valid_bbox_indices.append(ind)

    cleaned_datastore["images"].append(img)
    cleaned_datastore["annotations"].extend([annotations[_ind_] for _ind_ in valid_bbox_indices])
    
    del image

with open('./coco_json/cleaned_sote_mammo_emk.json', 'w') as fp:
    json.dump(cleaned_datastore, fp, sort_keys=True, indent=4)