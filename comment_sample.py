from my_util import *
import re
import random as rd

def clean_1():
    comment_dict = {}
    #my_sentences = MySentences2('./data/comment/', 'gb2312')
    my_sentences = MySentences('./data/comment/', 'utf-8')
    for sent in my_sentences:
        # try:
        #     parts = sent.decode('gb2312').split('\t')
        # except:
        #     print(sent)
        parts = sent.split('\t')
        if len(parts) != 10:
            print('error: %s' % sent)
            continue
        comment_content = parts[6]
        score = parts[7]    # much more sensitive
        score_level = parts[8]  # not sensitive
        if comment_dict.get(score):
            comment_dict[score].append(comment_content)
        else:
            comment_dict[score] = [comment_content]
    # print(comment_dict)

    # 根据评分初步划分为两个档次，其中4-5份为好评，1-3分为差评
    good_comments = comment_dict['5']+comment_dict['4']
    bad_comments = comment_dict['1']+comment_dict['2']+comment_dict['3']

    print(len(good_comments))
    print(len(bad_comments))

    return good_comments, bad_comments

def sample(good_comments, bad_comments):
    express_freight = {1:[], 0:[], -1:[]}
    delivery_speed = {1:[], 0:[], -1:[]}
    express_speed = {1:[], 0:[], -1:[]}
    customer_experience = {1:[], 0:[], -1:[]}
    courier_service = {1:[], 0:[], -1:[]}
    installation_experience = {1:[], 0:[], -1:[]}
    return_experience = {1:[], 0:[], -1:[]}
    packaging_experience = {1:[], 0:[], -1:[]}

    g_sen = []
    b_sen = []
    for gcc in set(good_comments):
        sentences = re.split('[。！；：]', gcc)
        no_null_sens = [s for s in sentences if s != '']
        #g_sen += no_null_sens
        for gc_x in no_null_sens:
            groups = re.split('，', gc_x)

            start_idx = gcc.find(gc_x)
            gc = gcc[start_idx:start_idx + len(gc_x)+1]
            g_sen.append(gc)
            for group in groups:

                if ('快递' in group or '送货' in group or '配送' in group or '派送' in group) and \
                        ('哥' in group or '小伙子' in group or '师傅' in group or '员' in group): #快递员服务
                    courier_service[1].append(gc)
                    break

                if ('运费' in group) or ('快递' in group and ('贵' in group or '便宜' in group)):   #快递运费
                    express_freight[1].append(gc)
                    break

                if '发货' in group or '出货' in group:   #发货速度
                    delivery_speed[1].append(gc)
                    break

                if '快递' in group or '物流' in group or '送货' in group or '配送' in group or '派送' in group \
                        or '送达' in group or ('到货' in group and ('快' in group or '慢' in group)):  #快递速度
                    express_speed[1].append(gc) #泛泛地提到了快递或物流或送货，一般指快递速度和发货速度都很快
                    break

                if '包装' in group:   #包装体验
                    packaging_experience[1].append(gc)
                    break

                if '安装' in group or '装机' in group:  #安装体验
                    installation_experience[1].append(gc)
                    break

                if '客服' in group or '回复' in group or '答复' in group or '回答' in group \
                        or '理我' in group or '回我' in group: #客服体验
                    customer_experience[1].append(gc)
                    break

                if '退货' in group or '换货' in group or '给退' in group or '退了' in group or '退钱' in group:    #退货体验
                    return_experience[1].append(gc)
                    break

    for gcc in set(bad_comments):
        sentences = re.split('[。！；：]', gcc)
        no_null_sens = [s for s in sentences if s != '']
        #b_sen += no_null_sens
        for gc_x in no_null_sens:
            groups = re.split('，', gc_x)

            start_idx = gcc.find(gc_x)
            gc = gcc[start_idx:start_idx+len(gc_x)+1]
            b_sen.append(gc)
            for group in groups:

                if ('运费' in group) or ('快递' in group and ('贵' in group or '便宜' in group)):   #快递运费
                    express_freight[-1].append(gc)
                    break

                if ('快递' in group or '送货' in group or '配送' in group or '派送' in group) and \
                        ('哥' in group or '小伙子' in group or '师傅' in group or '员' in group): #快递员服务
                    courier_service[-1].append(gc)
                    break

                if '发货' in group or '出货' in group:   #发货速度
                    delivery_speed[-1].append(gc)
                    break

                if '快递' in group or '物流' in group or '送货' in group or '配送' in group or '派送' in group \
                        or ('到货' in group and ('快' in group or '慢' in group)):  #快递速度
                    express_speed[-1].append(gc) #泛泛地提到了快递或物流或送货，一般指快递速度和发货速度都很快
                    break

                if '包装' in group:   #包装体验
                    packaging_experience[-1].append(gc)
                    break

                if '安装' in group or '装机' in group:  #安装体验
                    installation_experience[-1].append(gc)
                    break

                if '客服' in group or '回复' in group or '答复' in group or '回答' in group \
                        or '理我' in group or '回我' in group: #客服体验
                    customer_experience[-1].append(gc)
                    break

                if '退货' in group or '换货' in group or '给退' in group or '退了' in group or '退钱' in group:    #退货体验
                    return_experience[-1].append(gc)
                    break

    ef_smp = rd.sample(express_freight[1], 1000) + rd.sample(express_freight[-1], 1000)
    ds_smp = rd.sample(delivery_speed[1], 1000) + rd.sample(delivery_speed[-1], 1000)
    es_smp = rd.sample(express_speed[1], 1000) + rd.sample(express_speed[-1], 1000)
    ce_smp = rd.sample(customer_experience[1], 1000) + rd.sample(customer_experience[-1], 1000)
    cs_smp = rd.sample(courier_service[1], 1000) + rd.sample(courier_service[-1], 1000)
    ie_smp = rd.sample(installation_experience[1], 1000) + rd.sample(installation_experience[-1], 1000)
    re_smp = rd.sample(return_experience[1], 1000) + rd.sample(return_experience[-1], 1000)
    pe_smp = rd.sample(packaging_experience[1], 1000) + rd.sample(packaging_experience[-1], 1000)

    all_smp = set(ef_smp+ds_smp+es_smp+ce_smp+cs_smp+ie_smp+re_smp+pe_smp)
    print(len(all_smp))
    print(len(all_smp)/16000)

    g_minus = set(g_sen) - all_smp
    b_minus = set(b_sen) - all_smp

    print(len(g_minus)/len(g_sen))
    print(len(b_minus)/len(b_sen))

    random_smp = rd.sample(g_minus, 2000)+rd.sample(b_minus, 2000)

    store2file('./data/cates2/express_freight.txt', ef_smp)
    store2file('./data/cates2/delivery_speed.txt', ds_smp)
    store2file('./data/cates2/express_speed.txt', es_smp)
    store2file('./data/cates2/customer_experience.txt', ce_smp)
    store2file('./data/cates2/courier_service.txt', cs_smp)
    store2file('./data/cates2/installation_experience.txt', ie_smp)
    store2file('./data/cates2/return_experience.txt', re_smp)
    store2file('./data/cates2/packaging_experience.txt', pe_smp)
    store2file('./data/cates2/random.txt', random_smp)

    print('finish')

