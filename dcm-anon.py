#!/usr/bin/env python

import argparse
import pydicom
import os
import pathlib
import hashlib
import re

hash_list = [
  (0x0008,0x0080),
  (0x0008,0x0081),
  (0x0008,0x1030),
  (0x0008,0x1070),
  (0x0010,0x0010),
  (0x0010,0x0020),
  (0x0032,0x1060),
  (0x0040,0x0254)
]

date_overwrite_list = [
  (0x0010,0x0030),
  (0x0008,0x0012),
  (0x0008,0x0020),
  (0x0008,0x0021),
  (0x0008,0x0022),
  (0x0008,0x0023),
  (0x0040,0x0244)
]

date_sub_list = [
  (0x0008,0x0018),
  (0x0029,0x1009),
  (0x0029,0x1019),
  (0x0040,0x0253),
  (0x0020,0x000e),
  (0x0020,0x0052)
]

def dcm_anon(dcm_file):
    dcm = pydicom.dcmread(dcm_file)
    for tag in hash_list:
        dcm[tag].value = hashlib.md5(dcm[tag].value.encode('utf-8')).hexdigest()
    date_to_replace = dcm[(0x0008,0x0012)].value
    date_to_replace_with = '19991231'
    for tag in date_overwrite_list:
        dcm[tag].value = '19991231'
    for tag in date_sub_list:
        dcm[tag].value = re.sub(date_to_replace, date_to_replace_with, dcm[tag].value)
    # Recurse through subitems in (0x0008,0x1140) and replace datestring
    for el in dcm[(0x0008,0x1140)].value:
        el[(0x0008,0x1155)].value = re.sub(date_to_replace, date_to_replace_with, dcm[tag].value)
    suggested_out_file = re.sub(date_to_replace, date_to_replace_with, os.path.basename(dcm_file))
    
    # Also change tag (0x0002, 0x0003) which pydicom segragates into the 'file_meta' sturcture
    dcm.file_meta[(0x0002, 0x0003)].value = re.sub(date_to_replace, date_to_replace_with, dcm.file_meta[(0x0002, 0x0003)].value)
    return dcm, suggested_out_file

parser = argparse.ArgumentParser(description='Parse command line options')
parser.add_argument('input_directory')
parser.add_argument('output_directory')
args = parser.parse_args()

filelist = [f for f in os.listdir(args.input_directory) if os.path.isfile(os.path.join(args.input_directory, f))]

out_path = pathlib.Path(args.output_directory)
out_path.mkdir(parents=True, exist_ok=True)

for f in filelist:
    dcm, suggested_out_file = dcm_anon(os.path.join(args.input_directory,f))
    dcm.save_as(os.path.join(args.output_directory,suggested_out_file))
