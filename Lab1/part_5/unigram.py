# coding:utf-8
import re
import math
from oov import *

from utils import *
from evaluation import *

class Unigram:
    def __init__(self, CONTENT_path, DICT_path, output_path, flags=r'[，。；！？《》【】：“”]', gamma=0.2):
        self.CONTENT_path = CONTENT_path
        self.DICT_path = DICT_path
        self.output_path = output_path
        self.flags = flags
        self.gamma = gamma
        self.oov = OOV()
        self._read_dict()
    
    def _read_dict(self):
        with open(self.DICT_path, 'r', encoding='utf8') as f:
            lines = [l.strip().split() for l in f.readlines()]
        self.dict = {l[0]: int(l[1]) for l in lines}
        self.max_len = max([len(w) for w in self.dict])
        self.dict_total = len(self.dict)
    
    def _get_DAG(self, word):
        DAG = {}
        for r in range(len(word)):
            DAG[r] = [r]
            for l in range(max(r - self.max_len, 0), r):
                if word[l:r + 1] in self.dict:
                    DAG[r].append(l)
        return DAG
    
    def Unigram(self):
        f_res = open(self.output_path, 'w', encoding='utf8')
        with open(self.CONTENT_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        for line in lines:
            if not line: 
                f_res.write('\n')
                continue
            f_res.write(line[:19] + '/ ')
            line = line[19:]
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
                DAG = self._get_DAG(word)
                route = self._calc_unigram(word, DAG)
                segs = self._get_segs(word, route)
                segs = self.oov.oov(segs)
                segs = post_process(segs)
                f_res.write('/ '.join(segs) + '/ ')
                if flag != '': f_res.write(flag + '/ ')
            f_res.write('\n')
        f_res.close()
    
    def _get_prob(self, word):
        # return math.log(1 if word not in self.dict else self.dict[word]) - self.log_total
        pr = 0 if word not in self.dict else self.dict[word]
        return math.log(self.gamma * pr / self.dict_total + (1 - self.gamma) / self.dict_total)

    def _calc_unigram(self, sequence, DAG):
        len_seq = len(sequence)
        self.log_total = math.log(self.dict_total)
        route = [(0, 0)] * len_seq
        for i in range(len_seq):
            route[i] = max([(self._get_prob(sequence[x: i + 1]) + route[x - 1][0], x) for x in DAG[i]])
        return route
    
    def _get_segs(self, sequence, route):
        segs = []
        r = len(sequence) - 1
        while r >= 0:
            segs.append(sequence[route[r][1]:r + 1])
            r = route[r][1] - 1
        return segs[::-1]

if __name__ == '__main__':
    def test(gamma):
        uni = Unigram(DATA_TEST_CONTENT, DICT_UNIGRAM, UNI_SEG, flags=r'[，。；！？《》【】：“”]', gamma=gamma)
        uni.Unigram()
        print("gamma={}, acc={}".format(gamma, str(Evaluation(DATA_TEST_POS, UNI_SEG))))
    
    # test(0.9)
    # test(0.8)
    # test(0.7)
    # test(0.6)
    # test(0.5)
    test(0.4)
    # test(0.3)
    # test(0.2)
    # test(0.1)
    # test(0)

    """
        precision: 94.05%, recall: 96.15%, F: 95.09%
    """
