import os, json
Data = {}
for probset in ('lg', 'cf', 'at'):
    Data[probset] = {}
    for fn in os.listdir(os.path.join('data', probset)):
        if fn.split('.')[-1] == 'in':
            try:
                file = fn.split('.')[0]
                Data[probset][file] = {}
                with open(os.path.join('data', probset, fn), encoding = 'utf-8') as f:
                    Data[probset][file]['in'] = f.read().rstrip()
                with open(os.path.join('data', probset, fn[0: -3] + '.out'), encoding = 'utf-8') as f:
                    Data[probset][file]['out'] = f.read().rstrip()
            except Exception:
                del Data[probset][file]
    print('OK: ' + probset)
with open(os.path.join('data', 'data.json'), 'w') as f:
    f.write(json.dumps(Data, separators = (',', ':')))
