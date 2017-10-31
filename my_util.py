import os

class MySentences2(object):
    def __init__(self, dirname, charset):
        self.dirname = dirname
        self.charset = charset

    def __iter__(self):
        global line
        error_count = 0
        for fname in os.listdir(self.dirname):
            file = open(os.path.join(self.dirname, fname), encoding=self.charset)
            while True:
                try:
                    line = file.readline()
                    if not line:
                        #print('finish')
                        break
                except Exception as e:
                    if '0xbc' in str(e):
                        print('fatal error')
                        break
                    # print(e)
                    error_count += 1
                    continue
                # line = unicode(line, 'utf-8')
                # yield line.split()
                yield line
            print('error count: {}'.format(error_count))

class MySentences(object):
    def __init__(self, dirname, charset):
        self.dirname = dirname
        self.charset = charset

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding=self.charset):
            #for line in open(os.path.join(self.dirname, fname)):
                # line = unicode(line, 'utf-8')
                # yield line.split()
                yield line

def store2file(filename, str_list):
    w_file = open(filename, mode='w', encoding='utf-8')
    w_file.write('\n'.join(str_list))
    print('write to file '+filename)

def readFromFile(filename):
    r_file = open(filename, encoding='utf-8')
    res = r_file.read()
    t_list = res.split('\n')
    return [t for t in t_list if t != '']