def convert(inputfile, outputfile, flag):
    t_list = readFromFile(inputfile)
    rd.shuffle(t_list)
    id_t_list = ['%s-%05d\t%s' % (flag, idx, t.replace('\t', '')) for idx, t in enumerate(t_list)]
    store2file(outputfile, id_t_list)

#good_com, bad_com = clean_1()
# store2file('./data/good_comm_sample.txt', good_com)
# store2file('./data/bac_comm_sample.txt', bad_com)
#sample(good_com, bad_com)
# convert('./data/cates2/random.txt', './data/cates3/id_random.txt', 'RANDX')
# convert('./data/cates2/express_freight.txt', './data/cates3/id_express_freight.txt', 'KDYFX')
# convert('./data/cates2/delivery_speed.txt', './data/cates3/id_delivery_speed.txt', 'FHSDX')
# convert('./data/cates2/express_speed.txt', './data/cates3/id_express_speed.txt', 'KDSDX')
# convert('./data/cates2/customer_experience.txt', './data/cates3/id_customer_experience.txt', 'KFTYX')
# convert('./data/cates2/installation_experience.txt', './data/cates3/id_installation_experience.txt', 'AZTYX')
# convert('./data/cates2/return_experience.txt', './data/cates3/id_return_experience.txt', 'THHTY')
# convert('./data/cates2/packaging_experience.txt', './data/cates3/id_packaging_experience.txt', 'BZTYX')
# convert('./data/cates2/courier_service.txt', './data/cates3/id_courier_service.txt', 'KDYFW')
