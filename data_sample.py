import os
import re
import xlwt
import random
from copy import deepcopy
from my_util import *


def filter_by_category(category):
    '''
    
    :param category: 'PER'-人名,'LOC'-地名,'ORG'-组织机构,'BRA'-品牌,'PRO'-产品,'TYP'-型号,'COL'-颜色,'SIZ'-规格
    :return: 
    '''
    tag = re.compile('<.*?>')
    totallist = []
    for doc in MySentences('./data/files', 'utf-8'):
        for line in re.split(r'[。；！]', doc):
            beg = line.find('<' + category + '>')
            sublist = []
            while beg != -1:
                end = line.find('</'+category+'>', beg)
                if end == -1:
                    print('error:'+line)
                    continue
                target = line[beg:(end+6)]
                # print(target+line)
                cur_res = '{0}\t{1}'.format(tag.sub('', target), tag.sub('', line.replace('\t', '')))
                sublist.append(cur_res)

                # print(cur_res)
                beg = line.find('<' + category + '>', beg + 1)
            if len(sublist)==0:
                continue
            # print(list(set(sublist)))
            sub_str = '&&'.join(set(sublist)).replace('\n','')
            print(sub_str)
            totallist.append(sub_str)

    print('total {} group'.format(len(totallist)))
    return totallist


def step_one_sample(source_file, encode):
    target_words = [line.split()[0]
                    for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                    if len(line.split()) == 2]
    sentiment_words = [line.split()[0]
                       for line in open('./data/Sentiment.txt', encoding='utf-8')
                       if len(line.split()) == 2]
    count = 0

    w_file = open('./data/jd_ali_target_sentence_all.txt', 'w', encoding='gbk')

    for line in MySentences(source_file, encode):
        tmp = deepcopy(line).replace('\n', '')
        for target in target_words:

            if target in tmp:
                # if count > 10000:
                #     break

                tmp = tmp.replace(target, '')
                count += 1
                #print('{0}:{1}:{2}'.format(count,target,line.replace('\n', '')))
                print(count)
                sen = '{}\t{}'.format(target,line)
                w_file.write(sen)
                continue
        # if count>10000:
        #     break
    w_file.flush()
    w_file.close()
    #print(target_words)
# store2file('./data/PRO_total.txt', filter_by_category('PRO'))
# step_one_sample('./data/news', 'gbk')

# file = open('./data/rawNews/test/wenzhang1_20170616171745.txt', encoding='gbk')
# error_count = 0
# right_count = 0
# while True:
#     try:
#         line = file.readline()
#         if not line:
#             print('finish')
#             break
#         # print(line)
#         right_count+=1
#         print('{}:{}'.format(right_count, line))
#     except UnicodeDecodeError as e:
#         error_count+=1
#         print('{}:{}'.format(error_count,e))
#     # print(line)
cur_sen = ''
count = 0
idx = 0
def pre_step_cut_sentence():
    global cur_sen
    global count
    global idx
    w_file = open('./data/unseged_news_corpus.txt', 'w', encoding='gbk')
    for doc in MySentences2('./data/rawNews', 'gbk'):
        #print(doc)
        count += 1
        if count > 1000:
            idx += 1
            w_file.flush()
            count = 0
            #print(str(idx)+':flush')

        doc = doc.replace('\n', '')
        doc = doc.replace('\u3000', ' ')
        doc = doc.replace('&nbsp;', ' ')
        title_content_pair = doc.split('\t')
        if len(title_content_pair) != 2 or title_content_pair[1] == 'content':
            continue
        if title_content_pair[0] == title_content_pair[1]:
            continue

        w_file.write(title_content_pair[0]+'\n')
        sens = re.split(r'([。！？；])', title_content_pair[1])
        for sen in sens:
            if sen == '':
                continue
            if sen in '。！？；':
                if cur_sen == '':
                    continue
                cur_sen += sen
                w_file.write(cur_sen + '\n')
                #w_file.
                cur_sen = ''
                continue
            cur_sen += sen.strip()
            # w_file.write(sen.strip())
        cur_sen = ''
        #print(cur_sen)

        #print(sens)
    print('finish')
    w_file.flush()
    w_file.close()

