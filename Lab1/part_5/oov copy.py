from hmm import *

class OOV:
    def __init__(self, WORDDICT_path):
        self.WORDDICT_path = WORDDICT_path
        self.words = set()
        self.hmm = HMM(None, DICT_HMM)
        self._load_dict()

    def _load_dict(self):
        with open(self.WORDDICT_path, 'r', encoding='utf-8') as f:
            for token in f.readlines():
                self.words.add(token.strip())

    def oov(self, segs):
        to_seg_word, result_segs = '', []
        for i in range(len(segs)):
            if len(segs[i]) == 1:
                if segs[i] in self.words:
                    if to_seg_word:
                        result_segs.extend(self.hmm.process_word(to_seg_word))
                        to_seg_word = ''
                    result_segs.append(segs[i])
                else:
                    to_seg_word += segs[i]
                    if i + 1 == len(segs):
                        result_segs.extend(self.hmm.process_word(to_seg_word))
            else:
                if to_seg_word:
                    result_segs.extend(self.hmm.process_word(to_seg_word))
                    to_seg_word = ''
                result_segs.append(segs[i])
        return result_segs