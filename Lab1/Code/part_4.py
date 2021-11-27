from part_2 import *

import time

DIC_FILE = '../io_files/dic.txt'
BETTER_FMM_FILE = '../io_files/better_seg_FMM.txt'
BETTER_BMM_FILE = '../io_files/better_seg_BMM.txt'
TEST_FILE = '../io_files/test.txt'
FMM_FILE_10 = '../io_files/seg_FMM_1_10.txt'
BMM_FILE_10 = '../io_files/seg_BMM_1_10.txt'

FMM_FILE = '../io_files/seg_FMM.txt'
BMM_FILE = '../io_files/seg_BMM.txt'
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
            字符串中当前字符不存在 则返回前面存在的长度; 
            字符串中没有字符不存在 遍历结束 返回该字符串长度
        """
        length = len(word)
        res = 0
        for i,char in enumerate(word):
            exist, p = self.get_child_by_char(char)
            if self.is_word:
                res = i
            if not exist:
                # if i == 0:  # i==0时不存在 返回1
                #     return 1
                return res
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

def get_dict_tree_FMM(dic_path = DIC_FILE):
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

def get_dict_tree_BMM(dic_path = DIC_FILE):
    global MAX_LEN
    root = Node()
    with open(dic_path, 'r') as dic_file:
        lines = dic_file.readlines()
        for line in lines:
            line = line.strip()[::-1] # 将词典反向
            MAX_LEN = len(line) if len(line) > MAX_LEN else MAX_LEN
            root.insert_word(line)
            
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
                    length = root.search_word(tryword) # 获取存在的字符串词长 不存在时为 0
                    if length == 0:
                        length = 1
                tryword = tryword[ :length]

                seg_list.append(tryword)
                if not tryword.isascii() or (length == 1 and not line[1].isascii()):  # 当前位或下一位不在ASCII码中 进行分割
                    seg_list.append('/ ')  # 用 '/' 和 ' ' 进行分隔
                line = line[length: ]
                sum += len(tryword)
                # print('better_FMM '  +str(sum) + '/' + str(all))
            fmm_file.write(''.join(seg_list) + '\n')  # 写入换行符
        print('better FMM cut over!')

def better_BMM(root, test_path = TEST_FILE, better_bmm_path = BETTER_BMM_FILE):
    '''
        优化后反向最大匹配分词
        input: test.txt(测试集)
        output: better_seg_BMM.txt(BMM模型分词)
    '''
    sum = 0
    with open(test_path, 'r') as test_file:
        lines = test_file.readlines()
        all = len(''.join(lines).replace(" ","").replace("\n",""))
    with open(better_bmm_path, 'w') as bmm_file:
        for line in lines:
            line = line.strip()[::-1] # 句子反向
            seg_list = [] # 分割后字段
            if line != '':
                seg_list.append(' /')
            while len(line) > 0:
                tryword = line[0:MAX_LEN if len(line) > MAX_LEN else len(line)] # 取最大词长的字符串
                if tryword[0].isascii():
                    length = 1
                else:
                    length = root.search_word(tryword) # 获取存在的字符串词长 不存在时为 0
                    if length == 0:
                        length = 1
                tryword = tryword[ :length]

                seg_list.append(tryword)
                if not tryword.isascii()  or ((not len(line) == 1) and length == 1 and (not line[1].isascii())):
                    seg_list.append(' /')  # 用 '/' 和 ' ' 进行分隔
                line = line[length: ]
                sum += len(tryword)
                # print('better_BMM '  +str(sum) + '/' + str(all))
            bmm_file.write(''.join(seg_list)[::-1] + '\n')  # 写入换行符
        print('better BMM cut over!')

def all():
    # part_2 全文分割
    root = get_dict_tree_FMM()
    better_FMM(root,test_path='../io_files/199801_sent.txt',better_fmm_path=FMM_FILE) 
    
    rootp = get_dict_tree_BMM()
    better_BMM(rootp,test_path='../io_files/199801_sent.txt',better_bmm_path=BMM_FILE) 

def timer():
    ### 优化前
    get_dict('../io_files/dic.txt')

    start_time_FMM = time.time()
    FMM(fmm_path = FMM_FILE_10)
    end_time_FMM = time.time()
    cost_time_FMM = end_time_FMM - start_time_FMM

    start_time_BMM = time.time()
    BMM(bmm_path = BMM_FILE_10)
    end_time_BMM = time.time()
    cost_time_BMM = end_time_BMM - start_time_BMM

    ### 优化后
    root = get_dict_tree_FMM()
    start_time_better_FMM = time.time()
    better_FMM(root)
    end_time_better_FMM = time.time()
    cost_time_better_FMM = end_time_better_FMM - start_time_better_FMM
    # print(cost_time_better_FMM)

    root = get_dict_tree_BMM()
    start_time_better_BMM = time.time()
    better_BMM(root)
    end_time_better_BMM = time.time()
    cost_time_better_BMM = end_time_better_BMM - start_time_better_BMM
    # print(cost_time_better_BMM)

    with open('../io_files/TimeCost.txt', 'w') as time_cost:
        time_cost.write("优化前\n")
        time_cost.write('FMM时间花销为：' + str(cost_time_FMM) + 's\n')
        time_cost.write('BMM时间花销为：' + str(cost_time_BMM) + 's\n\n')
        time_cost.write("优化后\n")
        time_cost.write("FMM时间花销为：" + str(cost_time_better_FMM) + 's\n')
        time_cost.write("FMM优化比例为：" + str((1-cost_time_better_FMM/cost_time_FMM)*100) + "%\n")
        time_cost.write("BMM时间花销为：" + str(cost_time_better_BMM) + 's\n')
        time_cost.write("BMM优化比例为：" + str((1-cost_time_better_BMM/cost_time_BMM)*100) + "%\n")
    print('Finish')



if __name__ == '__main__':
    # part_2
    all()
    # part_4
    timer()
    

    
    
