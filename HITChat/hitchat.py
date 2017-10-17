# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,redirect,url_for,session,g,send_from_directory,make_response
from werkzeug import secure_filename
import config
from models import User,Question,Answer,YX_Aiml
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
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
global kernel
kernel = aiml.Kernel()
flag = True
#############################################################################
ALLOWED_EXTENSIONS = set(['xml','html','aiml','png'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/uploadfiles/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.chdir('/PythonProgramming/hitproject/hitqa/hitqa/Robot')
            #print os.getcwd()
            file.save(os.path.join(os.getcwd(),'upload_'+filename))
            kernel.learn('upload_'+filename)
            file_url = url_for('uploaded_file', filename=filename)
            return redirect(url_for('aiml_detail'))
#############################################################################
@app.route('/test/')
@login_required
def test():
    return render_template('test.html')

@app.route('/')
@login_required
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

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
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
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
        question = Question(title=title,content=content)
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
        os.chdir("\Robot")  # 打开aiml库
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
    return render_template('YX_aiml.html',yx_aiml=yxaiml)

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
    return render_template('detail.html',question=question_model,answer=answer)

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

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),
                              Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html',questions=questions)

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
    app.run()
