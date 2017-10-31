import re
import random
from my_util import *
zh_pattern = re.compile('.*[\u4e00-\u9fa5].*')

def sample(filename):
    jd_relate = ['京东','jd','1号店','刘强东','奶茶妹妹','章泽天','东哥','狗东','京准达']
    ali_relate = ['阿里','天猫','淘宝','taobao','alibaba','马云','支付宝','蚂蚁金服','余额宝','聚划算','马爸爸']

    # 初始化变量
    data_dict = {'京东':{1:set(),-1:set(),0:set()},
                 '阿里':{1:set(),-1:set(),0:set()},
                 '天猫':{1:set(),-1:set(),0:set()},
                 '淘宝':{1:set(),-1:set(),0:set()},
                 '蚂蚁金服':{1:set(),-1:set(),0:set()},
                 'jd':{1:set(),-1:set(),0:set()},
                 '1号店':{1:set(),-1:set(),0:set()},
                 'taobao':{1:set(),-1:set(),0:set()},
                 'alibaba':{1:set(),-1:set(),0:set()},
                 '东哥': {1: set(), -1: set(), 0: set()},
                 '余额宝': {1: set(), -1: set(), 0: set()},
                 '刘强东': {1: set(), -1: set(), 0: set()},
                 '奶茶妹妹': {1: set(), -1: set(), 0: set()},
                 '支付宝': {1: set(), -1: set(), 0: set()},
                 '章泽天': {1: set(), -1: set(), 0: set()},
                 '聚划算': {1: set(), -1: set(), 0: set()},
                 '马云': {1: set(), -1: set(), 0: set()},
                 '狗东': {1: set(), -1: set(), 0: set()},
                 '二手东': {1: set(), -1: set(), 0: set()},
                 '马爸爸': {1: set(), -1: set(), 0: set()},
                 '飞猪旅行': {1: set(), -1: set(), 0: set()},
                 '京准达': {1: set(), -1: set(), 0: set()},
                 'Alimama': {1: set(), -1: set(), 0: set()}}

    # 读取原始语料
    f = open(filename, encoding='utf-8')
    for line in f:
        parts = line.split('\t')
        if len(parts) != 3:
            continue

        if '震东哥' in parts[1] or '中东哥' in parts[1] or '二手东风' in parts[1] or '二手东方' in parts[1] or '狗东西' in parts[1] or '京东方' in parts[1] or '进球' in parts[1] or '                               ' in parts[1]:
            continue

        if not zh_pattern.match(parts[1]):
            continue

        if len(parts[1]) > 150:
            continue

        # if '京东' in parts[1]:
        #     data_dict['京东'].add(parts[1])
        #     continue
        # elif '阿里' in parts[1]:
        #     data_dict['阿里'].add(parts[1])
        #     continue
        # elif '天猫' in parts[1]:
        #     data_dict['天猫'].add(parts[1])
        #     continue
        # elif '淘宝' in parts[1]:
        #     data_dict['淘宝'].add(parts[1])
        #     continue
        # elif 'JD' in parts[1] or 'jd' in parts[1]:
        #     data_dict['jd'].add(parts[1])
        #     continue
        # elif '1号店' in parts[1] or '一号店' in parts[1] or '壹号店' in parts[1]:
        #     data_dict['1号店'].add(parts[1])
        #     continue
        # elif '蚂蚁金服' in parts[1] or '蚂蚁花呗' in parts[1]:
        #     data_dict['蚂蚁金服'].add(parts[1])
        #     continue
        # elif ('taobao' in parts[1] or 'Taobao' in parts[1]):
        #     if 'http' not in parts[1]:
        #         data_dict['taobao'].add(parts[1])
        #     continue
        # elif 'Alibaba' in parts[1] or 'alibaba' in parts[1]:
        #     data_dict['alibaba'].add(parts[1])
        #     continue
        # else:
        #     pass

        target = parts[0]
        if target == '211限时达' or target == '虾米网' or target == 'alimama':
            continue
        if '京东' in target:
            data_dict['京东'][int(parts[2])].add(parts[1])
        elif '阿里' in target:
            data_dict['阿里'][int(parts[2])].add(parts[1])
        elif '天猫' in target:
            data_dict['天猫'][int(parts[2])].add(parts[1])
        elif '淘宝' in target:
            data_dict['淘宝'][int(parts[2])].add(parts[1])
        elif 'JD' in target or 'jd' in target:
            data_dict['jd'][int(parts[2])].add(parts[1])
        elif '1号店' == target or '一号店' == target or '壹号店' == target:
            data_dict['1号店'][int(parts[2])].add(parts[1])
        elif '蚂蚁金服' == target or '蚂蚁花呗' == target:
            data_dict['蚂蚁金服'][int(parts[2])].add(parts[1])
        elif 'taobao' == target or 'Taobao' == target:
            if 'http' not in parts[1]:
                data_dict['taobao'][int(parts[2])].add(parts[1])
        elif 'Alibaba' == target or 'alibaba' == target:
            data_dict['alibaba'][int(parts[2])].add(parts[1])
        else:
            data_dict[target][int(parts[2])].add(parts[1])
            # if data_dict.get(target):
            #     data_dict[target][int(parts[2])].add(parts[1])
            # else:
            #     data_dict[target] = {}
            #     data_dict[target][1] = set()
            #     data_dict[target][-1] = set()
            #     data_dict[target][0] = set()
            #     data_dict[target][int(parts[2])].add(parts[1])
    f.close()

    # 过滤掉数量较少的目标词
    cleaned_dict = {}
    for target, sen_dict in data_dict.items():
        count = len(sen_dict[1]) + len(sen_dict[-1]) + len(sen_dict[0])
        if count < 100:
            continue
            #data_dict.pop(target)
        cleaned_dict[target] = sen_dict
        print('%s:%s'%(target, count))

    # 开始采样
    set_2500 = ['京东', '刘强东']
    set_2000 = ['阿里', '马云']
    set_1000 = ['1号店', '奶茶妹妹', '章泽天', 'jd', '天猫', '淘宝', '支付宝', '蚂蚁金服', '余额宝']
    set_500 = ['东哥', '聚划算']
    set_100 = ['京准达', '狗东', '马爸爸', 'taobao', 'alibaba']

    jd_smp = set(random.sample(cleaned_dict['京东'][1], 1250)+random.sample(cleaned_dict['京东'][-1], 1250))
    liu_smp = set(random.sample(cleaned_dict['刘强东'][1], 1250)+random.sample(cleaned_dict['刘强东'][-1], 1250))

    ali_smp = set(random.sample(cleaned_dict['阿里'][1], 1000)+random.sample(cleaned_dict['阿里'][-1], 1000))
    mayun_smp = set(random.sample(cleaned_dict['马云'][1], 1000)+random.sample(cleaned_dict['马云'][-1], 1000))

    no1_smp = set(random.sample(cleaned_dict['1号店'][1], 500)+random.sample(cleaned_dict['1号店'][-1], 500))
    mtea_smp = set(random.sample(cleaned_dict['奶茶妹妹'][1], 500)+random.sample(cleaned_dict['奶茶妹妹'][-1], 500))
    zzt_smp = set(random.sample(cleaned_dict['章泽天'][1], 500) + random.sample(cleaned_dict['章泽天'][-1], 480) + random.sample(cleaned_dict['章泽天'][0], 20))
    ljd_smp = set(random.sample(cleaned_dict['jd'][1], 430) + random.sample(cleaned_dict['jd'][-1], 210) + random.sample(cleaned_dict['jd'][0], 360))

    tm_smp = set(random.sample(cleaned_dict['天猫'][1], 500) + random.sample(cleaned_dict['天猫'][-1], 500))
    tb_smp = set(random.sample(cleaned_dict['淘宝'][1], 500) + random.sample(cleaned_dict['淘宝'][-1], 500))
    zfb_smp = set(random.sample(cleaned_dict['支付宝'][1], 500) + random.sample(cleaned_dict['支付宝'][-1], 500))
    myjf_smp = set(random.sample(cleaned_dict['蚂蚁金服'][1], 500) + random.sample(cleaned_dict['蚂蚁金服'][-1], 400) + random.sample(cleaned_dict['蚂蚁金服'][0], 100))
    yeb_smp = set(random.sample(cleaned_dict['余额宝'][1], 500) + random.sample(cleaned_dict['余额宝'][-1], 500))

    dg_smp = set(random.sample(cleaned_dict['东哥'][1], 180) + random.sample(cleaned_dict['东哥'][-1], 290) + random.sample(cleaned_dict['东哥'][0], 30))
    jhs_smp = set(random.sample(cleaned_dict['聚划算'][1], 250) + random.sample(cleaned_dict['聚划算'][-1], 140) + random.sample(cleaned_dict['聚划算'][0], 110))

    jzd_smp = set(cleaned_dict['京准达'][1]|cleaned_dict['京准达'][-1]|cleaned_dict['京准达'][0])
    gd_smp = set(cleaned_dict['狗东'][1]|cleaned_dict['狗东'][-1] | cleaned_dict['狗东'][0])

    mbb_smp = set(cleaned_dict['马爸爸'][1]|cleaned_dict['马爸爸'][-1]|cleaned_dict['马爸爸'][0])
    ltb_smp = set(cleaned_dict['taobao'][1]|cleaned_dict['taobao'][-1]|cleaned_dict['taobao'][0])
    lali_smp = set(cleaned_dict['alibaba'][1]|cleaned_dict['alibaba'][-1]|cleaned_dict['alibaba'][0])

    cross_jd_ali_smp = set(random.sample(cleaned_dict['京东'][1]&cleaned_dict['阿里'][1], 1000)
                           +random.sample(cleaned_dict['京东'][-1]&cleaned_dict['阿里'][-1], 1000))
    cross_liu_ma_smp = set((cleaned_dict['刘强东'][1]&cleaned_dict['马云'][1])
                           |(cleaned_dict['刘强东'][-1]&cleaned_dict['马云'][-1])
                           |(cleaned_dict['刘强东'][0]&cleaned_dict['马云'][0]))
    cross_jd_tm_smp = set(random.sample(cleaned_dict['京东'][1]&cleaned_dict['天猫'][1], 1000)
                          +random.sample(cleaned_dict['京东'][-1]&cleaned_dict['天猫'][-1], 1000))
    cross_jd_ma_smp = set((cleaned_dict['京东'][1]&cleaned_dict['马云'][1])
                           |(cleaned_dict['京东'][-1]&cleaned_dict['马云'][-1])
                           |(cleaned_dict['京东'][0]&cleaned_dict['马云'][0]))
    cross_liu_ali_smp = set((cleaned_dict['刘强东'][1]&cleaned_dict['阿里'][1])
                           |(cleaned_dict['刘强东'][-1]&cleaned_dict['阿里'][-1])
                           |(cleaned_dict['刘强东'][0]&cleaned_dict['阿里'][0]))

    single_whole = jd_smp|liu_smp|ali_smp|mayun_smp|no1_smp|mtea_smp|zzt_smp|ljd_smp|tm_smp|tb_smp|zfb_smp|myjf_smp\
                   |yeb_smp|dg_smp|jhs_smp|jzd_smp|gd_smp|mbb_smp|ltb_smp|lali_smp
    cross_whole = cross_jd_ali_smp|cross_liu_ma_smp|cross_jd_tm_smp|cross_jd_ma_smp|cross_liu_ali_smp

    single_whole = list(single_whole-cross_whole)
    cross_whole = list(cross_whole)

    print('single:%s'%len(single_whole))
    print('cross:%s'%len(cross_whole))

    r1 = int(len(single_whole)/8)
    r2 = int(len(cross_whole)/2)

    l_single=[]
    for i in range(8):
        start = r1*i
        end = start+r1
        if i == 7:
            end = len(single_whole)+1
        l_single.append(single_whole[start:end])

    l_whole=[]
    for i in range(2):
        start = r2*i
        end = start+r2
        if i == 1:
            end = len(cross_whole)+1
        l_whole.append(cross_whole[start:end])

    return l_single, l_whole

    # jd_count = 0
    # ali_count = 0
    # jd_set = set([])
    # ali_set = set([])
    # for target, sen_set in cleaned_dict.items():
    #     print('%s:%s' % (target, len(sen_set)))
    #     if target in jd_relate:
    #         jd_count+=len(sen_set)
    #         jd_set|=sen_set
    #     elif target in ali_relate:
    #         ali_count+=len(sen_set)
    #         ali_set|=sen_set
    # print('Trouva 的模式本质与大型电商平台 Amazon、阿里等是接近的，其产品定位与京东、聚美优品差异不大，而它最独特的地方在于整合小众品牌实体店的思维。\n' in jd_set)
    # print('Trouva 的模式本质与大型电商平台 Amazon、阿里等是接近的，其产品定位与京东、聚美优品差异不大，而它最独特的地方在于整合小众品牌实体店的思维。\n' in ali_set)
    # both_set = jd_set&ali_set
    # maliu_set = cleaned_dict['马云']&cleaned_dict['刘强东']
    # jdali_set = cleaned_dict['阿里']&cleaned_dict['京东']
    # jdtm_set = cleaned_dict['天猫']&cleaned_dict['京东']
    # print('jd:%s'%jd_count)
    # print('ali:%s'%ali_count)
    # print('both:%s'%len(both_set))
    #[print(sen) for sen in both_set]
    #print(cleaned_dict)

def do_sample():
    l_s, l_w = sample('data/target_news_pred_3.txt')
    for i in range(len(l_s)):
        store2file('data/target_news/s_corpus_%s.txt'%(i+1), l_s[i])
    for i in range(len(l_w)):
        store2file('data/target_news/w_corpus_%s.txt'%(i+1), l_w[i])

def convert(inputfile, outputfile, flag):
    t_list = readFromFile(inputfile)
    random.shuffle(t_list)
    id_t_list = ['%s-%05d\t%s' % (flag, idx, t.replace('\t', '')) for idx, t in enumerate(t_list)]
    store2file(outputfile, id_t_list)

id_ls = ['ONEXX','TWOXX','THREE', 'FOURX','FIVEX','SIXXX','SEVEN','EIGHT']
ID_ls = ['TENXX', 'ELEVE']
for i in range(8):
    convert('data/target_news/s_corpus_%s.txt'%(i+1), 'data/target_news/id_s_corpus_%s.txt'%(i+1), id_ls[i])
for i in range(2):
    convert('data/target_news/w_corpus_%s.txt'%(i+1), 'data/target_news/id_w_corpus_%s.txt'%(i+1), ID_ls[i])

#print(zh_pattern.match('【你好'))
