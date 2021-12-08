#-*- coding:utf-8 -*-
import sys
import pickle
import re
import math

from utils import *
from evaluation import *

B_TOKEN = 'B'
M_TOKEN = 'M'
E_TOKEN = 'E'
S_TOKEN = 'S'

PRE_TOKEN = {B_TOKEN:[E_TOKEN, S_TOKEN], M_TOKEN:[S_TOKEN, M_TOKEN], E_TOKEN:[M_TOKEN, B_TOKEN], S_TOKEN:[S_TOKEN, E_TOKEN]}

class HMM:
    def __init__(self, CONTENT_path, DICT_path, flags=r'[，。；！？《》【】：“”]', epsilon=sys.float_info.epsilon):
        self.CONTENT_path = CONTENT_path
        self.DICT_path = DICT_path
        self.epsilon = math.log(epsilon)
        self.state_lst = [B_TOKEN, M_TOKEN, E_TOKEN, S_TOKEN]
        self.flags = flags
        self.state_epsilon = {}
        self._load_dict()
    
    def _load_dict(self):
        with open(self.DICT_path, 'rb') as f:
            self.start_p = pickle.load(f)
            self.trans_p = pickle.load(f)
            self.emit_p = pickle.load(f)

    def _viterbi(self, sentence):
        trans = [{}]
        path = {}
        for state in self.state_lst:
            trans[0][state] = self.start_p[state] + self.emit_p[state].get(sentence[0], self.epsilon)
            path[state] = [state]

        for index in range(1, len(sentence)):
            word, new_path = sentence[index], {}
            trans.append({})

            for cur_state in self.state_lst:
                emitp = self.emit_p[cur_state].get(word, self.epsilon)
                (prob, pre_state) = max([(trans[index - 1][pre_state] + self.trans_p[pre_state].get(cur_state, self.epsilon) + emitp, pre_state) for pre_state in PRE_TOKEN[cur_state]])
                trans[index][cur_state] = prob
                new_path[cur_state] = path[pre_state] + [cur_state]
            path = new_path

        (prob, state) = max([(trans[len(sentence) - 1][state], state) for state in (E_TOKEN, S_TOKEN)])
        return prob, path[state]
    
    def _restore(self, token_list, word):
        begin, end = 0, 0
        segs = []
        for i in range(len(word)):
            token = token_list[i]
            if token == B_TOKEN:
                begin = i
            elif token == E_TOKEN:
                segs.append(word[begin: i + 1])
                end = i + 1
            elif token == S_TOKEN:
                segs.append(word[i])
                end = i + 1
        if end < len(word):
            segs.append(word[end:])
        return segs

    def process_word(self, word):
        _, token_list = self._viterbi(word)
        segs = self._restore(token_list, word)
        # print(word, '->', segs)
        # time.sleep(0.1)
        return segs

    def hmm(self):
        f_res = open(HMM_SEG, 'w', encoding='utf8')
        with open(self.CONTENT_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        for line in lines:
            now_line, last_pos = [], 0
            for i in re.finditer(self.flags, line):
                now_line.append((line[last_pos: i.start()], i.group()))
                last_pos = i.start() + 1
            now_line.append((line[last_pos:], ''))
            for sequence in now_line:
                word, flag = sequence
                if len(word) == 0: 
                    if flag != '': f_res.write(flag + '/ ')
                    continue
                segs = self.process_word(word)
                segs = post_process(segs)
                f_res.write('/ '.join(segs) + '/ ')
                if flag != '': f_res.write(flag + '/ ')
            f_res.write('\n')
        f_res.close()

if __name__ == '__main__':
    dict = HMM(DATA_TEST_CONTENT, DICT_HMM)
    dict.hmm()
    print("acc={}".format(str(Evaluation(DATA_TEST_POS, HMM_SEG))))
    