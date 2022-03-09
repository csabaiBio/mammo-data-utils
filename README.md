# DICOM conversion

For some reason some DICOMs are encoded with some propietary format...

First need to encode these:

```bash
find . -name '*.dcm'  | xargs -n1 -P8 -I{} bash -c 'f={}; gdcmconv --raw -F $f ${f/.dcm/_raw.dcm}'
```

After converting to `normal` DICOMs we can finally decode to PNG:

```bash
find . -name '*_raw.dcm'  | xargs -n1 -P8 -I{} bash -c 'f={}; dcmj2pnm $f | convert - ${f/_raw.dcm/.png}'
```

Finally we have a lot of PNGs decoded from the dicom files. :)

### Steps

1. Run `process_data_dir.py`
2. Run `process_annotations.py`
3. Run `create_coco.py`
4. Run `visualize.py` # to visualize
