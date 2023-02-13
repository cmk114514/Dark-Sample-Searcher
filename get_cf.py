from bs4 import BeautifulSoup as bs
import requests as req
from os.path import join as pjoin
def get(cid, pid):
    print(f'Getting {cid}{pid}...')
    try:
        url = f'https://codeforces.com/{"gym" if cid >= 100000 else "contest"}/{cid}/problem/{pid}'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        txt = res.text.replace('<br/>', '\n').replace('<br />', '\n')
        s = bs(txt, 'lxml')
        si = s.select('#pageContent > div.problemindexholder > div.ttypography > div.problem-statement > div.sample-tests > div.sample-test > div.input > pre')
        so = s.select('#pageContent > div.problemindexholder > div.ttypography > div.problem-statement > div.sample-tests > div.sample-test > div.output > pre')
        assert len(si) == len(so)
        ret = []
        for i in range(0, len(si)):
            ca = si[i].select('div')
            if len(ca) != 0:
                in_txt = ''
                for j in ca:
                    in_txt += j.get_text() + '\n'
                ret.append((in_txt, so[i].get_text()))
            else:
                ret.append((si[i].get_text(), so[i].get_text()))
        return ret
    except Exception as e:
        print(f'Error {e}')
        return []
def save(cid, pid, sam):
    print(f'Saving {cid}{pid}...')
    try:
        for i in range(len(sam)):
            with open(pjoin('cf', f'{cid}_{pid}_{i + 1}.in'), 'w') as f:
                f.write(sam[i][0].strip())
            with open(pjoin('cf', f'{cid}_{pid}_{i + 1}.out'), 'w') as f:
                f.write(sam[i][1].strip())
    except Exception as e:
        print(f'Error {e}')
def get_and_save(cid):
    print(f'Getting {cid}...')
    try:
        url = f'https://codeforces.com/{"gym" if cid >= 100000 else "contest"}/{cid}'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        s = bs(res.text, 'lxml')
        p = s.select('#pageContent > div.datatable > div > table.problems > tr > td.id > a')
        for i in p:
            pid = i.get_text().strip()
            save(cid, pid, get(cid, pid))
    except Exception as e:
        print(f'Error {e}')
l, r = map(int, input('From ?~?: ').split())
for i in range(l, r + 1):
    get_and_save(i)
