# -*- coding: utf-8 -*-
import pickle

from utils import *
from evaluation import *
from oov import *

class Bigram:

    def __init__(self, CONTENT_path, DICT_path, DICT_UNI_path, output_path, epsilon=sys.float_info.epsilon):
        self.CONTENT_path = CONTENT_path
        self.DICT_path = DICT_path
        self.DICT_UNI_path = DICT_UNI_path
        self.output_path = output_path
        self.epsilon = math.log(epsilon)
        self.oov = OOV()
        self._read_dict()

    def _read_dict(self):
        with open(self.DICT_path, 'rb') as f:
            self.dict = pickle.load(f)
        with open(self.DICT_UNI_path, 'r', encoding='utf8') as f:
            lines = [l.strip().split() for l in f.readlines()]
        self.word_dict = {l[0]: int(l[1]) for l in lines}
        self.max_len = max([len(w) for w in self.word_dict])

    def _get_DAG(self, token):
        DAG = {}
        for l in range(1, len(token) - 1):
            DAG[l] = [l]
            for r in range(l, min(l + self.max_len, len(token) - 1)):
                if token[l:r + 1] in self.word_dict:
                    DAG[l].append(r)
        DAG[len(token) - 1] = [len(token) - 1]
        DAG[0] = [0]
        return DAG
    
    def _get_segs(self, sequence, route, DAG):
        segs, start = [], 1
        end = max((self.dict.get(sequence[1:y + 1], {}).get(sequence[0], self.epsilon) + route.get(1)[y][0], y) for y in DAG[1])[1]
        while start < len(sequence) - 1:
            segs.append(sequence[start:end + 1])
            temp = start
            start = end + 1
            end = route[temp][end][1]
        return segs

    def _calc_bigram(self, sequence, DAG):
        route = {i:{} for i in range(len(sequence))}
        route[len(sequence) - 1][len(sequence) - 1] = (0., len(sequence))
        for i in range(len(sequence) - 2, -1, -1):
            for x in DAG[i]:
                prob_index = max((self.dict.get(sequence[x + 1:y + 1], {}).get(sequence[i:x + 1], self.epsilon) +
                     route.get(x + 1)[y][0], y) for y in DAG[x + 1])
                route[i][x] = prob_index
        return route

    def bigram(self):
        f_res = open(self.output_path, 'w', encoding='utf8')
        with open(self.CONTENT_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        
        for line in lines:
            if not line: 
                f_res.write('\n')
                continue
            line = '@' + line + '&'

            DAG = self._get_DAG(line)
            route = self._calc_bigram(line, DAG)
            segs = self._get_segs(line, route, DAG)
            segs = post_process(segs)
            segs = self.oov.oov(segs)

            f_res.write('/ '.join(segs) + '/ \n')
        f_res.close()

if __name__ == '__main__':
    bi = Bigram(DATA_TEST_CONTENT, DICT_BIGRAM, DICT_UNIGRAM, BI_SEG)
    bi.bigram()
    print(str(Evaluation(DATA_TEST_POS, BI_SEG)))