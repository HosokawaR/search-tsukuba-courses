import json

from flask import Flask, jsonify, render_template, request

from .gen_syll_vec import gen_syll_vec
from .scrap import scrap_syll
from .search import search_lec

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_lecture():
    req = request.get_data(as_text=True)
    keywords = json.loads(req)["keywords"].split()
    print(keywords)
    try:
        l = search_lec(keywords)
    except KeyError:
        print('理解できず')
        return jsonify({"stat": 404})
    except Exception as e:
        print(e)
        return jsonify({"stat": 500})
    else:
        return jsonify({"stat": 0, "data": l})
    # デバック用
    # l = search_lec(keywords)
    # return jsonify({"stat": 0, "data": l})
