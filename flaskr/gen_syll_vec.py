import pickle
import sys

import pandas as pd

from .settings import EXIST_SYLL_TXT_PATH, SYLL_VEC_PATH, WEIGHTS
from .utl import conv_texts_to_vec


def is_weight_valid(weights):
    weights_sum = sum(weights.values())
    if weights_sum == 10:
        return True
    else:
        print('エラー: WEIGHTSの合計は10である必要があります。', file=sys.stderr)
        sys.exit(1)


def gen_syll_vec():
    df = pd.read_pickle(EXIST_SYLL_TXT_PATH)
    print(f'講義数: {len(df.index)}')

    vecs = []
    if is_weight_valid(WEIGHTS):
        for col, weight in WEIGHTS.items():
            if weight > 0:
                print(f'{col}を処理中')
                vecs.append(conv_texts_to_vec(df.loc[:, col].values.tolist()) * weight)
        with open(SYLL_VEC_PATH, "wb") as f:
            all_vecs = sum(vecs)
            pickle.dump(all_vecs, f)
