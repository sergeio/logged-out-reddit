import functools
import json
import os
import re
import time
import unicodedata

from flask import Flask
from flask import make_response
from flask import jsonify
from flask import request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Not threadsafe!
url_cache = set()

def cache(fn):
    seen = dict()

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        bust_cache = kwargs.pop('bust_cache', False)
        key = json.dumps(*args, **kwargs)
        value = seen.get(key)
        if key not in seen or bust_cache:
            value = fn(*args, **kwargs)
            seen[key] = value
        return value
    return wrapped


@app.route('/cached-llm', methods=['POST'])
def cached_llm():
    request_json = request.get_json()
    bust_cache = request_json.pop('bust_cache', False)
    if 'stop' in request_json:
        request_json['stop'] = tuple(request_json['stop'])
    # json.dumps is not a good cache key
    llm_response = ask_llm_n_times(
        json.dumps(request_json), bust_cache=bust_cache)
    my_response = jsonify({'response': llm_response})
    my_response.headers.add("Access-Control-Allow-Origin", "*")
    return my_response


# @functools.lru_cache(1024)
@cache
def ask_llm_n_times(request_json, n=3):
    results = []
    for _ in range(n):
        try:
            results.append(int(ask_llm(request_json)))
        except Exception:
            pass
    return '%.1f' % (sum(results) / (len(results) or 1))

def ask_llm(request_json):
    json_dict = json.loads(request_json)
     #json_dict = dict(json_tuple)
    res = requests.post( 'http://localhost:11434/api/generate', json=json_dict)
    llm_response = res.json()['response']
    print('  ', 'asking', json_dict['prompt'], '\n', llm_response)
    return res.json()['response']


@app.route('/url/hide', methods=['POST'])
def hide_urls():
    global url_cache
    json = request.get_json()
    url_cache.update(json.get('urls', []))
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/url/is-hidden', methods=['POST'])
def is_hidden():
    global url_cache
    json = request.get_json()
    create_story_file(json['title'])
    response = make_response({'is_hidden': json['url'] in url_cache})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def create_story_file(name):
    directory = './__stories__/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = f"{directory}{valid_filename(name)}"
    with open(path, 'w') as f:
        pass

def valid_filename(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[/]', '', value)
    return value[:250]

