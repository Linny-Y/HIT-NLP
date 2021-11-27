
FMM_FILE = '../io_files/seg_FMM.txt'
BMM_FILE = '../io_files/seg_BMM.txt'
STD_FILE = '../io_files/std.txt'
SCORE_FILE = '../io_files/score.txt'

'''
    3.3 正反向最大匹配分词效果分析
    输入文件：std.txt(标准答案)、seg_FMM.txt、seg_BMM.txt
    输出：score.txt(包括准确率(precision)、召回率(recall)，F 值的结果文件)
'''


def score(std_path=STD_FILE, fmm_path=FMM_FILE, bmm_path=BMM_FILE, score_path=SCORE_FILE, k=1):
    '''
        计算评测得分
        input: std.txt(标准分词文件), seg_FMM.txt(FMM模型分词文件), seg_BMM.txt(BMM模型分词文件)
        output: score.txt(评测结果)
    '''
    FMM_correct_words, FMM_std_words, FMM_my_words = count(fmm_path, std_path)
    BMM_correct_words, BMM_std_words, BMM_my_words = count(bmm_path, std_path)
    FMM_precision, FMM_recall, FMM_f_value = calc(FMM_correct_words, FMM_std_words, FMM_my_words, k)
    BMM_precision, BMM_recall, BMM_f_value = calc( BMM_correct_words, BMM_std_words, BMM_my_words, k)
    with open(score_path, 'w') as score_file:
        score_file.write('正向最大匹配效果分析: \n')
        score_file.write('正确分词数: '+str(FMM_correct_words)+'\n')
        score_file.write('标准分词数: '+str(FMM_std_words)+'\n')
        score_file.write('模型分词数: '+str(FMM_my_words)+'\n')
        score_file.write('准确率: '+str(FMM_precision * 100)+' %\n')
        score_file.write('召回率: '+str(FMM_recall * 100)+' %\n')
        score_file.write('F值: '+str(FMM_f_value * 100)+' %\n\n')
        score_file.write('反向最大匹配效果分析: \n')
        score_file.write('正确分词数: '+str(BMM_correct_words)+'\n')
        score_file.write('标准分词数: '+str(BMM_std_words)+'\n')
        score_file.write('模型分词数: '+str(BMM_my_words)+'\n')
        score_file.write('准确率: '+str(BMM_precision * 100)+' %\n')
        score_file.write('召回率: '+str(BMM_recall * 100)+' %\n')
        score_file.write('F值: '+str(BMM_f_value * 100)+' %\n')


def count(file_path, std_path):
    '''
        计算总词数和正确词数
        input: std.txt(标准分词文件), (seg_FMM.txt / seg_BMM.txt)(模型分词文件)
        return: correct_words(正确分词数), std_words(标准分词数), my_words(模型分词数)
    '''
    correct_words = 0
    std_words = 0
    my_words = 0
    with open(std_path, 'r') as std_file:
        with open(file_path, 'r') as seg_file:
            std_line = std_file.readline()  # 读取一行
            seg_line = seg_file.readline()
            while std_line != '' and seg_line != '':
                while std_line == '\n':
                    std_line = std_file.readline()
                while seg_line == '\n':
                    seg_line = seg_file.readline()
                std_index = get_index(std_line)
                seg_index = get_index(seg_line)
                std_words += len(std_index) - 1
                my_words += len(seg_index) - 1
                head = 0
                for i in range(len(std_index)-1):
                    for j in range(head, len(seg_index)-1):
                        if std_index[i] == seg_index[j] and std_index[i + 1] == seg_index[j + 1]:
                            correct_words += 1
                            # print(head)
                            head = j + 1
                            break
                # print(std_index)
                # print(seg_index)
                # print(correct_words)
                # break
                std_line = std_file.readline()
                seg_line = seg_file.readline()
    return correct_words, std_words, my_words


def calc(correct_words, std_words, my_words, k):
    '''
        计算准确率 召回率和f值
        input: correct_words(正确分词数), std_words(标准分词数), my_words(模型分词数)
        return: precision(准确率), recall(召回率), f_value(f值)
    '''
    precision = 0
    recall = 0
    f_value = 0
    precision = correct_words / my_words
    recall = correct_words / std_words
    f_value = (k*k+1)*precision*recall / (k*k*precision + recall)
    # print('{}, {}, {}'.format(precision,recall,f_value))
    return precision, recall, f_value

def get_index(line):
    '''
        获取词对应下标
        input: line(一行待分词字符)
        return: indexes(每个词对应的下标的列表)
    '''
    indexes = []
    index = 0
    indexes.append(index)
    line = line.strip()
    for word in line.split():
        word = word[1 if word[0] == '[' else 0: word.index('/')]
        index += len(word)
        indexes.append(index)
    return indexes


if __name__ == '__main__':
    ## 全文
    score(std_path = '../io_files/199801_seg&pos.txt')
