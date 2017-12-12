# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,session,g,send_from_directory,make_response,jsonify
from werkzeug import secure_filename
import config
from models import User,Question,Answer,YX_Aiml,Answer2
from exts import db
from decorators import login_required
from sqlalchemy import or_
import re
import sys
import aiml
import os
import security
import json
import random
import urllib
import datetime
import uuid
from spider.mysqlconnectortodayhit import mysql
from sendcode import sendmscode
from testRank import articleKey
from bs4 import BeautifulSoup
#sql = mysql()  # 连接爬虫数据库，并初始化游标
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
global kernel
kernel = aiml.Kernel()
flag = True

@app.route('/resetpassword/',methods=['GET','POST'])
def resetpassword():
    if request.method == 'GET':
        return render_template('resetpassword.html')
    else:
        telephone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        yzm = request.form.get('yzm')
        ip = request.remote_addr
        #进行手机号码验证是否注册
        user = User.query.filter(User.telephone == telephone).first()
        if user and yzm == yzmdict[ip][1]:
            # 随机生成4位salt
            salt = security.create_salt()
            password = security.create_md5(password1, salt)
            user.password=password
            user.salt=salt
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        elif not user:
            return render_template('resetpassword_warning.html',flag=1)
        else:
            return render_template('resetpassword_warning.html',flag=2)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/contactAdmin/')
def contactAdmin():
    return render_template('contactadmin.html')

@app.route('/label/')
@login_required
def label():
    try:
        keylist = []
        with open("/home/ubuntu/HITChat/userarticle.txt","r") as f:
            for line in f.readlines():
                keylist.append(line.strip())
        return render_template('label.html',keylist=keylist,usermsg=g.user, picid=str(g.user.picid))
    except:
        return render_template('404.html')

@app.route('/news/')
@login_required
def news():
    try:
        try:
            sql = mysql()  # 连接爬虫数据库，并初始化游标
            dataSql = sql.select('slideright1')
            datajwc = sql.select('jwcarticlehtml')
            datatencent = sql.select('tencentnews')
            #print datajwc[0][2]
            sql.conn.close()
            return render_template('news.html',dataSql=dataSql,datajwc=datajwc,datatencent=datatencent,usermsg=g.user, picid=str(g.user.picid))
        except:
            return render_template('404.html')
    except:
        return render_template('404.html')

@app.route('/')
@login_required
def index():
    sql = mysql()  # 连接爬虫数据库，并初始化游标
    dataSql = sql.selectTop10('slideright1')
    datajwc = sql.selectTop10('jwcarticlehtml')
    #datatencent = sql.select('tencentnews')
    #print datajwc[0][2]
    sql.conn.close()
    #print datajwc
    context = {
         'questions': Question.query.order_by(db.desc(Question.create_time)).all()
    }
    allq = Question.query.order_by(db.desc(Question.create_time)).all()
    picids = {}
    for q in allq:
        picids[q.id] = str(q.author.picid)

    imgs = {}
    papers = []
    count = 1
    for question in context['questions']:
        if (count>6):
            break
        if (question.label=='旅游'):
            try:
                soup = BeautifulSoup(question.content,'html.parser')
                imgway = "http://www.hitchat.cn:5000" + soup.img['src']
                imgs[question.id] = imgway
                papers.append(question)
                count+=1
            except:
                pass

    foodimgs = {}
    foodpapers = []
    count = 1
    for question in context['questions']:
        if (count>10):
            break
        if (question.label=='美食'):
            try:
                soup = BeautifulSoup(question.content,'html.parser')
                imgway = "http://www.hitchat.cn:5000" + soup.img['src']
                foodimgs[question.id] = imgway
                foodpapers.append(question)
                count+=1
            except:
                pass

    educationimgs = {}
    educationpapers = []
    count = 1
    for question in context['questions']:
        if (count>10):
            break
        if (question.label=='教育'):
            try:
                soup = BeautifulSoup(question.content,'html.parser')
                imgway = "http://www.hitchat.cn:5000" + soup.img['src']
                educationimgs[question.id] = imgway
                educationpapers.append(question)
                count+=1
            except:
                pass

    return render_template('index.html', dataSql=dataSql,datajwc=datajwc,usermsg=g.user, picid=str(g.user.picid), picids=picids, imgs=imgs, papers=papers, foodimgs=foodimgs, foodpapers=foodpapers, educationimgs=educationimgs, educationpapers=educationpapers, **context)


