# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: manage.py
@time: 2017/8/14 21:40
@desc:
'''
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from hitqa import app
from exts import db
from models import User,Question

manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app,db)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()