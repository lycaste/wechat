from flask import Flask, request, make_response
import hashlib
import xml.etree.cElementTree as ET

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
			print("echostr",echostr)
			return make_response(echostr)

	if request.method == 'POST':
		xml_str = request.stream.read()
		xml = ET.fromstring(xml_str)
		toUserName = xml.find('ToUserName').text
		fromUserName = xml.find('FromUserName').text
		createTime = xml.find('CreateTime').text
		msgType = xml.find('MsgType').text
		if msgType != 'text':
			reply = '''
	            <xml>
	            <ToUserName><![CDATA[%s]]></ToUserName>
	            <FromUserName><![CDATA[%s]]></FromUserName>
	            <CreateTime>%s</CreateTime>
	            <MsgType><![CDATA[%s]]></MsgType>
	            <Content><![CDATA[%s]]></Content>
	            </xml>
	            ''' % (
				fromUserName,
				toUserName,
				createTime,
				'text',
				'Unknow Format, Please check out'
			)
			return reply
		content = xml.find('Content').text
		msgId = xml.find('MsgId').text
		print('aaaaa',type(content).__name__)
		print('aaaaa',content)
		print('aaaaa',content[::-1])
		reply = '''
	                <xml>
	                <ToUserName><![CDATA[%s]]></ToUserName>
	                <FromUserName><![CDATA[%s]]></FromUserName>
	                <CreateTime>%s</CreateTime>
	                <MsgType><![CDATA[%s]]></MsgType>
	                <Content><![CDATA[%s]]></Content>
	                </xml>
	                ''' % (fromUserName, toUserName, createTime, msgType, content)
		return reply
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

