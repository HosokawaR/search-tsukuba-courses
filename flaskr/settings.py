# ベクトルモデルのパス
# MODEL_PATH = 'flaskr/models/siroyagi/word2vec.gensim.model'
MODEL_PATH = 'flaskr/models/wikientvec/entity_vector.model.bin'

# 行列への変換を許可する品詞
# トップレベルで許可するもの
ALLOWED_PARTS_TOP = ['名詞', '動詞']

# MEMO
# 接尾語 〇〇学 を含めるベキか
# 動詞は標準形に治すか
# ひらがなは漢字にすべきか

# シラバスの文章のパス
SYLL_TXT_PATH = 'flaskr/data/lectures.pickle'

# 存在が確認されたシラバスの文章のパス
EXIST_SYLL_TXT_PATH = 'flaskr/data/exist_lectures.pickle'

# シラバスのベクトルのパス
SYLL_VEC_PATH = "flaskr/data/syll_vec.pickle"

# スクレイピングする講義番号が記録されたcsvへのパス
# 文字コードはUTF-8にすること
LECTURES_CSV_PATH = "flaskr/data/kdb.csv"

# シラバス→ベクトル変換の重み付け
# 少数はうまく計算できないので禁止
WEIGHTS = {'講義番号': 0,
           '講義名': 4,
           '授業概要': 3,
           '備考': 0,
           '授業形態': 0,
           '学位プログラム・コンピテンスとの関係': 0,
           '授業の到達目標': 0,
           'キーワード': 3,
           '授業計画': 0,
           '履修条件': 0,
           '成績評価方法': 0,
           '学修時間の割り当て及び授業外における学修方法': 0,
           '教材・参考文献・配付資料等': 0,
           'オフィスアワー等': 0,
           'その他': 0,
           '他の授業科目との関連': 0,
           'ティーチン グフェロー(TF)・ティーチングアシスタント(TA)': 0,
           '取得時刻': 0,
           'シラバスは存在したか': 0
           }

