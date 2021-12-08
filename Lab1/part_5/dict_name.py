from utils import *

class Dict_name:
    def __init__(self, NAME_path, NAME_FIRST_path, NAME_LAST_path):
        self.NAME_path = NAME_path
        self.NAME_FIRST_path = NAME_FIRST_path
        self.NAME_LAST_path = NAME_LAST_path
        self.first_name = {}
        self.last_name = {}
    
    def get_dict(self):
        with open(self.NAME_path, 'r', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        for l in lines:
            if len(l) == 3:
                self.first_name[l[0]] = self.first_name.get(l[0], 0) + 1
                self.last_name[l[1]] = self.last_name.get(l[1], 0) + 1
                self.last_name[l[2]] = self.last_name.get(l[2], 0) + 1
            elif len(l) == 4:
                self.first_name[l[:2]] = self.first_name.get(l[:2], 0) + 1
                self.last_name[l[2]] = self.last_name.get(l[2], 0) + 1
                self.last_name[l[3]] = self.last_name.get(l[3], 0) + 1
        self._save_dict()

    def _save_dict(self):
        with open(self.NAME_FIRST_path, 'w', encoding='utf-8') as f:
            for name in self.first_name:
                f.write('{} {}\n'.format(name, self.first_name[name]))
        with open(self.NAME_LAST_path, 'w', encoding='utf-8') as f:
            for name in self.last_name:
                f.write('{} {}\n'.format(name, self.last_name[name]))

if __name__ == '__main__':
    dict = Dict_name(NAME, NAME_FIRST, NAME_LAST)
    dict.get_dict()
