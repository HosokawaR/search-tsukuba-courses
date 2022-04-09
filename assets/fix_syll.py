import re

import pandas as pd

import time
# 組み込むまでもないけど、便利そうだから残しとくファイル

def is_valid(text):
    if re.match(r"[0-9A-Z]{7}", text):
        return True
    else:
        print(f'{text}は不正な講義番号です。')
        return False


df = pd.read_pickle('../flaskr/data/lectures.pickle')
df.drop(columns='取得時刻')
df['取得時刻'] = time.time()

SE = {'講義番号': 'object',
      '講義名': 'object',
      '授業概要': 'object',
      '備考': 'object',
      '授業形態': 'object',
      '学位プログラム・コンピテンスとの関係': 'object',
      '授業の到達目標': 'object',
      'キーワード': 'object',
      '授業計画': 'object',
      '履修条件': 'object',
      '成績評価方法': 'object',
      '学修時間の割り当て及び授業外における学修方法': 'object',
      '教材・参考文献・配付資料等': 'object',
      'オフィスアワー等': 'object',
      'その他': 'object',
      '他の授業科目との関連': 'object',
      'ティーチングフェロー(TF)・ティーチングアシスタント(TA)': 'object',
      '取得時刻': 'float64',
      'シラバスは存在したか': 'bool'
      }

import numpy as np
# df.astype(SE)
# print(df.loc['01AB476', '取得時刻'])
# print()
# print(type(df.loc['01AB341', '取得時刻']))

# NaNを空白に置換
# df = df.replace(np.nan, '', regex=True)

# print(df[df['シラバスは存在したか']].isnull().any())
# print(df[df['シラバスは存在したか']].loc[:, '講義名'])
# print(df.loc[df.isnull().any(axis=1), 'シラバスは存在したか'])

# 保存
# df.to_pickle('../flaskr/data/lectures.pickle')
