from flask import *
import os, difflib, json
app = Flask('Dark Sample Searcher')
html, Data = None, None
with open('index.html') as f:
    html = f.read()
with open(os.path.join('data', 'data.json')) as f:
    Data = json.loads(f.read())
print('Init OK')
def simi(x, y):
    return difflib.SequenceMatcher(None, x, y).ratio()
@app.route('/')
def index():
    return html
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
@app.route('/search')
def search():
    ret = []
    probset = request.args.get('p').strip()
    cin = request.args.get('i').strip()
    cout = request.args.get('o').strip()
    if len(cin) > 300 or len(cout) > 300:
        return jsonify([])
    checkIn = request.args.get('t') != '2'
    checkOut = request.args.get('t') != '0'
    for file in Data[probset]:
        try:
            v, cnt = 1, 0
            if checkIn:
                v *= simi(cin, Data[probset][file]['in']); cnt += 1
            if checkOut:
                v *= simi(cout, Data[probset][file]['out']); cnt += 1
            v **= 1 / cnt
            if int(v * 100) >= 80:
                token = file.split('_')
                if probset == 'lg':
                    ret.append({
                        "PID": token[0],
                        "SID": token[1],
                        "SIM": int(v * 100)
                        })
                elif probset == 'cf':
                    ret.append({
                        "CID": token[0],
                        "PID": token[1],
                        "SID": token[2],
                        "SIM": int(v * 100)
                        })
                elif probset == 'at':
                    ret.append({
                        "CID": token[0],
                        "PID": token[1],
                        "SID": token[2],
                        "SIM": int(v * 100)
                        })
        except Exception:
            pass
    ret.sort(key=lambda x : -x['SIM'])
    return jsonify(ret)
app.run('127.0.0.1', 80)
