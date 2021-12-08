# -*- coding: utf-8 -*-
import pickle
import math
import sys

from utils import *

class Dict_unigram:
    def __init__(self, SEG_POS_path, DICT_path):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.words = {}
        self.max_len = 0

    def get_dict(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
        segs = [l[i] for l in lines for i in range(1, len(l))]
        for seg in segs:
            if ('/m' in seg and seg.isascii()) or len(seg) == 0: continue
            word = seg[1 if seg[0] == '[' else 0 : seg.index('/')]
            if word not in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1
            self.max_len = max(len(word), self.max_len)
        self._save_dict()
    
    def _save_dict(self):
        with open(self.DICT_path, 'w', encoding='utf8') as f:
            for word in self.words:
                f.write('{} {}\n'.format(word, self.words[word]))


class Dict_bigram:
            
    def __init__(self, SEG_POS_path, DICT_path, DICT_UNI_path, epsilon=sys.float_info.epsilon):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.DICT_UNI_path = DICT_UNI_path
        self.bigram_dic = {}
        self.epsilon = math.log(epsilon)
        self._read_dict()

    def _read_dict(self):
        with open(self.DICT_UNI_path, 'r', encoding='utf8') as f:
            lines = [l.strip().split() for l in f.readlines()]
        self.word_num = sum([int(l[1]) for l in lines])

    def _save_dict(self):
        with open(self.DICT_path, 'wb') as f:
            pickle.dump(self.bigram_dic, f)

    def get_dict(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        seg_lists = []
        # 按行提取分词结果
        for line in lines:
            if not line: continue
            seg_list = []
            for word in line[23:].split():
                seg_list.append(word[1 if word[0] == '[' else 0:word.index('/')])
            seg_list.insert(0, '@')  # BOS标识符
            seg_list.append('&')  # EOS标识符
            seg_lists.append(seg_list)

        # 二元文法词典
        self.bigram_dic = {}
        for seg_list in seg_lists:
            for i in range(1, len(seg_list)):
                # 之前没出现，新加入词典中
                if seg_list[i] not in self.bigram_dic:
                    self.bigram_dic[seg_list[i]] = {}
                    self.bigram_dic[seg_list[i]][seg_list[i - 1]] = 1
                else:
                    self.bigram_dic[seg_list[i]][seg_list[i - 1]] = self.bigram_dic[seg_list[i]].get(
                        seg_list[i - 1], 0) + 1

        # 计算概率，取对数
        for post_word in self.bigram_dic.keys():
            sigma = 1e-7
            total_cnt = 0
            for pre_word in self.bigram_dic.get(post_word):
                total_cnt += self.bigram_dic[post_word].get(pre_word)
            for pre_word in self.bigram_dic.get(post_word):
                self.bigram_dic[post_word][pre_word] = math.log(
                    (self.bigram_dic[post_word].get(pre_word) + sigma) / (total_cnt + sigma * self.word_num))
                cur_frec = math.log(sigma / (total_cnt + self.word_num))
                if cur_frec < self.epsilon:
                    self.epsilon = cur_frec
        
        self._save_dict()


if __name__ == '__main__':
    # dict = Dict_unigram(DATA_TRAIN_POS, DICT_UNIGRAM)
    # dict.get_dict()
    dict = Dict_bigram(DATA_TRAIN_POS, DICT_BIGRAM, DICT_UNIGRAM)
    dict.get_dict()
