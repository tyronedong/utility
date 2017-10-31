from gensim.models.word2vec import *


def dict2list(inputfile):
    rd = file(inputfile)
    word_list = []
    for line in rd:
        split = line.split('\t')
        if len(split) != 2:
            print('error:', line)
            continue
        #word_list.append(unicode(split[0].strip(),'utf-8'))
        word_list.append(str(split[0], 'utf-8'))
    rd.close()
    return word_list

def list2txtvector(inputfile, outputfile):
    w_list = dict2list(inputfile)

    model = Word2Vec.load('../files/word2vec_model_0611/word2vec/data/model/news_word2vec.model')

    error_count = 0
    right_count = 0
    file_list = []
    for word in w_list:
        line_list = []
        line_list.append(word)
        try:
            for val in model.wv[word]:
                line_list.append(str(val))
            right_count+=1
            if right_count == 5000:
                print('top 5000 not in vocab:', error_count)
        except:
            print('not in vocab:', word)
            error_count += 1
        file_list.append('\t'.join(line_list))

    print('total not in vocab:', error_count)

    wf = file(outputfile,'w')
    wf.write('\n'.join(file_list).encode('utf-8'))
    wf.close()

    print('finish')

def gensim2vectorfile(word2vec_model_path, output_file):
    output_file = open(output_file, 'w')
    model = Word2Vec.load(word2vec_model_path)
    for idx, word in enumerate(model.wv.vocab):
        list = [str(i) for i in model[word]]
        list.insert(0, word.encode('utf-8'))
        output_file.write('\t'.join(list))
        output_file.write('\n')
        print(idx, word)
    output_file.close()

def test_vector_file(filename):
    f = open(filename)
    for line in f:
        print(line)

# list2txtvector('../files/kafang_dic.txt', '../files/news_vectors.txt')
# list2txtvector('../files/idf.txt', '../files/idf_vectors.txt')
# gensim2vectorfile('../data/model/seged_word2vec_train.model', '../data/model/news_vectors.txt')

# test_vector_file('../data/model/news_vectors.txt')
gensim2vectorfile('../data/comment_wrod2vec_raw.model', '../data/comment_vectors.txt')
