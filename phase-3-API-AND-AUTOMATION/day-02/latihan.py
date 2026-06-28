import requests ; from datetime import datetime
url = "https://api.alternative.me/fng/"
k = requests.get(url)
print(k.json())

data = {
	'name' : 'test',
	'result' : [
			{'score' : '75', 'grade' : 'B'},
			{'score' : '90', 'grade' : 'A'}
		]
}

o = data['result'][0]
print("SCORE: ", o['score'])
print("GRADE: ", o['grade'])

unix = '1782604800'
unix = datetime.fromtimestamp(int(unix)).strftime("%Y/%m/%d %H:%M:%S")
print(unix)

