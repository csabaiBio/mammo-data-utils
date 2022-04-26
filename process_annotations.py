import json
from pprint import pprint

with open('data.json', 'r') as fp:
    data = json.load(fp)

annotations = {}

for _id_, record in data.items():
    annotations[_id_] = {}
    with open(record['annotations'], 'r') as fp:
        records = json.load(fp)
    if records is not None:
        ann = records.get('drawings', {})
        for rect in ann.get('children', []):
            if rect['attrs'].get('id') is None:
                continue
            slice_id = rect['attrs']['id']
            annotations[_id_][slice_id] =  []

error_ind = 0
n_annotations = 0

errors = {}

for _id_, record in data.items():
    if len(record["images"]) == 0:
        continue
    with open(record['annotations'], 'r') as fp:
        records = json.load(fp)
    if records is not None:
        ann = records.get('drawings', {})
        for rect in ann.get('children', []):
            if rect['attrs'].get('id') is None:
                continue
            slice_id = rect['attrs']['id']
            for bbox in rect.get('children', []):
                attrs = bbox.get('attrs', {})
                if not attrs.get('visible', False):
                    continue
                for bbox in bbox.get('children', []):
                    if bbox['className'] == 'Rect':
                        try:
                            x = bbox['attrs']['x']
                            y = bbox['attrs']['y']
                            width = bbox['attrs']['width']
                            height = bbox['attrs']['height']

                            label = bbox['attrs']['category']

                            image_path = list(filter(lambda value : str(slice_id) in value, record["images"]))

                            if len(record["images"]) == 1 and len(image_path) == 0:
                                image_path = record["images"]
                            elif len(record["images"]) == 0:
                                print('Error, no image')
                                print(slice_id, _id_, image_path, record["images"])
                                continue
                            elif len(image_path) ==0 or len(image_path) > 1:
                                print('full error')
                                print(slice_id, _id_, image_path, record["images"])
                                continue

                            annotations[_id_][slice_id].append({
                                'x': x, 'y':y, 'width':width, 'height': height, 'category': label, 'image_path': image_path[0]
                            })

                            n_annotations += 1
                        except KeyError as ke:
                            errors[error_ind] = {
                                "id" : _id_,
                                "annotation": bbox
                            }
                            error_ind += 1

with open('errors.json', 'w') as efp:
    json.dump(errors, efp, indent=4, sort_keys=True)

with open('annotations.json', 'w') as afp:
    json.dump(annotations, afp, indent=4, sort_keys=True)