@app.route('/classify')
@login_required
def classify():
    try:
        context = {
            'questions': Question.query.order_by(db.desc(Question.create_time)).all()
        }
        return render_template('classify.html',**context)
    except:
        return render_template('404.html')
###################################################################
#修改基本信息
@app.route('/basicmessage/')
@login_required
def basicmessage():
    try:
        return render_template('BasicMessage.html', usermsg=g.user, picid=str(g.user.picid))
    except:
        return render_template('404.html')

#修改个性信息
@app.route('/personalitymessage/')
@login_required
def personalitymessage():
    try:
        return render_template('PersonalityMessage.html', usermsg=g.user, picid=str(g.user.picid))
    except:
        return render_template('404.html')

#展示基本信息
@app.route('/showbasicmessage/<msgid>', methods=['POST', 'GET'])
@login_required
def showbasicmessage(msgid):
    try:
        username = request.form.get('username')
        realname = request.form.get('realname')
        gender = request.form.get('gender')
        institute = request.form.get('institute')
        contactway = request.form.get('contactway')
        birthyear = request.form.get('birthyear')
        birthmonth = request.form.get('birthmonth')
        birthday = request.form.get('birthday')

        # 得到目标用户的User表
        usermsg = User.query.filter(User.id == msgid).first()
        if username:
            usermsg.username = username
        if realname:
            usermsg.realname = realname
        if gender:
            usermsg.gender = gender
        if contactway:
            usermsg.contactway = contactway
        if birthyear:
            usermsg.birthyear = birthyear
        if birthmonth:
            usermsg.birthmonth = birthmonth
        if birthday:
            usermsg.birthday = birthday
        if institute:
            usermsg.institude = institute

        db.session.add(usermsg)
        db.session.commit()
        usermsg = User.query.filter(User.id == msgid).first()

        return render_template('ShowBasic.html', usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)
    except:
        return render_template('404.html')

#展示个性信息
@app.route('/showpersonalitymessage/<msgid>', methods=['POST', 'GET'])
@login_required
def showpersonalitymessage(msgid):
    try:
        motto = request.form.get('motto')
        hobby = request.form.get('hobby')
        birthplace = request.form.get('birthplace')
        liveplace = request.form.get('liveplace')
        education = request.form.get('education')
        resume = request.form.get('resume')

        usermsg = User.query.filter(User.id == msgid).first()
        if motto:
            usermsg.motto = motto
        if hobby:
            usermsg.hobby = hobby
        if birthplace:
            usermsg.birthplace = birthplace
        if liveplace:
            usermsg.liveplace = liveplace
        if education:
            usermsg.education = education
        if resume:
            usermsg.resume = resume

        db.session.add(usermsg)
        db.session.commit()
        usermsg = User.query.filter(User.id == msgid).first()

        return render_template('ShowPersonality.html', usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)
    except:
        return render_template('404.html')

#头像设置
@app.route('/headportreait/')
@login_required
def headportrait():
    try:
        return render_template('HeadPortrait.html', usermsg=g.user, picid=str(g.user.picid))
    except:
        return render_template('404.html')

