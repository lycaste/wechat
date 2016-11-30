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

		m = hashlib.sha1()
		m.update(repr(list).encode('utf-8'))
		hashcode = m.hexdigest()

		print(hashcode)
		print(signature)



		if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
			make_response(echostr)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

