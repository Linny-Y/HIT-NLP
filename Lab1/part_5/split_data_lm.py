# -*- coding: utf-8 -*-
import random
import numpy as np

from utils import *

def split_data_lm(seed=2021):
    random.seed(seed)
    with open(DATA1_SEG_POS, 'r') as f:
        lines_pos1 = np.array([l.strip() for l in f.readlines()])
    with open(DATA2_SEG_POS, 'r') as f:
        lines_pos2 = np.array([l.strip() for l in f.readlines()])
    with open(DATA1_CONTENT, 'r') as f:
        lines_content = np.array([l.strip() for l in f.readlines()])
    
    assert len(lines_content) == len(lines_pos1)
    new_index = list(range(len(lines_pos1)))
    random.shuffle(new_index)
    lines_pos1 = lines_pos1[new_index]
    lines_content = lines_content[new_index]
    trian_size = len(lines_content) // 5 * 4
    TRAIN_POS, TEST_POS = lines_pos1[:trian_size], lines_pos1[trian_size:]
    _, TEST_CONTENT = lines_content[:trian_size], lines_content[trian_size:]
    
    with open(DATA_TRAIN_POS, 'w') as f:
        for l in TRAIN_POS:
            f.write(l + '\n')
        for l in lines_pos2:
            f.write(l + '\n')
    with open(DATA_TEST_POS, 'w') as f:
        for l in TEST_POS:
            f.write(l + '\n')
    with open(DATA_TEST_CONTENT, 'w') as f:
        for l in TEST_CONTENT:
            f.write(l + '\n')

if __name__ == '__main__':
    split_data_lm()