# pre_step_cut_sentence()
isMatch = False
def step_two_sample():
    global isMatch
    sentiment_words_pos = [line.split()[0]
                           for line in open('./data/Sentiment.txt', encoding='utf-8')
                           if len(line.split()) == 2 and line.split()[1]=='1.0']
    sentiment_words_neg = [line.split()[0]
                           for line in open('./data/Sentiment.txt', encoding='utf-8')
                           if len(line.split()) == 2 and line.split()[1] == '-1.0']

    #sentiment_filtered_list = []
    w_file = open('./data/jd_ali_target_sentence_filter.txt', 'w', encoding='gbk')
    for line in open('./data/jd_ali_target_sentence_all.txt', encoding='gbk'):
        isMatch = False
        for s_word in sentiment_words_neg:
            if s_word in line:
                #sentiment_filtered_list.append(line)
                w_file.write("neg\t{}".format(line))
                #w_file.write("{}:{}".format(s_word, line))
                print("{}:{}".format(s_word, line.replace('\n','')))
                isMatch = True
                break
        if isMatch:
            continue
        for s_word in sentiment_words_pos:
            if s_word in line:
                #sentiment_filtered_list.append(line)
                w_file.write("pos\t{}".format(line))
                #w_file.write("{}:{}".format(s_word, line))
                print("{}:{}".format(s_word, line.replace('\n','')))
                break

    w_file.flush()
    w_file.close()

# step_two_sample()
#tmp = ''
def step_three_sample():
    #global tmp
    pos_filter_list = []
    neg_filter_list = []
    for line in open('./data/jd_ali_target_sentence_filter.txt', encoding='gbk'):
        pairs = line.replace('\n','').split('\t')
        #filter_list.append(line.replace('\n',''))
        if pairs[0] == 'pos':
            pos_filter_list.append('{}\t{}'.format(pairs[1], pairs[2]))
        elif pairs[0] == 'neg':
            neg_filter_list.append('{}\t{}'.format(pairs[1], pairs[2]))
    all_list = []
    for line in open('./data/jd_ali_target_sentence_all.txt', encoding='gbk'):
        all_list.append(line.replace('\n',''))

    print(len(pos_filter_list))
    print(len(neg_filter_list))
    print(len(all_list))

    pos_sample_1500 = random.sample(pos_filter_list, 1400)
    neg_sample_1500 = random.sample(neg_filter_list, 1400)
    neu_sample_500 = random.sample(set(all_list)-(set(pos_sample_1500) | set(neg_sample_1500)), 450)
    sample = set(pos_sample_1500)|set(neg_sample_1500)|set(neu_sample_500)
    print(len(sample))

    target_words = [line.split()[0]
                       for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                       if len(line.split()) == 2]
    target_words_jd = [line.split()[0]
                    for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                    if len(line.split()) == 2 and line.split()[0] == '京东']
    target_words_ali = [line.split()[0]
                       for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                       if len(line.split()) == 2 and line.split()[0] == '阿里']

    app_list = []
    for sam in sample:
        cur_app_list = []
        target_list = []
        pair = sam.split('\t')
        target_list.append(pair[0])
        tmp = deepcopy(pair[1]).replace(pair[0], '')
        for target in target_words:
            if target == pair[0]:
                continue
            if target in tmp:
                target_list.append(target)
                cur_app_list.append('{}\t{}'.format(target, pair[1]))
                tmp = tmp.replace(target,'')
        if len(set(target_words_jd)&set(target_list))>0 and len(set(target_words_ali)&set(target_list))>0:
            app_list.extend(cur_app_list)

    print(len(app_list))

