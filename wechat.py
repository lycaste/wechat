from flask import Flask, request, make_response
from config import Config
import hashlib
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def wechat():
	if request.method == 'GET':
		print("receive Get")
		data = request.args
		toekn = 'wechat_token'
		signature = data.get('signature','')
		timestamp = data.get('timestamp','')
		nonce = data.get('nonce','')
		echostr = data.get('echostr','')
		s = [timestamp, nonce, toekn]
		s.sort()
		s=''.join(s)
		m = hashlib.sha1()
		print(s)
		m.update(s.encode('utf-8'))
		hashcode = m.hexdigest()
		if (hashcode==signature):
			print(echostr)
			make_response(echostr)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

