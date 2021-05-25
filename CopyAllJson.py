import glob
import os
import shutil

current_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(current_dir, 'input')
output_dir = os.path.join(current_dir, 'raw_json')

def copy(src, dest):
    for file_path in glob.glob(os.path.join(src, '**', '*.json'), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)
    
###############################################
copy(input_dir, output_dir)


