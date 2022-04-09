import csv
import os
import re
from time import sleep, time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from .settings import EXIST_SYLL_TXT_PATH, LECTURES_CSV_PATH, SYLL_TXT_PATH

COLUMNS = ['講義番号', '講義名', '授業概要', '備考', '授業形態', '学位プログラム・コンピテンスとの関係', '授業の到達目標',
           'キーワード', '授業計画', '履修条件', '成績評価方法', '学修時間の割り当て及び授業外における学修方法',
           '教材・参考文献・配付資料等', 'オフィスアワー等', 'その他', '他の授業科目との関連',
           'ティーチングフェロー(TF)・ティーチングアシスタント(TA)', '取得時刻', 'シラバスは存在したか']

COLUMNS_TYPE = {'講義番号': 'object',
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


def get_text_by_id(soup, id_name):
    try:
        return soup.find(id=id_name).get_text(strip=True)
    except:
        print(f'無し:{id_name}', end=' ')
        return ''


def scrap_by_lecture_id(lec_id):
    sleep(1)
    url = requests.get(f'https://kdb.tsukuba.ac.jp/syllabi/2020/{lec_id}/jpn/0/')
    soup = BeautifulSoup(url.content, 'html.parser')
    h1 = soup.find('h1').get_text()
    # バグあり
    if h1 == 'シラバスが見つかりません(EN)':
        print('シラバスはなかった', end=' ')
        empty_list = [''] * 17
        se = empty_list.extend([time(), False])
    else:
        se = [
            get_text_by_id(soup, 'course'),
            get_text_by_id(soup, 'title'),
            get_text_by_id(soup, 'summary-contents'),
            get_text_by_id(soup, 'note'),
            get_text_by_id(soup, 'style'),
            get_text_by_id(soup, 'outcomes'),
            get_text_by_id(soup, 'aim'),
            get_text_by_id(soup, 'keyword'),
            get_text_by_id(soup, 'topics'),
            get_text_by_id(soup, 'prerequisite'),
            get_text_by_id(soup, 'assessment'),
            get_text_by_id(soup, 'prepostworks'),
            get_text_by_id(soup, 'textbook'),
            get_text_by_id(soup, 'office'),
            get_text_by_id(soup, 'remark'),
            get_text_by_id(soup, 'relevants'),
            get_text_by_id(soup, 'tfta'),
            time(),
            True
        ]
    return se


def is_valid(text):
    # print(text)
    if re.match(r"[0-9A-Z]{7}", text):
        return True
    else:
        print(f'「{text}」は不正な講義番号です。')
        return False


def scrap_syll():
    if not os.path.isfile(SYLL_TXT_PATH):
        df = pd.DataFrame(index=[], columns=COLUMNS)
        df.to_pickle(SYLL_TXT_PATH)

    with open(LECTURES_CSV_PATH) as f:
        reader = csv.reader(f)
        lecture_id_list = [row[0] for row in reader if is_valid(row[0])]

        df = pd.read_pickle(SYLL_TXT_PATH)
        for lecture_id in lecture_id_list:
            progress = str(int((lecture_id_list.index(lecture_id) + 1) / len(lecture_id_list) * 100)).rjust(3)
            print(f'({progress}%)', end=' ')
            if lecture_id not in df.index:
                print(f'{lecture_id}の情報を取得中...', end='')
                try:
                    se = scrap_by_lecture_id(lecture_id)
                except Exception as e:
                    print('失敗')
                    print(e)
                else:
                    print('成功')
                    df.loc[lecture_id] = se
                    df.to_pickle(SYLL_TXT_PATH)
            else:
                print(f'{lecture_id}はすでに取得しています。')

        df.astype(COLUMNS_TYPE)
        df = df.replace(np.nan, '', regex=True)
        df.to_pickle(SYLL_TXT_PATH)
        df2 = df[df['シラバスは存在したか']]
        df2.to_pickle(EXIST_SYLL_TXT_PATH)
