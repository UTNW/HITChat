# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,session,g,send_from_directory,make_response
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
from mysqlconnector import mysql
sql = mysql()  # 连接爬虫数据库，并初始化游标
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
global kernel
kernel = aiml.Kernel()
flag = True

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/contactAdmin/')
def contactAdmin():
    return render_template('contactadmin.html')

@app.route('/news/')
@login_required
def news():
    dataSql = sql.select('slideRight1')
    return render_template('news.html',dataSql=dataSql,usermsg=g.user, picid=str(g.user.picid))

@app.route('/')
@login_required
def index():
    context = {
        'questions': Question.query.order_by(db.desc(Question.create_time)).all()
    }
    allq = Question.query.order_by(db.desc(Question.create_time)).all()
    picids = {}
    for q in allq:
        picids[q.id] = str(q.author.picid)
    return render_template('index.html', usermsg=g.user, picid=str(g.user.picid), picids=picids, **context)

@app.route('/classify')
@login_required
def classify():
    context = {
        'questions': Question.query.order_by(db.desc(Question.create_time)).all()
    }
    return render_template('classify.html',**context)
###################################################################
#修改基本信息
@app.route('/basicmessage/')
def basicmessage():
    return render_template('BasicMessage.html', usermsg=g.user, picid=str(g.user.picid))

#修改个性信息
@app.route('/personalitymessage/')
def personalitymessage():
    return render_template('PersonalityMessage.html', usermsg=g.user, picid=str(g.user.picid))

#展示基本信息
@app.route('/showbasicmessage/<msgid>', methods=['POST', 'GET'])
def showbasicmessage(msgid):
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

#展示个性信息
@app.route('/showpersonalitymessage/<msgid>', methods=['POST', 'GET'])
def showpersonalitymessage(msgid):
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

#头像设置
@app.route('/headportreait/')
def headportrait():
    return render_template('HeadPortrait.html', usermsg=g.user, picid=str(g.user.picid))

#上传图片
@app.route('/uploadpic/', methods=['GET', 'POST'])
def uploadpic():
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

#展示用户所有文章
@app.route('/userquestion/<msgid>')
def userquestion(msgid):
    if g.user.isAdmin == 1:
        userquestionmsg = Question.query.filter()
    else:
        userquestionmsg = Question.query.filter(Question.author_id == msgid)
    usermsg = User.query.filter(User.id == msgid).first()
    return render_template('UserQuestion.html', userquestionmsg=userquestionmsg, usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)

#删除文章
@app.route('/deletequestion/<question_id>')
def deletequestion(question_id):
    print question_id
    question = Question.query.filter(Question.id == question_id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('userquestion',msgid=g.user.id))

#展示用户所有评论
@app.route('/useranswer/<msgid>')
def useranswer(msgid):
    if g.user.isAdmin == 1:
        useranswermsg = Answer.query.filter()
    else:
        useranswermsg = Answer.query.filter(Answer.author_id == msgid)
    usermsg = User.query.filter(User.id == msgid).first()
    return render_template('UserAnswer.html', useranswermsg=useranswermsg, usermsg=usermsg, picid=str(usermsg.picid), currentid=g.user.id)

#删除评论
@app.route('/deleteanswer/<answer_id>')
def deleteanswer(answer_id):
    answer = Answer.query.filter(Answer.id == answer_id).first()
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('useranswer', msgid=g.user.id))
#####################################################################

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
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

        #进行手机号码验证是否注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return render_template('register_warning.html')
        else:
            # 随机生成4位salt
            salt = security.create_salt()
            password = security.create_md5(password1, salt)
            user = User(telephone=telephone,username=username,password=password,salt=salt)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

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
        # for i in content:
        #     print i
        # Listcontent = list(content)
        # content = ""
        # for i in range(len(Listcontent)):
        #      if(Listcontent[i] == '\n'):
        #          content += "<br/>"
        #          print "hhh"
        #      else:
        #          content += Listcontent[i]
        # print title,content
        question = Question(title=title,label=label,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/aiml_detail/')
@login_required
def aiml_detail():
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

@app.route('/YX_aiml/',methods=['POST'])
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
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    answer = Answer.query.filter(Answer.question_id == question_id).first()
    allanswerpicid = {}
    for a in question_model.answers:
        allanswerpicid[a.id] = str(a.author.picid)
    return render_template('detail.html',question=question_model, answer=answer, usermsg=g.user, picid=str(g.user.picid), allanswerpicid=allanswerpicid)

@app.route('/newsdetail/<news_leftid>/<news_id>')
def newsdetail(news_leftid,news_id):
    dataSql = sql.selectnews('slideRightDetail'+str(news_leftid),news_id)
    return render_template('newsdetail.html',dataSql = dataSql,usermsg = g.user,picid=str(g.user.picid))

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/add_answer2/',methods=['POST'])
@login_required
def add_answer2():
    content = request.form.get('answer2')
    answer_id = request.form.get('answer_id')
    question_id = request.form.get('question_id')
    print content,answer_id
    answer2 = Answer2(content=content)
    answer2.author = g.user
    answer = Answer.query.filter(Answer.id == answer_id).first()
    answer2.answer = answer
    db.session.add(answer2)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

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
    q = request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),
                              Question.content.contains(q))).order_by(db.desc(Question.create_time))
    picids = {}
    for q in questions:
        picids[q.id] = str(q.author.picid)
    return render_template('index.html',questions=questions,usermsg=g.user,picids=picids,picid=str(g.user.picid))

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

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)
