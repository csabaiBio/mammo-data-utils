from pathlib import Path
from os.path import join as opj
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='/tank/qbeer/mammo_annotations_v3', type=str)
    parser.add_argument('--output_json', default='data.json', type=str)

    args = parser.parse_args()
    
    base = Path(args.base_dir)

    data = {}

    for path in base.iterdir():
        if path.is_file() and path.suffix == '.json':
            try:
                _id_ = path.stem
                data[_id_] = {}
                data[_id_]['annotations'] = str(path)
                data[_id_]['images'] = []
                for image_path in Path(opj(base, _id_)).iterdir():
                    if image_path.is_file() and image_path.suffix == '.dcm' and not image_path.stem.endswith('raw'):
                        data[_id_]['images'].append(str(image_path))
            except Exception as e:
                print(e)
                continue

    with open(args.output_json, 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    exit(main())