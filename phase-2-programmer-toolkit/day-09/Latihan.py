from pathlib import Path ; from datetime import datetime
import json

file = {
"Lol" : 1,
"Mol" : datetime.now(),
"Kol" : Path.cwd()
}
def handling(obj):
	if isinstance(obj, datetime):
		return obj.strftime("%d %m %Y,%H/%M/%S")
	elif isinstance(obj, Path):
		return str(obj)
k = json.dumps(file, default=handling)
print(k)