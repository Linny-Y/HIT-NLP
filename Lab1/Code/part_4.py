from part_2 import *

import time

DIC_FILE = '../io_files/dic.txt'
BETTER_FMM_FILE = '../io_files/better_seg_FMM.txt'
TEST_FILE = '../io_files/test.txt'
"""
    3.4 基于机械匹配的分词系统的速度优化
    输入文件：199801_sent.txt(1998 年 1 月《人民日报》语料，未分词)
    输出：TimeCost.txt(分词所用时间)
"""
MAX_LEN = 0  # 最大词长

class Node:
    def __init__(self, is_word=False, char='', init_list_size=4096):
        self.char = char
        self.is_word = is_word
        self.child_list = [None] * init_list_size
        self.position = 0

    def insert_word(self, word):
        """
            添加字符串 word
        """
        for i,char in enumerate(word):
            exist, p = self.get_child_by_char(char)
            if not exist:
                child = Node() # 不存在 新建节点
                child.char = char
                child.position = p
                self.child_list[p] = child
            if i == len(word) - 1: # 最后一个字符
                self.child_list[p].is_word = True
            else:
                self = self.child_list[p]  # 不为最后一个字符 把当前节点更新为父节点
                continue
    
    def search_word(self, word):
        """
            查找字符串 word
            字符串中当前字符不存在 则返回前面存在的长度; i==0时不存在 返回1
            字符串中没有字符不存在 遍历结束 返回该字符串长度
        """
        length = len(word)
        for i,char in enumerate(word):
            exist, p = self.get_child_by_char(char)
            if not exist:
                if i == 0:
                    return 1
                return i
            self = self.child_list[p]
        return length
            


    def get_child_by_char(self, char):
        """
            在该节点子节点中查找字符 char 对应位置
        """
        p = self.hash_of_ord_char(char)
        while True:
            if self.child_list[p] is None:  # 该位为空 返回 False 空位下标
                return False, p
            # 该位不为空 判断是否为该字符
            if self.child_list[p].char == char:  # 是该字符 返回 True 该位下标
                return True, p
            
            else:
                p = (p + 1) % len(self.child_list) # 不是该字符 更新位置


    def hash_of_ord_char(self, char):
        """
            返回哈希值
        """
        return ord(char) % len(self.child_list)

def get_dict_tree(dic_path = DIC_FILE):
    global MAX_LEN
    root = Node()
    with open(dic_path, 'r') as dic_file:
        lines = dic_file.readlines()
        for line in lines:
            line = line.strip()
            MAX_LEN = len(line) if len(line) > MAX_LEN else MAX_LEN
            root.insert_word(line)
            # print(line)
    return root

def better_FMM(root, test_path = TEST_FILE, better_fmm_path = BETTER_FMM_FILE):
    '''
        优化后正向最大匹配分词
        input: test.txt(测试集)
        output: better_seg_FMM.txt(FMM模型分词)
    '''
    sum = 0
    with open(test_path, 'r') as test_file:
        lines = test_file.readlines()
        all = len(''.join(lines).replace(" ","").replace("\n",""))
    with open(better_fmm_path, 'w') as fmm_file:
        for line in lines:
            line = line.strip() # 去除结尾换行符
            # print(line[0:len(line)-10])
            seg_list = [] # 分割后字段
            while len(line) > 0:
                tryword = line[0:MAX_LEN if len(line) > MAX_LEN else len(line)] # 取最大词长的字符串
                # print(MAX_LEN)
                # print(line)
                # print(tryword)
                if tryword[0].isascii():
                    length = 1
                else:
                    length = root.search_word(tryword) # 获取存在的字符串词长 不存在时为 1
                tryword = tryword[ :length]

                seg_list.append(tryword)
                if not tryword.isascii() or (length == 1 and not line[1].isascii()):  # 当前位或下一位不在ASCII码中 进行分割
                    seg_list.append('/ ')  # 用 '/' 和 ' ' 进行分隔
                line = line[length: ]
                sum += len(tryword)
                print('better_FMM'  +str(sum) + '/' + str(all))
            fmm_file.write(''.join(seg_list) + '\n')  # 写入换行符
        print('FMM cut over!')


if __name__ == '__main__':
    root = get_dict_tree()
    start_time_better_FMM = time.time()
    better_FMM(root)
    end_time_better_FMM = time.time()
    cost_time_better_FMM = end_time_better_FMM - start_time_better_FMM
    print(cost_time_better_FMM)
