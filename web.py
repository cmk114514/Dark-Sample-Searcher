from flask import Flask, request, jsonify
import os, difflib
from os.path import join as pjoin
app = Flask('Dark Sample Searcher')
f = open('index.html')
html = f.read()
f.close()
def simi(x, y):
    return difflib.SequenceMatcher(None, x, y).ratio()
@app.get('/')
def index():
    return html
@app.get('/search')
def search():
    ret = []
    probset = request.args.get('p').strip()
    cin = request.args.get('i').strip()
    cout = request.args.get('o').strip()
    if len(cin) > 300 or len(cout) > 300:
        return jsonify([])
    checkIn = request.args.get('t') != '2'
    checkOut = request.args.get('t') != '0'
    for fn in os.listdir(probset):
        if fn.split('.')[-1] == 'in':
            try:
                v, cnt = 1, 0
                if checkIn:
                    with open(pjoin(probset, fn), encoding='utf-8') as f:
                        v *= simi(cin, f.read()); cnt += 1
                if checkOut:
                        with open(pjoin(probset, fn[: -3] + '.out'), encoding='utf-8') as f:
                            v *= simi(cout, f.read()); cnt += 1
                if cnt >= 2:
                    v **= 0.5
                if int(v * 100) >= 80:
                    qwq = fn.split('_')
                    if probset == 'lg':
                        ret.append({
                            "PID": qwq[0],
                            "SID": qwq[1].split('.')[0],
                            "SIM": int(v * 100)
                            })
                    elif probset == 'cf':
                        ret.append({
                            "CID": qwq[0],
                            "PID": qwq[1],
                            "SID": qwq[2].split('.')[0],
                            "SIM": int(v * 100)
                            })
                    elif probset == 'at':
                        ret.append({
                            "CID": qwq[0],
                            "PID": qwq[1],
                            "SID": qwq[2].split('.')[0],
                            "SIM": int(v * 100)
                            })
            except Exception:
                pass
    ret.sort(key=lambda x : -x['SIM'])
    return jsonify(ret)
app.run('127.0.0.1', 80)
