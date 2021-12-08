import os
import re

def get_hash(token):
    return ord(token) & 0x7FFFFFFF

def del_old_file(file):
    if os.path.exists(file):
        os.remove(file)

def post_process_mm(segs):
    now, result_segs = '', []
    for i in range(len(segs)):
        if segs[i].isascii():
            now += segs[i]
        elif len(now) > 0:
            result_segs.append(now)
            now = segs[i]
        else:
            result_segs.append(segs[i])
    if len(now) > 0:
        result_segs.append(now)
    return post_process_1(result_segs)

def post_process_1(segs):
    now, result_segs = '', []
    num = '０１２３４５６７８９'
    for i in range(len(segs)):
        if segs[i] in num:
            now += segs[i]
        elif len(now) > 0:
            result_segs.append(now)
            now = segs[i]
        else:
            result_segs.append(segs[i])
    if len(now) > 0:
        result_segs.append(now)
    return result_segs


def post_process(bigram_segs):
    segs = []  # 存放后处理结果
    single_words = []  # 存放连续的单个字
    for word in bigram_segs:
        # 将单个字放入single_words，直到出现多字的词
        if len(word) == 1:
            single_words.append(word)
        else:
            if len(single_words) > 1:
                segs.extend(handle_nums_letters(single_words))
            else:
                segs.extend(single_words)
            segs.append(word)
            single_words = []

    if len(single_words) > 0:
        segs.extend(handle_nums_letters(single_words))

    return segs


# 处理数词和英文单词
def handle_nums_letters(words):
    # 全角英文字母Unicode范围\uff41-\uff5a、\uff21-\uff3aa
    letters = r'[\uff41-\uff5a\uff21-\uff3aa-zA-Z]'
    p_letters = re.compile(letters)

    # 全角数字Unicode范围\uff10-\uff19
    nums = r'[\uff10-\uff19\.．·0-9-]'
    p_nums = re.compile(nums)

    # 中文数字中可能出现的词
    chinese_nums = ['○', '零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                    '百', '千', '万', '亿', '兆', '分', '之', '点']

    # 数字后面可能出现的单位
    units = ['％', '‰', '年', '月', '日', '时', '分', '秒']

    year = r'[\uff10-\uff19]{4}'
    p_year = re.compile(year)

    segs, single_words = [], []
    for word in words:
        if p_nums.match(word) or p_letters.match(word) or word in chinese_nums:
            single_words.append(word)
        elif word in units:
            # 如'10年'应该分为'10/ 年/ '，而非'10年/ '
            if word == '年' and not p_year.match(''.join(single_words)):
                if len(single_words) > 0:
                    segs.append(''.join(single_words))
                segs.append(word)
            # 但如果是年份，则不分，如'１９９８年/ '
            else:
                single_words.append(word)
                segs.append(''.join(single_words))
            single_words = []
        else:
            if len(single_words) > 0:
                segs.append(''.join(single_words))
            segs.append(word)
            single_words = []

    if len(single_words) > 0:
        segs.append(''.join(single_words))

    return segs
