from pathlib import Path
from os.path import join as opj
import json


base = Path('/tank/reg_backup/mammo_raw/mammo_from_server')

data = {}

for path in base.iterdir():
    if path.is_file() and path.suffix == '.json':
        _id_ = path.stem
        data[_id_] = {}
        data[_id_]['annotations'] = str(path)
        data[_id_]['images'] = []
        for image_path in Path(opj(base, _id_)).iterdir():
            if image_path.is_file() and image_path.suffix == '.dcm':
                data[_id_]['images'].append(str(image_path))

with open('data.json', 'w') as fp:
    json.dump(data, fp, indent=4, sort_keys=True)

