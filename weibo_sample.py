import os
import random

dir_1 = '/hadoop/ww/weibo'
dir_2 = '/hadoop/ww/weibo_compress'
charset = 'gbk'

def weibo_sample():
    dl1 = os.listdir(dir_1)
    dl2 = os.listdir(dir_2)
    rdm = random.sample(dl1+dl2, 30)
    w_file = open('./smp_list.txt', mode='w', encoding='utf-8')
    w_file.write('\n'.join(rdm))
    w_file.close()