def step_four_sample():
    pos_filter_dict = {}
    neg_filter_dict = {}
    for line in open('./data/jd_ali_target_sentence_filter.txt', encoding='gbk'):
        pairs = line.replace('\n', '').split('\t')
        # filter_list.append(line.replace('\n',''))
        if pairs[0] == 'pos':
            # pos_filter_list.append('{}\t{}'.format(pairs[1], pairs[2]))
            if pos_filter_dict.get(pairs[2]):
                pos_filter_dict[pairs[2]].add(pairs[1])
            else:
                pos_filter_dict[pairs[2]] = set([pairs[1]])
        elif pairs[0] == 'neg':
            # neg_filter_list.append('{}\t{}'.format(pairs[1], pairs[2]))
            if neg_filter_dict.get(pairs[2]):
                neg_filter_dict[pairs[2]].add(pairs[1])
            else:
                neg_filter_dict[pairs[2]] = set([pairs[1]])
    all_dict = {}
    for line in open('./data/jd_ali_target_sentence_all.txt', encoding='gbk'):
        pairs = line.split('\t')
        if all_dict.get(pairs[1]):
            all_dict[pairs[1]].add(pairs[0])
        else:
            all_dict[pairs[1]] = set([pairs[0]])
            #all_dict.append(line.replace('\n', ''))

    print(len(pos_filter_dict.items()))
    print(len(neg_filter_dict.items()))
    print(len(all_dict.items()))

    pos_filter_dict_both = []
    pos_filter_dict_single = []
    neg_filter_dict_both = []
    neg_filter_dict_single = []
    abandon = set(['taobao','jd','JD','alibaba'])
    for (key, targets) in pos_filter_dict.items():
        if len(targets) > 5:
            continue
        if len(abandon & targets)>0:
            continue
        if isBothRelate(targets):
            if len(targets)>3:
                if random.randint(1,6) <=3:
                    continue
            pos_filter_dict_both.append((key, targets))
        else:
            if len(targets)>2:
                if random.randint(1,6) <= 3:
                    continue
            pos_filter_dict_single.append((key, targets))
    for (key, targets) in neg_filter_dict.items():
        if len(targets) > 5:
            continue
        if len(abandon & targets)>0:
            continue
        if isBothRelate(targets):
            if len(targets)>3:
                if random.randint(1,6) <=3:
                    continue
            neg_filter_dict_both.append((key, targets))
        else:
            if len(targets)>2:
                if random.randint(1,6) <=3:
                    continue
            neg_filter_dict_single.append((key, targets))

    print('pos_filter_both{}'.format(len(pos_filter_dict_both)))
    print('neg_filter_both{}'.format(len(neg_filter_dict_both)))
    print('pos_filter_single{}'.format(len(pos_filter_dict_single)))
    print('neg_filter_single{}'.format(len(neg_filter_dict_single)))

    both_pos_sample = random.sample(pos_filter_dict_both, 400)
    both_neg_sample = random.sample(neg_filter_dict_both, 400)

    pos_sample_1k = random.sample(pos_filter_dict_single, 1000)
    pos_sample_1k.extend(both_pos_sample)
    neg_sample_1k = random.sample(neg_filter_dict_single, 1000)
    neg_sample_1k.extend(both_neg_sample)
    neu_sample_3h = random.sample(all_dict.items(), 200)

    count = 0
    for (key,targets) in pos_sample_1k:
        count+= len(targets)
    print("pos"+str(count))
    count = 0
    for (key, targets) in neg_sample_1k:
        count += len(targets)
    print("neg" + str(count))
    count = 0
    for (key, targets) in neu_sample_3h:
        count += len(targets)
    print("neu" + str(count))

    sample_list = pos_sample_1k+neg_sample_1k+neu_sample_3h
    #sample_set = set(sample_list)
    redu_set = set()
    redu_sample_list=[]
    for (key, value) in sample_list:
        if key in redu_set:
            continue
        redu_set.add(key)
        redu_sample_list.append((key,value))

    print(len(sample_list))
    print(len(redu_sample_list))

    w_file = open('./data/jd_ali_target_sentence_unlabeled_9.csv', 'w', encoding='gbk')
    random.shuffle(redu_sample_list)
    macro_id = 1
    w_file.write(','.join(['Id','Label','Target','Content']))
    w_file.write('\n')
    for (key, targets) in redu_sample_list:
        if len(key) < 10 or len(key)> 100:
            continue
        micro_id = 1
        cur_list = []
        #print(targets)
        sorted_targets = sorted(targets)
        sorted_targets.reverse()
        #print(sorted_targets)
        tmp = deepcopy(key.replace('\n',''))
        for target in sorted_targets:
            cur_list.append((target, tmp.find(target)))
            tmp = tmp.replace(target, '')
            # w_file.write(','.join(['', target, key.replace('\n','')]))
            # w_file.write('\n')
            # micro_id += 1
        #print(sorted(cur_list, key=lambda student: student[1]))
        sorted_list = sorted(cur_list, key=lambda student: student[1])
        for target, idx in sorted_list:
            if target in ['奶茶妹妹']:
                continue
            w_file.write(','.join(['{:0>5}-{}'.format(macro_id, micro_id), '', target, key.replace('\n', '').replace(',','，')]))
            w_file.write('\n')
            micro_id += 1
        macro_id += 1
    w_file.flush()
    w_file.close()
    # print(len(sample_set))

    # pos_sample_1500 = random.sample(pos_filter_list, 1400)
    # neg_sample_1500 = random.sample(neg_filter_list, 1400)
    # neu_sample_500 = random.sample(set(all_list) - (set(pos_sample_1500) | set(neg_sample_1500)), 450)
    # sample = set(pos_sample_1500) | set(neg_sample_1500) | set(neu_sample_500)
    # print(len(sample))
    #
    # target_words = [line.split()[0]
    #                 for line in open('./data/jd_ali_words.txt', encoding='utf-8')
    #                 if len(line.split()) == 2]
    # target_words_jd = [line.split()[0]
    #                    for line in open('./data/jd_ali_words.txt', encoding='utf-8')
    #                    if len(line.split()) == 2 and line.split()[0] == '京东']
    # target_words_ali = [line.split()[0]
    #                     for line in open('./data/jd_ali_words.txt', encoding='utf-8')
    #                     if len(line.split()) == 2 and line.split()[0] == '阿里']
    #
    # app_list = []
    # for sam in sample:
    #     cur_app_list = []
    #     target_list = []
    #     pair = sam.split('\t')
    #     target_list.append(pair[0])
    #     tmp = deepcopy(pair[1]).replace(pair[0], '')
    #     for target in target_words:
    #         if target == pair[0]:
    #             continue
    #         if target in tmp:
    #             target_list.append(target)
    #             cur_app_list.append('{}\t{}'.format(target, pair[1]))
    #             tmp = tmp.replace(target, '')
    #     if len(set(target_words_jd) & set(target_list)) > 0 and len(set(target_words_ali) & set(target_list)) > 0:
    #         app_list.extend(cur_app_list)
    #
    # print(len(app_list))

# step_three_sample()

target_words_jd = [line.split()[0]
                       for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                       if len(line.split()) == 2 and line.split()[0] == '京东']
target_words_ali = [line.split()[0]
                        for line in open('./data/jd_ali_words.txt', encoding='utf-8')
                        if len(line.split()) == 2 and line.split()[0] == '阿里']
def isBothRelate(targets):
    global target_words_jd
    global target_words_ali

    if len(set(target_words_jd) & set(targets)) > 0 and len(set(target_words_ali) & set(targets)) > 0:
        return True
    else:
        return False

step_four_sample()