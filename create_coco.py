import os
import numpy as np
import json
import datetime
from PIL import Image
from pathlib import Path


class COCOJsonConverter:
    def __init__(self, annotation_path, dataset_name):
        self.info = {
            "year": str(datetime.datetime.now().year),
            "version": "1.0",
            "description":
            "COCO-like dataset for mammography",
            "url": "http://olaralex.com",
            "date_created": str(datetime.datetime.now())
        }
        self.licenses = [{
            "id":
            1,
            "name":
            "Attribution-NonCommercial",
            "url":
            "http://creativecommons.org/licenses/by-nc-sa/2.0/"
        }]
        self.images = []
        self.annotations = []
        self.categories = []

        self.cat2id = {}

        self.annotation_data = json.load(open(annotation_path, 'r'))
        self.dataset_name = dataset_name

    def _build_categories(self):
        category_names = set()
        for record_id, values in self.annotation_data.items():
            for slice_id, annotations in values.items():
                for annotation in annotations:
                    if annotation['category'] == 'Egyéb':
                        continue
                    else:
                        category_names.add(annotation['category'])

        category_names = sorted(list(category_names))

        for ind, cat in enumerate(category_names):
            self.categories.append({'id' : ind, 'supercategory': cat, 'name': cat})
            self.cat2id[cat] = ind

    def _build_images(self):
        for record_id, values in self.annotation_data.items():
            for slice_id, annotations in values.items():
                if len(annotations) == 0:
                    continue

                img_path = annotations[0]['image_path']

                if img_path.endswith('.dcm'):
                    img_path = img_path.replace('.dcm', '.png')

                img = Image.open(img_path)
                w, h = img.size

                image = {
                    "license": 1,
                    "path": img_path,
                    "file_name": f"{str(Path(img_path).stem)}{str(Path(img_path).suffix)}",
                    "coco_url": "",
                    "height": h,
                    "width": w,
                    "date_captured": str(datetime.datetime.now()),
                    "flickr_url": "",
                    "id": str(Path(img_path).stem)
                }
                self.images.append(image)

    def _build_annotations(self):
        annotation_id = 0
        for record_id, values in self.annotation_data.items():
            for slice_id, annotations in values.items():
                for annotation in annotations:
                    if annotation['category'] == 'Egyéb':
                        continue

                    bbox = [annotation['x'], annotation['y'], annotation['width'], annotation['height']]
                    anno = {
                        # (x0, y0),
                        # (x1, y0),
                        # (x1, y1),
                        # (x0, y1)
                        "segmentation": [[bbox[0], bbox[1],
                                        bbox[0] + \
                                        bbox[2], bbox[1],
                                        bbox[0] + \
                                        bbox[2], bbox[1] + \
                                        bbox[3],
                                        bbox[0], bbox[1] + bbox[3]]],
                        "area": bbox[2] * bbox[3],
                        "iscrowd": 0,
                        "image_id": str(Path(annotations[0]['image_path'].replace('.dcm', '.jpg')).stem),
                        "bbox": bbox,
                        "category_id": self.cat2id[annotation['category']],
                        "id": annotation_id
                    }
                    annotation_id += 1
                    self.annotations.append(anno)

    def create_coco_json(self):
        self._build_categories()
        self._build_images()
        self._build_annotations()
        coco_output = {
            "info": self.info,
            "licenses": self.licenses,
            "categories": self.categories,
            "images": self.images,
            "annotations": self.annotations,
            "cat2id": self.cat2id
        }
        with open("coco_json/" + self.dataset_name + ".json",
                  "w") as output_json_file:
            json.dump(coco_output, output_json_file, indent=4)


if __name__ == "__main__":
    coco_json = COCOJsonConverter('./annotations.json', 'sote_mammo_emk')
    coco_json.create_coco_json()