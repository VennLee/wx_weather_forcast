# -*- coding: utf-8 -*-
import time
from flask import Flask,g,request,make_response,render_template
import hashlib
import urllib2

import xml.etree.ElementTree as ET
app = Flask(__name__)
# app.debug=True

# def get_pictext(title,description,picurl,url):
#     return  [title,description,picurl,url]

# @app.route('/',methods=['GET','POST'])
# def wechat_auth():
#     #微信验证
#     if request.method == 'GET':
#         token='weixin'
#         data = request.args
#         signature = data.get('signature','')
#         timestamp = data.get('timestamp','')
#         nonce = data.get('nonce','')
#         echostr = data.get('echostr','')
#         s = [timestamp,nonce,token]
#         s.sort()
#         s = ''.join(s)
#         if (hashlib.sha1(s).hexdigest() == signature):
#             return make_response(echostr)
#     #对话
#     else:
#         rec = request.stream.read()
#         xml_rec = ET.fromstring(rec)
#         to_user = xml_rec.find('ToUserName').text #消息的发送者
#         from_user = xml_rec.find('FromUserName').text #消息的接受者
#         msg_type=xml_rec.find('MsgType').text#消息类型
#         content=u'' #即将回复的内容
#         if msg_type=='text':#文本信息
#             # content = xml_rec.find('Content').text #消息内容
#             # if 'text'==content:
#             #     content=u'你好'
#             #     return render_template('reply_txt.html',toUser=from_user,fromUser=to_user,time_stamp=str(int(time.time())),Content=content)
#             # else:
#             #     content=u'呵呵!!'
#             #    return render_template('reply_txt.html',toUser=from_user,fromUser=to_user,time_stamp=str(int(time.time())),Content=content)
#             content=u'文本消息'
#         elif msg_type=='image':
#             content=u'图片消息'
#         elif msg_type=='voice':
#             content=u'语音消息'
#         elif msg_type=='video':
#             content=u'小视频'
#         elif msg_type=='location':
#             content=u'位置信息'
#         elif msg_type=='link':
#             content=u'链接'
#         elif msg_type=='event':
#             event=xml_rec.find('Event').text#事件类型
#             if event=='subscribe':
#                 content=u'关注'
#             if event=='unsubscribe':
#                 content=u'取关'
#             if event=='SCAN':
#                 content=u'扫码'
#             if event=='LOCATION':
#                 content=u'地理位置'
#             if event=='CLICK':
#                 content=u'点击自定义菜单'
#         else:
#             content=u'未知'
#         # return render_template('reply_txt.html',toUser=from_user,fromUser=to_user,time_stamp=str(int(time.time())),Content=content)
#         item1=get_pictext('hehe','test','http://imglf0.ph.126.net/R3EOmpgQ4FwSz4uP7uMZ-Q==/6630309102676745133.jpg','www.baidu.com')
#         item2=get_pictext('hehe2','test','http://imglf0.ph.126.net/R3EOmpgQ4FwSz4uP7uMZ-Q==/6630309102676745133.jpg','www.baidu.com')
#         item3=get_pictext(u'你好',u'这是一个测试','http://imglf.nosdn.127.net/img/SklVczZMM3QzelZKcXFNLzRjU1VIN0JiUE1JTGlra1M.jpeg?imageView&thumbnail=1680x0&quality=96&stripmeta=0','http://vennle.lofter.com/post/18c725_796f5fa')
#
#         items=[item1,item2,item3]
#         # print items[1][0]
#         return render_template('reply_pictext.html',toUser=from_user,fromUser=to_user,time_stamp=str(int(time.time())),item_num=len(items),items=items)
#
#     # return response
#     return 'default'
@app.route('/',methods=['GET','POST'])
def wechat_auth():
    #微信验证
    if request.method == 'GET':
        token='weixin'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    #对话
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        to_user = xml_rec.find('ToUserName').text #消息的发送者
        from_user = xml_rec.find('FromUserName').text #消息的接受者
        msg_type=xml_rec.find('MsgType').text#消息类型
        if msg_type=='text':
            content = xml_rec.find('Content').text#用户输入的消息内容
            content_city=content
            city=content.encode('UTF-8')
            url='http://api.map.baidu.com/telematics/v3/weather?location='+city+'&ak=1557cdbdaf2a1db4229cfb947438a7c5'
            response=urllib2.urlopen(url)
            html=response.read()
            weather=ET.fromstring(html)
            error_code=weather.findtext('./error')
            content=u''
            weather_dict={u'暴雨':u'\ue04b',u'阵雨':u'\ue13d',u'多云':u'\ue049',u'晴':u'\ue04a'}
            if error_code=='-3':
                content=u'你输入的城市不存在，请确定以后再输入'+u'\ue40d'
            else:
                w_data=weather.findtext('./results/weather_data/weather')
                if  weather_dict.has_key(w_data):
                    content=content_city+u'今天天气是'+weather_dict[w_data]
                else:
                    content=content_city+u'今天天气是'+w_data
                sugst1=weather.findtext('./results/index/des[1]')
                sugst2=weather.findtext('./results/index/des[3]')
                pm25=weather.findtext('./results/pm25')
                w_date=weather.findtext('./results/weather_data/date[1]')
                content=u'\ue404今天是'+w_date+u'\ue402'+content+u'\ue107PM25指数是'+pm25+u'\ue40c'+sugst1+sugst2
        else:
            content=msg_type



        return render_template('reply_txt.html',toUser=from_user,fromUser=to_user,time_stamp=str(int(time.time())),Content=content)
    return 'hehe'
