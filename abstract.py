# 导入系统模块
import os
import sys
# imp模块提供了一个可以实现import语句的接口
from importlib import reload

# 异常处理
try:
    # reload方法用于对已经加载的模块进行重新加载，一般用于原模块有变化的情况
    reload(sys)
    # 设置系统的默认编码方式，仅本次有效，因为setdefaultencoding函数在被系统调用后即被删除
    sys.setdefaultencoding('utf-8')
except:
    pass

"""
展示textrank4zh模块的主要功能：
提取关键词
提取关键短语（关键词组）
提取摘要（关键句）
"""

# 导入编码转换模块
import codecs
# 从textrank4zh模块中导入提取关键词和生成摘要的类
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def analy(file):
    # 待读取的文本文件，一则新闻
    # 打开并读取文本文件
    text = codecs.open(file, 'r', 'utf-8').read()
    news_name = os.path.basename(file)

    # 创建分词类的实例
    tr4w = TextRank4Keyword()
    # 对文本进行分析，设定窗口大小为2，并将英文单词小写
    tr4w.analyze(text=text, lower=True, window=2)

    """输出"""
    file_handle = open('./abstract.txt', mode='a')
    file_handle.writelines(['新闻原稿：', news_name, '\n'])
    file_handle.write('关键词为：\n')
    # 从关键词列表中获取前20个关键词
    for item in tr4w.get_keywords(num=20, word_min_len=1):
        # 打印每个关键词的内容及关键词的权重
        file_handle.writelines([item.word, ' ', str(item.weight), '\n'])
    file_handle.write('\n')

    file_handle.write('关键短语为：\n')
    # 从关键短语列表中获取关键短语
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        file_handle.write(phrase)
    file_handle.write('\n')

    # 创建分句类的实例
    tr4s = TextRank4Sentence()
    # 英文单词小写，进行词性过滤并剔除停用词
    tr4s.analyze(text=text, lower=True, source='all_filters')

    file_handle.write('\n摘要为：\n')
    # 抽取3条句子作为摘要
    for item in tr4s.get_key_sentences(num=3):
        # 打印句子的索引、权重和内容
        file_handle.writelines([str(item.index), ' ', str(item.weight), ' ', item.sentence, '\n'])
    file_handle.write('\n')

'''
if __name__ == '__main__':
    fpath = './data/'
    d = os.walk(fpath)
    for dirpath, dirnames, filenames in d:
        for dirname in dirnames:
            for dp, dn, fn in os.walk(os.path.join(dirpath, dirname)):
                for f in fn:
                    news = str(os.path.join(dp, f))
                    analy(news)
'''
