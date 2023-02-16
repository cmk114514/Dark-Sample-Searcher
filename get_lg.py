from requests import get
from time import sleep

def fetch(name):
	return get(f'https://www.luogu.com.cn/problem/{name}?_contentOnly', headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'
	})

def get_samples(name):
	resp = fetch(name)
	while resp.status_code != 200:
		print(f'warn: fetched status code {resp.status_code}, retrying.')
		sleep(0.1)
		resp = fetch(name)
	if resp.json()['code'] != 200:
		print(f'warn: {name} is forbidden, {resp.json()["currentData"]["errorMessage"]}')
		return
	samples = resp.json()['currentData']['problem']['samples']
	sample_id = 0
	for [sample_input, sample_output] in samples:
		sample_id += 1
		open(f'data/lg/{name}_{sample_id}.in', 'w', encoding='utf-8').write(sample_input)
		open(f'data/lg/{name}_{sample_id}.out', 'w', encoding='utf-8').write(sample_output)
	print(f'info: fetched {name} with {sample_id} samples.')
print('From ??? to ???')
x, y = map(int, input().split())
names = [f'P{_}' for _ in range(x, y + 1)]
for name in names:
	get_samples(name)
	sleep(0.05)
