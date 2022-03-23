# Copyright 2019. All Rights Reserved.
#
# Prepared by: Aishwarya Malgonde
# Date & Time: 5th March 2019 | 12:17:00
# ==============================================================================

r"""Test Train Split.
This executable is used to split train and test datasets. 
Example usage:
    python test_train_split.py \
        --datadir='data/all/' \
        --split=0.1 \
        --output='data/' \
        --image_ext='jpeg'
"""

import argparse
import os
from random import shuffle
import pandas as pd
from math import floor
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--datadir', help='Path to the all input data', type=str)
parser.add_argument('--split', help='Split value - Test %', type=float, default=0.1)
parser.add_argument('--output', help='Path to output train & test data', type=str)
parser.add_argument('--image_ext', help='jpeg or jpg or png', type=str, default='jpeg')
FLAGS = parser.parse_args()

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Creating directory -', directory)
    else:
        print('Directory exists -', directory)

def get_file_list_from_dir(datadir):
    all_files = os.listdir(os.path.abspath(datadir))
    data_files = list(filter(lambda file: file.endswith('.'+FLAGS.image_ext), all_files))
    shuffled_files = randomize_files(data_files)
    all_cervix_images = pd.DataFrame({'imagepath': shuffled_files})
    all_cervix_images['filename'] = all_cervix_images.apply(lambda row: row.imagepath.split(".")[0], axis=1)
    return all_cervix_images

def randomize_files(file_list):
    shuffle(file_list)
    return  file_list

def get_training_and_testing_sets(file_list, split):
    split_index = floor(file_list.shape[0] * split)
    testing = file_list[:split_index]
    training = file_list[split_index:]
    training = training.reset_index(drop=True)
    return training, testing

def copy_data(name, datadir, out, kosong):
    try:
        # Moving images
        rd_path = os.path.join(datadir, name+'.'+FLAGS.image_ext)
        wr_path = os.path.join(out, name+'.'+FLAGS.image_ext)
        shutil.copy(rd_path, wr_path)
        if kosong:
            try:
                # Moving xmls
                rd_path = os.path.join(datadir, name+'.xml')
                wr_path = os.path.join(out, name+'.xml')
                shutil.copy(rd_path, wr_path)
            except:
                print('Could not find {}'.format(name+'.xml'))
    except:
        print('Could not find {}'.format(name+'.'+FLAGS.image_ext))

def write_data(training, testing, datadir, output, kosong):
    
    # Train Data
    print ('Writing -', training.shape[0], '- Train data images at -', output)
    for name in training['filename']:
        copy_data(name, datadir, output + '/train', kosong)

    # Test Data
    print ('Writing -', testing.shape[0], '- Test data images at -', output)
    for name in testing['filename']:
        copy_data(name, datadir, output + '/test', kosong)

def main():
    check_dir(FLAGS.output + '/train')
    check_dir(FLAGS.output + '/test')
    file_list_sampel = get_file_list_from_dir(FLAGS.datadir + '/sampel')
    file_list_kosong = get_file_list_from_dir(FLAGS.datadir + '/kosong')
    print('Read -', file_list_sampel.shape[0], '- files from the directory -', FLAGS.datadir + '/sampel')
    print('Read -', file_list_kosong.shape[0], '- files from the directory -', FLAGS.datadir + '/kosong')
    training_sampel, testing_sampel = get_training_and_testing_sets(file_list_sampel, FLAGS.split)
    training_kosong, testing_kosong = get_training_and_testing_sets(file_list_kosong, FLAGS.split)
    write_data(training_sampel, testing_sampel, FLAGS.datadir + '/sampel', FLAGS.output, True)
    write_data(training_kosong, testing_kosong, FLAGS.datadir + '/kosong', FLAGS.output, False)

if __name__ == '__main__':
    main()