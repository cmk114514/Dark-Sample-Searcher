from bs4 import BeautifulSoup as bs
import requests as req
from os.path import join as pjoin
def get(idx):
	print(f'Getting {idx}...')
	try:
		url = f'https://www.luogu.com.cn/problem/P{idx}'
		res = req.get(url, headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
		})
		s = bs(res.text, 'lxml')
		sa = s.select('#app > div.lg-container > article > pre > code')
		assert len(sa) % 2 == 0
		ret = []
		for i in range(0, len(sa), 2):
			ret.append((sa[i].get_text(), sa[i + 1].get_text()))
		return ret
	except Exception as e:
		print(f'Error {e}')
		return []
def save(idx, sam):
	print(f'Saving {idx}...')
	try:
		for i in range(len(sam)):
			with open(pjoin('lg', f'P{idx}_{i + 1}.in'), 'w') as f:
				f.write(sam[i][0].strip())
			with open(pjoin('lg', f'P{idx}_{i + 1}.out'), 'w') as f:
				f.write(sam[i][1].strip())
	except Exception as e:
		print(f'Error {e}')
l, r = map(int, input('From ?~?: ').split())
for i in range(l, r + 1):
	save(i, get(i))
