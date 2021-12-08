import os
import re

def get_hash(token):
    return ord(token) & 0x7FFFFFFF

def del_old_file(file):
    if os.path.exists(file):
        os.remove(file)

# def post_process(segs):
#     now, result_segs = '', []
#     for i in range(len(segs)):
#         if segs[i].isascii():
#             now += segs[i]
#         elif len(now) > 0:
#             result_segs.append(now)
#             now = segs[i]
#         else:
#             result_segs.append(segs[i])
#     if len(now) > 0:
#         result_segs.append(now)
#     return post_process_1(result_segs)
#
# def post_process_1(segs):
#     now, result_segs = '', []
#     num = '０１２３４５６７８９'
#     for i in range(len(segs)):
#         if segs[i] in num:
#             now += segs[i]
#         elif len(now) > 0:
#             result_segs.append(now)
#             now = segs[i]
#         else:
#             result_segs.append(segs[i])
#     if len(now) > 0:
#         result_segs.append(now)
#     return result_segs


def post_process(bigram_segs):
    s1 = r'^[一二三四五六七八九十]+$'
    p1 = re.compile(s1)
    s2 = r'^[一二三四五六七八九十]+[月日]$'
    p2 = re.compile(s2)
    s3 = r'^[○零一二三四五六七八九十百千万亿兆分之点]+$'
    p3 = re.compile(s3)
    segs = []  # 存放后处理结果
    single_words = []  # 存放连续的单个字
    merged_segs = []
    i = 0
    if len(bigram_segs) == 1:
        merged_segs.extend(bigram_segs)
    else:
        while i < len(bigram_segs) - 1:
            if (p1.match(bigram_segs[i]) and p2.match(bigram_segs[i + 1])) or (p3.match(bigram_segs[i]) and p3.match(bigram_segs[i + 1])):
                for w in bigram_segs[i]:
                    merged_segs.append(w)
                for w in bigram_segs[i + 1]:
                    merged_segs.append(w)
                i += 2
            else:
                merged_segs.append(bigram_segs[i])
                i += 1
        if i == len(bigram_segs) - 1:
            merged_segs.append(bigram_segs[i])

    for idx, word in enumerate(merged_segs):
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

    year = r'[\uff10-\uff19一二三四五六七八九十零]{4}'
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


# s = ['十', '二', '月']
# print(post_process(s))
