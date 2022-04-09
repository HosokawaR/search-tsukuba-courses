import sys

from flaskr import app, gen_syll_vec, scrap_syll


def production():
    app.run(host='0.0.0.0', port=80, debug=False)


def dev():
    app.run(host='127.0.0.1', port=5000, debug=True)


def update_syll_vec():
    gen_syll_vec()


def update_syll_txt():
    scrap_syll()


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        production()

    elif args[1] == 'dev':
        print('開発モードでサーバを起動します。')
        dev()

    elif args[1] == 'genvec':
        print('シラバスのベクトルファイルを生成します。')
        update_syll_vec()

    elif args[1] == 'scrap':
        print('シラバスデータを更新します。')
        update_syll_txt()

    else:
        print('引数エラー')
