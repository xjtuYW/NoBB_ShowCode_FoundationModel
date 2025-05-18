import collections
import re
import pdb
END_TOKEN   = r'</w>'   # 用</w>表示单词结束

def get_word_freq_dict_dict(corpus):
    word_freq_dict = collections.defaultdict(int)
    for sentence in corpus:
        words = sentence.strip().split()
        for word in words:
            word_freq_dict[" ".join(list(word))+ " " + END_TOKEN] += 1
    return word_freq_dict


def get_pair_freq_dict(word_freq_dict):
    # 获取初始词表字符对统计信息
    pair_freq_dict  = collections.defaultdict(int)
    for word, freq in word_freq_dict.items():
        chars   = word.split()
        # 字符对统计
        for i in range(len(chars)-1):
            pair_freq_dict[(chars[i], chars[i+1])] += freq
    return pair_freq_dict

def get_vocab(word_freq_dict):
    vocab           = collections.defaultdict(int)
    for word, freq in word_freq_dict.items():
        chars   = word.split()
        # 字符统计
        for char in chars:
            vocab[char] += freq
    return vocab

def update_vocab_and_word_freq_dict(word_freq_dict, pair_freq_dict, vocab):
    # 获取最大频数字符对
    pair_with_max_freq = max(pair_freq_dict, key=pair_freq_dict.get)

    # 融合最大频数字符对
    merged_pair = re.escape(' '.join(pair_with_max_freq))

    # 定义正则表达式
    match_re = re.compile(r'(?<!\S)' + merged_pair + r'(?!\S)') # 目标pair左右两边得是空字符，如空格等

    # 将word_freq中满足pair_with_max_freq字符对合并
    new_word_freq = collections.defaultdict(int)
    for key in word_freq_dict:
        new_key = match_re.sub(''.join(pair_with_max_freq), key) # 满足则替换
        new_word_freq[new_key] = word_freq_dict[key]
    
    # 更新词表
    vocab[''.join(pair_with_max_freq)] = pair_freq_dict[pair_with_max_freq]
    vocab[pair_with_max_freq[0]] -= pair_freq_dict[pair_with_max_freq]
    vocab[pair_with_max_freq[1]] -= pair_freq_dict[pair_with_max_freq]
    
    return vocab, new_word_freq

def bpe(corpus=None, vocab_size:int=13, vocab=None, word_freq_dict=None):
    if vocab is None:
        word_freq_dict = get_word_freq_dict_dict(corpus)
        vocab          = get_vocab(word_freq_dict)
    pair_freq_dict          = get_pair_freq_dict(word_freq_dict)
    if len(vocab) < vocab_size:
        vocab, word_freq_dict = update_vocab_and_word_freq_dict(word_freq_dict, pair_freq_dict, vocab)
        bpe(corpus=corpus, vocab_size=vocab_size, vocab=vocab, word_freq_dict=word_freq_dict)
    return vocab
    
if __name__ == '__main__':
    # 定义个模拟语料库
    corpus = ["I am obama.", "I am banana!", "I like banana?"]
    vocab_size = 20
    vocab = bpe(corpus, vocab_size)
    print(vocab)