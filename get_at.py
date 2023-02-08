from bs4 import BeautifulSoup as bs
import requests as req
from os.path import join as pjoin
import re
stitle = re.compile(r'Sample (In|Out)put \d+')
def get(cid, pid, url):
	print(f'Getting {cid}{pid}...')
	try:
		res = req.get(url, headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
		})
		s = bs(res.text, 'lxml')
		sa = s.select('#task-statement > span > span.lang-en > div > section')
		tsa = []
		for i in sa:
			if stitle.match(i.find('h3').get_text()):
				tsa.append(i.find('pre'))
		assert len(tsa) % 2 == 0
		ret = []
		for i in range(0, len(tsa), 2):
			ret.append((tsa[i].get_text(), tsa[i + 1].get_text()))
		return ret
	except Exception as e:
		print(f'Error {e}')
		return []
def save(cid, pid, sam):
	print(f'Saving {cid}{pid}...')
	try:
		for i in range(len(sam)):
			with open(pjoin('at', f'{cid}_{pid}_{i + 1}.in'), 'w') as f:
				f.write(sam[i][0].replace('\r', '').strip())
			with open(pjoin('at', f'{cid}_{pid}_{i + 1}.out'), 'w') as f:
				f.write(sam[i][1].replace('\r', '').strip())
	except Exception as e:
		print(f'Error {e}')
def get_and_save(cid):
	print(f'Getting {cid}...')
	try:
		url = f'https://atcoder.jp/contests/{cid}/tasks'
		res = req.get(url, headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
		})
		s = bs(res.text, 'lxml')
		p = s.select('#main-container > div.row > div:nth-child(2) > div > table > tbody > tr > td:nth-child(1) > a')
		for i in p:
			pid = i.get_text().strip().lower()
			lk = i.get('href')
			save(cid, pid, get(cid, pid, 'https://atcoder.jp' + lk))
	except Exception as e:
		print(f'Error {e}')
t, l, r = input('Type & From ?~?: ').split()
l, r = int(l), int(r)
for i in range(l, r + 1):
	get_and_save('%s%03d' % (t, i))