#上传图片
@app.route('/uploadpic/', methods=['GET', 'POST'])
@login_required
def uploadpic():
    try:
        if request.method == 'POST':
            file = request.files['picture']
            if file:
                picway = '/home/ubuntu/HITChat/static/images/userimage/' + str(g.user.telephone) + str(g.user.picid) + '.png'
                if os.path.exists(picway):
                    os.remove(picway)
                usermsg = g.user
                usermsg.picid = usermsg.picid + 1
                db.session.add(usermsg)
                db.session.commit()
                file.save(os.path.join('/home/ubuntu/HITChat', 'static/images/userimage/' + str(g.user.telephone) + str(g.user.picid) + '.png'))
                return redirect(url_for('showbasicmessage', msgid=g.user.id))
    except:
        return render_template('404.html')

#展示用户所有文章
@app.route('/userquestion/<msgid>')
@login_required
def userquestion(msgid):
    try:
        if g.user.isAdmin == 1:
            userquestionmsg = Question.query.filter()
        else:
            userquestionmsg = Question.query.filter(Question.author_id == msgid)
        usermsg = User.query.filter(User.id == msgid).first()
        return render_template('UserQuestion.html', userquestionmsg=userquestionmsg, usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)
    except:
        return render_template('404.html')

#删除文章
@app.route('/deletequestion/<question_id>')
@login_required
def deletequestion(question_id):
    try:
        #print question_id
        question = Question.query.filter(Question.id == question_id).first()
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('userquestion',msgid=g.user.id))
    except:
        return render_template('404.html')

#展示用户所有评论
@app.route('/useranswer/<msgid>')
@login_required
def useranswer(msgid):
    try:
        if g.user.isAdmin == 1:
            useranswermsg = Answer.query.filter()
        else:
            useranswermsg = Answer.query.filter(Answer.author_id == msgid)
        usermsg = User.query.filter(User.id == msgid).first()
        return render_template('UserAnswer.html', useranswermsg=useranswermsg, usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)
    except:
        return render_template('404.html')

#删除评论
@app.route('/deleteanswer/<answer_id>')
@login_required
def deleteanswer(answer_id):
    try:
        answer = Answer.query.filter(Answer.id == answer_id).first()
        db.session.delete(answer)
        db.session.commit()
        return redirect(url_for('useranswer', msgid=g.user.id))
    except:
        return render_template('404.html')

