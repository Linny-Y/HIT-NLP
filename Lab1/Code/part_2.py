Dic_File = '../io_files/dic.txt'
FMM_File = '../io_files/seg_FMM.txt'
BMM_File = '../io_files/seg_BMM.txt'
Test_File = '../io_files/test.txt'
'''
    3.2 正反向最大匹配分词实现
    输入文件：199801_sent.txt（1998 年 1 月《人民日报》语料，未分词）dic.txt(自己形成的分词词典)
    输出：seg_FMM.txt 和 seg_BMM.txt(正反向最大匹配分词结果，格式参照分词语料 “词/_词/_......”)
'''
Max_Len = 0  # 最大词长
Words = []  # 词典列表

# 读取词典内容存入 Words
def get_dic(dic_path = Dic_File):
    global Max_Len
    with open(dic_path, 'r') as dic_file: 
        lines = dic_file.readlines()  # 按行读取词典内容
    for line in lines:
        # line_len = line.find('\n')
        # if(line_len == -1):
        #     line_len = len(line)
        line = line.strip()  ### 去除词后可能带有的 '\n'
        line_len = len(line) # 词长
        # print(line_len)
        Words.append(line[0 : line_len])  # 去除换行符存入词典列表
        if(line_len > Max_Len):
            Max_Len = line_len  # 更新最大词长

# 正向最大匹配分词
def FMM(test_path = Test_File, fmm_path = FMM_File):
    with open(test_path, 'r') as test_file:
        lines = test_file.readlines()
    with open(fmm_path, 'w') as fmm_file:
        for line in lines:
            line = line.strip() # 去除结尾换行符
            # print(line[0:len(line)-10])
            seg_list = [] # 分割后字段
            while len(line) > 0:
                tryword = line[0:Max_Len if len(line) > Max_Len else len(line)] # 取最大词长的字符串
                while tryword not in Words:
                    if len(tryword) == 1:  # 字串长度为1，跳出循环
                        break
                    tryword = tryword[0 : len(tryword)-1]  # 减小词长
                # 找到对应词
                seg_list.append(tryword)
                if not tryword.isascii() or (len(tryword) == 1 and not line[1].isascii()):  # 当前位或下一位不在ASCII码中 进行分割
                    seg_list.append('/ ')  # 用 '/' 和 ' ' 进行分隔
                line = line[len(tryword): ]
            fmm_file.write(''.join(seg_list) + '\n')  # 写入换行符
        print('FMM cut over!')

# 反向最大匹配分词                
def BMM(test_path = Test_File, bmm_path = BMM_File):
    with open(test_path, 'r') as test_file:
        lines = test_file.readlines()
    with open(bmm_path, 'w') as bmm_file:
        for line in lines:
            line = line.strip() # 去除结尾换行符
            seg_list = [] # 分割后字段
            while len(line) > 0:
                tryword = line if len(line) < Max_Len else line[len(line) - Max_Len:] # 从后开始 取最大词长的字符串
                while tryword not in Words:
                    if len(tryword) == 1:  # 字串长度为1，跳出循环
                        break
                    tryword = tryword[1 : ]  # 减小词长
                # 找到对应词
                seg_list.insert(0 , tryword) 
                if not tryword.isascii():  # 当前位或下一位不在ASCII码中 进行分割
                    seg_list.insert(0 , '/ ')  # 在词前用 '/' 和 ' ' 进行分隔
                line = line[ : len(line)-len(tryword)]
            if line != '':
                seg_list.append('/ ')
            bmm_file.write(''.join(seg_list) + '\n')  # 写入换行符
        print('BMM cut over!')



if __name__ == '__main__':
    get_dic()
    # FMM()
    BMM()