import pickle

import numpy as np
import pandas as pd

from .settings import EXIST_SYLL_TXT_PATH, SYLL_VEC_PATH
from .utl import clean_text, word2vec


def cosine_similarity(X, Y):
    return abs(X @ Y.T) / np.sqrt(np.nansum(np.power(X, 2), axis=1) * np.nansum(np.power(Y, 2), axis=1))


def search_lec(keywords):
    with open(SYLL_VEC_PATH, "rb") as f:
        all_vec = pickle.load(f)
        v = np.asarray([word2vec(
            clean_text(word)) for word in keywords])
        v = np.mean(v, axis=0).reshape(1, -1)
        similarities = cosine_similarity(all_vec, v)
        result_indexes = reversed(np.argsort(
            similarities[:, 0], axis=0)[-20:].tolist())
        df = pd.read_pickle(EXIST_SYLL_TXT_PATH)
        l = []
        for result_index in result_indexes:
            se = df.iloc[result_index[0], :]
            l.append([
                90 - int(np.rad2deg(np.arccos(
                    similarities[result_index].tolist()[0][0])) / 90 * 100),
                se['講義名'],
                se['授業概要'],
                se['講義番号'],
            ])
        return l
