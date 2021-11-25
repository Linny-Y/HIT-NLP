Dic_File = '../io_files/dic.txt'
Train_File = '../io_files/train.txt'
Std_File = '../io_files/std.txt'
Test_File = '../io_files/test.txt'
K = 10 # 将标准分词文件的9/10作为训练集

'''
    3.1 词典的构建
    输入文件：199801_seg&pos.txt（1998 年 1 月《人民日报》的分词语料库） 、199801_sent.txt（1998 年 1 月《人民日报》语料，未分词）
    输出：dic.txt（自己形成的分词词典)、train.txt（训练集）、std.txt（标准答案）、test.txt（测试集）
'''


def gene_dic(train_path =Train_File, dic_path = Dic_File):
    '''
        生成分词词典
        input: train.txt(训练集)
        output: dic.txt(分词词典)
    '''
    word_set = set()  # 词列表, 有序且不重复
    max_len = 0   # 最大词长
    with open(train_path, 'r') as train_file:  # 读取训练文本
        lines = train_file.readlines()
    with open(dic_path, 'w') as dic_file:  
        for line in lines:
            for word in line.split():
                if '/m' in word:  # 除去量词
                    continue
                word = word[1 if word[0] == '[' else 0 : word.index('/')]    #去除 '[' 符号, 取 '/'前的词
                if (len(word) > max_len): # 更新最大词长
                    max_len = len(word)
                word_set.add(word)  # 加入词典
        word_list = list(word_set)
        word_list.sort()  # 排序
        dic_file.write('\n'.join(word_list))  # 用 '\n' 连接成新字符串
    return word_list, max_len


def gene_train_std(seg_path ='../io_files/199801_seg&pos.txt', train_path = Train_File, std_path = Std_File, k = K):
    '''
        按9:1生成训练集和测试集
        input: 199801_seg&pos.txt(分词语料库)
        output: train.txt(训练集), std.txt(标准答案), test.txt(测试集)
    '''
    with open(seg_path, 'r') as seg_file:
        seg_lines = seg_file.readlines()
    std_lines = [] # 标准分词答案
    with open(train_path, 'w') as train_file:
        for i, line in enumerate(seg_lines):
            if i % k != 0:
                train_file.write(line) # 模 k 不为 0 的行数加入训练集
            else:
                std_lines.append(line) # 模 k 为 0 的行数加入标准答案
    with open(std_path, 'w') as std_file:
        std_file.write(''.join(std_lines)) # 写入标准分词答案
    gene_test() # 生成测试集


def gene_test(sent_path = '../io_files/199801_sent.txt', test_path = Test_File, k = K):
    '''
        生成测试集
        input: 199801_sent.txt(未分词语料)
        output: test.txt(测试集)
    '''
    with open(sent_path, 'r') as sent_file:
        sent_lines = sent_file.readlines()
    with open(test_path, 'w') as test_file:
        for i, line in enumerate(sent_lines):
            if i % k == 0:  
                test_file.write(line)  # 模 k 为 0 的行数加入测试集

if __name__ == '__main__':
    gene_train_std()
    gene_dic()