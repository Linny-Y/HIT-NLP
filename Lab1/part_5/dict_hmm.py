#-*- coding:utf-8 -*-
import sys
import pickle
import math

from utils import *

B_TOKEN = 'B'
M_TOKEN = 'M'
E_TOKEN = 'E'
S_TOKEN = 'S'

class Dict_hmm:
    def __init__(self, SEG_POS_path, DICT_path, epsilon=sys.float_info.epsilon):
        self.SEG_POS_path = SEG_POS_path
        self.DICT_path = DICT_path
        self.epsilon = epsilon
        self.state_lst = [B_TOKEN, M_TOKEN, E_TOKEN, S_TOKEN]
        self.start_p = {}
        self.trans_p = {}
        self.emit_p = {}
        for state in self.state_lst:
            self.start_p[state] = self.epsilon
            self.trans_p[state] = {s:self.epsilon for s in self.state_lst}
            self.emit_p[state] = {}

    def _label(self, word):
        out = []
        if len(word) == 1:
            out = [S_TOKEN]
        else:
            out += [B_TOKEN] + [M_TOKEN] * (len(word) - 2) + [E_TOKEN]
        return out

    def get_dict(self):
        with open(self.SEG_POS_path, 'r') as f:
            lines = [l.strip().split() for l in f.readlines()]
        
        line_nb, char_p = 0, {}
        for line in lines:
            if not line: continue
            char_lst, state_lst = [], []
            line_nb += 1
            for word in line:
                if ('/m' in word and word.isascii()) or len(word) == 0: continue
                true_word = word[1 if word[0] == '[' else 0 : word.index('/')]
                state_lst.extend(self._label(true_word))
                char_lst.extend(true_word)
            
            assert len(state_lst) == len(char_lst)
            for index, state in enumerate(state_lst):
                char_p[char_lst[index]] = char_p.get(char_lst[index], 0) + 1
                if index == 0:
                    self.start_p[state] += 1
                else:
                    self.trans_p[state_lst[index - 1]][state] += 1
                self.emit_p[state][char_lst[index]] = self.emit_p[state].get(char_lst[index], 0) + 1

        for state in [B_TOKEN, S_TOKEN]:
            self.start_p[state] = math.log(self.start_p[state] / line_nb)

        for pre_state in self.state_lst:
            total_num = 0
            for state in self.state_lst:
                total_num += self.trans_p[pre_state][state] if self.trans_p[pre_state][state] else 0
            for state in self.state_lst:
                self.trans_p[pre_state][state] = math.log(self.trans_p[pre_state][state] / total_num) if self.trans_p[pre_state][state] else self.epsilon
        
        for state in self.state_lst:
            for char in self.emit_p[state].keys():
                self.emit_p[state][char] = math.log((self.emit_p[state][char] + self.epsilon) / char_p[char])
        
        self._save_dict()
    
    def _save_dict(self):
        with open(self.DICT_path, 'wb') as f:
            pickle.dump(self.start_p, f)
            pickle.dump(self.trans_p, f)
            pickle.dump(self.emit_p, f)
        
if __name__ == '__main__':
    dict = Dict_hmm(DATA_TRAIN_POS, DICT_HMM)
    dict.get_dict()
    