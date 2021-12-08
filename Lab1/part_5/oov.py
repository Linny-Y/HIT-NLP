from hmm import *

class OOV:
    def __init__(self):
        self.hmm = HMM(None, DICT_HMM)
        self.OOV_name = OOV_name()

    def _oov(self, to_seg_word):
        single_nums = 0
        for w in to_seg_word:
            if self.hmm.emit_p['S'].get(w, 0) < -3.5:
                single_nums += 1
        if single_nums >= 2:
            return self.hmm.process_word(to_seg_word)
        else:
            return [x for x in to_seg_word]

    def _process(self, to_seg_word):
        oov_segs = self.OOV_name.oov_name(self.hmm.process_word(to_seg_word))
        if len(oov_segs) == len(to_seg_word):
            oov_segs = self._oov(to_seg_word)
        return oov_segs

    def oov(self, segs):
        to_seg_word, result_segs = '', []
        for seg in segs:
            if len(seg) == 1:
                to_seg_word += seg
            else:
                if len(to_seg_word) >= 3:
                    result_segs.extend(self._process(to_seg_word))
                else:
                    result_segs.extend(to_seg_word)
                result_segs.append(seg)
                to_seg_word = ''
        if len(to_seg_word):
            result_segs.extend(self._process(to_seg_word))
        return result_segs

class OOV_name:
    def __init__(self, NAME_FIRST_path=NAME_FIRST, NAME_LAST_path=NAME_LAST):
        self.NAME_FIRST_path = NAME_FIRST_path
        self.NAME_LAST_path = NAME_LAST_path
        self.hmm = HMM(None, DICT_HMM)
        self._load_dict()
        
    def _load_dict(self):
        def __load_dict(dict_path):
            with open(dict_path, 'r', encoding='utf8') as f:
                lines = [l.strip() for l in f.readlines()]
            dict_name = {}
            for l in lines:
                word, p = l.split()
                dict_name[word] = int(p)
            return dict_name
        self.first_name = __load_dict(self.NAME_FIRST_path)
        self.last_name = __load_dict(self.NAME_LAST_path)

    def oov_name(self, segs):
        result_segs = []
        for i, seg in enumerate(segs):
            if len(seg) == 1:
                result_segs.append(seg)
            else:
                score = 0
                for w in seg:
                    if w in self.last_name and self.last_name.get(w, 0) > 500: score += 3
                    else: score += 1
                if i > 0 and segs[i - 1] in self.first_name and self.first_name.get(segs[i - 1], 0) > 100:
                    score += 3
                if score * len(seg) >= 14:
                    result_segs.append(seg)
                else:
                    for w in seg:
                        result_segs.append(w)
        return result_segs