#话题分类
@app.route('/topic/<table>')
@login_required
def topic(table):
    try:
        import time
        time1 = time.time()
        
        context = {
            'questions': Question.query.order_by(db.desc(Question.create_time)).all()
        }
        time2 = time.time()
        print time2-time1
        usermsg = User.query.filter(User.id == g.user.id).first()
        time3 = time.time()
        print time3-time2
        if (table=='All'):
            return render_template('TopicAll.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Notification'):
            return render_template('TopicNotification.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Study'):
            return render_template('TopicStudy.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='QuestionAnswer'):
            return render_template('TopicQuestionAnswer.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='SecondHand'):
            return render_template('TopicSecondHand.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='News'):
            return render_template('TopicNews.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Travel'):
            return render_template('TopicTravel.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Food'):
            return render_template('TopicFood.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Education'):
            return render_template('TopicEducation.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Sport'):
            return render_template('TopicSport.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='MakeFriends'):
            return render_template('TopicMakeFriends.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        if (table=='Others'):
            return render_template('TopicOthers.html', usermsg=usermsg, picid=str(usermsg.picid), **context)
        else:
            return render_template('404.html')
    except:
        return render_template('404.html')

@app.route('/newtopic')
@login_required
def newtopic():
    title = request.args.get('title')
    reason = request.args.get('reason')
    #print title,reason
    sendemail("我申请的话题为: "+title+" \n理由如下："+reason,str(g.user.telephone))
    return jsonify(result='')

@app.route('/newemail')
@login_required
def newemail():
    title = request.args.get('title')
    reason = request.args.get('reason')
    #print title,reason
    sendemail("主题为: "+title+" \n内容："+reason,str(g.user.telephone))
    return jsonify(result='')

def sendemail(content,usr):
    import smtplib
    from email.mime.text import MIMEText
    from email.utils import formataddr
    my_sender='1508159393@qq.com'    # 发件人邮箱账号
    my_pass = 'aonqdwwkcjaegehi'              # 发件人邮箱密码
    my_user='xing_hua_zhang@126.com'      # 收件人邮箱账号，我这边发送给自己
    try:
        msg=MIMEText(content,'plain','utf-8')
        msg['From']=formataddr(["From "+usr,my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["Admin",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="联系管理员"                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        pass

@app.route('/admintopic/',methods=['POST'])
@login_required
def admintopic():
    topic = request.form.get('label')
    question_id = request.form.get('questionid')
    print topic,question_id
    question = Question.query.filter(Question.id == question_id).first()
    question.label = topic
    db.session.add(question)
    db.session.commit() 
    return redirect(url_for('userquestion',msgid=g.user.id))
#####################################################################

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        print request.remote_addr
        return render_template('login.html')
        
    else:
        telephone = request.form.get('telephone')
        pwd = request.form.get('password')
        user_salt = User.query.filter(User.telephone == telephone).first()
        if user_salt:
            salt = user_salt.salt
            password = security.create_md5(pwd, salt)
            user = User.query.filter(User.telephone == telephone,User.password==password).first()
            if user:
                session['user_id'] = user.id
                #如果想在31天内都不需要登录
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return render_template('login_warning.html')
        else:
            return render_template('login_warning.html')

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        yzm = request.form.get('yzm')
        ip = request.remote_addr
        #进行手机号码验证是否注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return render_template('register_warning.html',flag=1)
        elif yzm != yzmdict[ip][1]:
            return render_template('register_warning.html',flag=2)
        else:
            # 随机生成4位salt
            salt = security.create_salt()
            password = security.create_md5(password1, salt)
            user = User(telephone=telephone,username=username,password=password,salt=salt)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/sendyzm')
def sendyzm():
    try:
        telephone = request.args.get('telephone')
        #yzm = request.args.get('yzm')
        print len(telephone)
        ip = request.remote_addr
        #print ip
        if ip in yzmdict.keys():
            yzmdict[ip][0] += 1
        else:
            yzmdict[ip] = []
            yzmdict[ip].insert(0,1)
        if yzmdict[ip][0] < 4 and len(telephone) == 11:
            alycode = sendmscode()
            __business_id = uuid.uuid1()
            #print __business_id
            yzcode = alycode.randomCode()
            yzmdict[ip].insert(1,yzcode)
            params = "{\"code\":"+yzcode+",\"product\":\"云通信\"}"
            print alycode.send_sms(__business_id, telephone, "HITChat项目组", "SMS_114065115",params)
        return jsonify(result='')
    except:
        return render_template('404.html')

@app.route('/sendyzmreset')
def sendyzmreset():
    try:
        telephone = request.args.get('telephone')
        #yzm = request.args.get('yzm')
        print len(telephone)
        ip = request.remote_addr
        #print ip
        if ip in yzmdict.keys():
            yzmdict[ip][0] += 1
        else:
            yzmdict[ip] = []
            yzmdict[ip].insert(0,1)
        if yzmdict[ip][0] < 4 and len(telephone) == 11:
            alycode = sendmscode()
            __business_id = uuid.uuid1()
            #print __business_id
            yzcode = alycode.randomCode()
            yzmdict[ip].insert(1,yzcode)
            params = "{\"code\":"+yzcode+",\"product\":\"云通信\"}"
            print alycode.send_sms(__business_id, telephone, "HITChat项目组", "SMS_116566672",params)
        return jsonify(result='')
    except:
        return render_template('404.html')

@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html', usermsg=g.user, picid=str(g.user.picid))
    else:
        title = request.form.get('title')
        label = request.form.get('label')
        content = request.form.get('content')
        T = title
        if T.strip() == "":
            title = label
        question = Question(title=title,label=label,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        Key10 = articleKey()
        soup = BeautifulSoup(content,'html.parser')
        key = Key10.generator(title+soup.text)
        if label == '问答' or label == u'问答':
            admin_answer(key,question.id)
        #print key,question.id
        return redirect(url_for('index'))

@app.route('/aiml_detail/')
@login_required
def aiml_detail():
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #####################################################################
        global flag
        if flag:
            os.chdir("Robot")  # 打开aiml库
            #kernel = aiml.Kernel()
            # if os.path.isfile("bot_brain.brn"):
            #     kernel.bootstrap(brainFile = "bot_brain.brn")
            # else:
            #     kernel.bootstrap(learnFiles = "std-startup.xml", commands = "HELLO AIML")
            #     kernel.saveBrain("bot_brain.brn")
            kernel.learn("StartUp.xml")
            kernel.respond("LOAD AIML B")
            flag = False
        #####################################################################
        yxaiml = YX_Aiml.query.filter(YX_Aiml.id > 0)
        return render_template('YX_aiml.html',yx_aiml=yxaiml, usermsg=g.user, picid=str(g.user.picid))
    except:
        return render_template('404.html')

@app.route('/YX_aiml/',methods=['POST'])
@login_required
def YX_aiml():
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # #####################################################################
    # os.chdir("\Robot")  # 打开aiml库
    # #kernel = aiml.Kernel()
    # # if os.path.isfile("bot_brain.brn"):
    # #     kernel.bootstrap(brainFile = "bot_brain.brn")
    # # else:
    # #     kernel.bootstrap(learnFiles = "std-startup.xml", commands = "HELLO AIML")
    # #     kernel.saveBrain("bot_brain.brn")
    # kernel.learn("StartUp.xml")
    # kernel.respond("LOAD AIML B")
    # #####################################################################
    dialog_content = request.form.get('dialog_content')
    #print dialog_content
    robot_answer = kernel.respond(dialog_content.encode('utf-8'))
    yx_aiml = YX_Aiml(content_p = dialog_content,content_r = robot_answer)
    # dialog.robot = ''
    db.session.add(yx_aiml)
    db.session.commit()
    return redirect(url_for('aiml_detail'))

@app.route('/detail/<question_id>')
@login_required
def detail(question_id):
    try:
        question_model = Question.query.filter(Question.id == question_id).first()
        answer = Answer.query.filter(Answer.question_id == question_id).first()
        allanswerpicid = {}
        for a in question_model.answers:
            allanswerpicid[a.id] = str(a.author.picid)
        return render_template('detail.html',question=question_model, answer=answer, usermsg=g.user, picid=str(g.user.picid), allanswerpicid=allanswerpicid)
    except:
        return render_template('404.html')

@app.route('/newsdetail/<news_leftid>/<news_id>')
@login_required
def newsdetail(news_leftid,news_id):
    try:
        sql = mysql()
        dataSql = sql.selectnews('sliderightdetailhtml'+str(news_leftid),news_id)
        sql.conn.close()
        return render_template('newsdetail.html',dataSql = dataSql,usermsg = g.user,picid=str(g.user.picid))
    except:
        return render_template('404.html')

@app.route('/jwcdetail/<news_id>')
@login_required
def jwcdetail(news_id):
    try:
        sql = mysql()
        datajwc = sql.selectnews('jwcarticlehtml',news_id) 
        #print datajwc
        sql.conn.close()
        return render_template('jwc.html',datajwc = datajwc,usermsg = g.user,picid=str(g.user.picid))
    except:
        return render_template('404.html')

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    try:
        content = request.form.get('answer_content')
        question_id = request.form.get('question_id')
        answer = Answer(content=content)
        answer.author = g.user
        question = Question.query.filter(Question.id == question_id).first()
        answer.question = question
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail',question_id=question_id))
    except:
        return render_template('404.html')

def admin_answer(key,question_id):
    sql = mysql()
    datakey = sql.select('keyword')
    length = len(datakey)
    all = 0
    for i in range(length):
        if all > 10:
            break
        num = 0
        for j in range(5):
            if datakey[i][j+3] in key:
                num += 1
        if num > 2:
            all += 1
            #content = datakey[i][1]+": "+datakey[i][2]
            content = '<span>'+datakey[i][1]+'<a href="'+ datakey[i][2]+'" target="_blank">点击查看</a></span>'
            answer = Answer(content=content)
            user = User.query.filter(User.isAdmin == 1).first()
            print user
            if user:
                answer.author = user
            question = Question.query.filter(Question.id == question_id).first()
            answer.question = question
            db.session.add(answer)
            db.session.commit()

@app.route('/add_answer2/',methods=['POST'])
@login_required
def add_answer2():
    try:
        content = request.form.get('answer2')
        answer_id = request.form.get('answer_id')
        question_id = request.form.get('question_id')
        #print content,answer_id
        answer2 = Answer2(content=content)
        answer2.author = g.user
        answer = Answer.query.filter(Answer.id == answer_id).first()
        answer2.answer = answer
        db.session.add(answer2)
        db.session.commit()
        return redirect(url_for('detail',question_id=question_id))
    except:
        return render_template('404.html')

@app.route('/add_zan/',methods=['POST'])
@login_required
def add_zan():
    question_id = request.form.get('question_id')
    zan = request.form.get('zannum')
    question = Question.query.filter(Question.id == question_id).first()
    question.zan = zan
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
@login_required
def search():
    try:
        q = request.args.get('q')
        questions=Question.query.filter(or_(Question.title.contains(q),
                                  Question.content.contains(q))).order_by(db.desc(Question.create_time))
        label1 = q
        picids = {}
        for q in questions:
            picids[q.id] = str(q.author.picid)
        return render_template('search.html',questions=questions,usermsg=g.user,picids=picids,picid=str(g.user.picid))
    except:
        return render_template('404.html')

@app.route('/searchlabel/<name>')
@login_required
def searchlabel(name):
    try:
        q = name.decode('utf8')
        #print q
        questions=Question.query.filter(or_(Question.title.contains(q),
                                  Question.content.contains(q))).order_by(db.desc(Question.create_time))
        label1 = q
        picids = {}
        for q in questions:
            picids[q.id] = str(q.author.picid)
        return render_template('search.html',questions=questions,usermsg=g.user,picids=picids,picid=str(g.user.picid))
    except:
        return render_template('404.html')

def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript">
    window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
    </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response

#信息与反馈
@app.route('/informationandfeedback/<table>')
@login_required
def informationandfeedback(table):
    usermsg = User.query.filter(User.id == g.user.id ).first()
    if (table=='AboutUs'):
        return render_template('FooterAboutUs.html', usermsg=usermsg, picid=str(usermsg.picid))
    elif (table=='Contact'):
        return render_template('FooterContact.html', usermsg=usermsg, picid=str(usermsg.picid))
    elif (table=='Suggestion'):
        return render_template('FooterSuggestion.html', usermsg=usermsg, picid=str(usermsg.picid))
    elif (table=='Donate'):
        return render_template('FooterDonate.html', usermsg=usermsg, picid=str(usermsg.picid))
    elif (table=='Statement'):
        return render_template('FooterStatement.html', usermsg=usermsg, picid=str(usermsg.picid))
    else:
        return render_template('404.html')

#网站介绍
@app.route('/intrpduction/')
@login_required
def introduction():
    usermsg = User.query.filter(User.id == g.user.id ).first()
    return render_template('Introduction.html', usermsg=usermsg, picid=str(usermsg.picid))

@app.before_request
def my_before_request():
    try:
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            if user:
                g.user = user
    except:
        pass

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

yzmdict = {}
if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
    #from gevent.wsgi import WSGIServer
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
