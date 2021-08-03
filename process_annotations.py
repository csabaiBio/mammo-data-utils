import json
from pprint import pprint

with open('data.json', 'r') as fp:
    data = json.load(fp)

annotations = {}

for _id_, record in data.items():
    annotations[_id_] = {}
    with open(record['annotations'], 'r') as fp:
        records = json.load(fp)
    from pprint import pprint
    if records is not None:
        ann = records.get('drawings', {})
        for rect in ann.get('children', []):
            if rect['attrs'].get('id') is None:
                continue
            slice_id = int(rect['attrs']['id'].replace('slice-', '').split('_')[0])
            annotations[_id_][slice_id] =  []

error_ind = 0
n_annotations = 0

errors = {}

for _id_, record in data.items():
    with open(record['annotations'], 'r') as fp:
        records = json.load(fp)
    from pprint import pprint
    if records is not None:
        ann = records.get('drawings', {})
        for rect in ann.get('children', []):
            if rect['attrs'].get('id') is None:
                continue
            slice_id = int(rect['attrs']['id'].replace('slice-', '').split('_')[0])
            for bbox in rect.get('children', []):
                for bbox in bbox.get('children', []):
                    if bbox['className'] == 'Rect':
                        try:
                            x = bbox['attrs']['x']
                            y = bbox['attrs']['y']
                            width = bbox['attrs']['width']
                            height = bbox['attrs']['height']

                            label = bbox['attrs']['category']

                            annotations[_id_][slice_id].append({
                                'x': x, 'y':y, 'width':width, 'height': height, 'category': label
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

print(n_annotations)
print(error_ind)