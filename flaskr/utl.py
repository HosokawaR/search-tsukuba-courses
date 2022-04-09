import re

import gensim
import MeCab
import mojimoji
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

from .settings import ALLOWED_PARTS_TOP, MODEL_PATH

# model = gensim.models.Word2Vec.load(MODEL_PATH)
model = gensim.models.KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True)


def word2vec(word):
    return model.get_vector(word)


def is_allowed(text):
    return text in ALLOWED_PARTS_TOP
        


def text2wakati(text):
    tagger = MeCab.Tagger()
    parsed_text = tagger.parse(text)
    # print(parsed_text)
    rows = parsed_text.split('\n')
    wakati = []
    for row in rows:
        cells = re.split(',|\s+', row)
        if len(cells) > 2 and model.has_index_for(cells[0]) and is_allowed(cells[1]):
            wakati.append(cells[0])
    return ' '.join(wakati)


def clean_text(text):
    text = mojimoji.han_to_zen(text, digit=False, ascii=False)
    text = mojimoji.zen_to_han(text, kana=False)
    text = text.lower()
    text = text.replace(u'\n', ' ').replace(u'\xa0', ' ').replace('・', ' ')
    return text


# 文章をtf*idfで重み付けした(文章数 * ベクトル)の行列で変換する。
def conv_texts_to_vec(corpus):
    victories = TfidfVectorizer(token_pattern=u'(?u)\\b\\w+\\b')
    raw_document = [text2wakati(clean_text(text)) for text in tqdm(corpus, desc="  [tf*idfを計算中]")]
    # print(raw_document)
    # 単語ごとのtf*idf と 各文 の 行列
    # fit_transformは'・'とかも区切り文字として認識してしまうので注意！
    W = victories.fit_transform(raw_document)
    # feature_names = victories.get_feature_names()
    feature_names = victories.get_feature_names_out()
    W = W.toarray()
    # 単語ごとのベクトル行列
    l = [word2vec(word) for word in feature_names]
    V = np.asmatrix(l)
    sum_ = np.asmatrix([W.sum(axis=1)]).T + 0.00001  # 0除算を防ぐため...
    return (W @ V) / sum_
