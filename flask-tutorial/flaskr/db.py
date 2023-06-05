import sqlite3 #数据库 结构化查询语言mySQL Postgre 独立数据库 oracle数据公司 mongodb非结构化语言 SQLite可直接调用

import click
from flask import current_app, g
from flask.cli import with_appcontext

# db模块


def get_db():
    if 'db' not in g: # g全局变量
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )  # 创建文件，sqlite格式，connect连接到数据库
        g.db.row_factory = sqlite3.Row  #g.db 丢进

    return g.db


def close_db(e=None):
    db = g.pop('db', None)  #pop堆栈，弹底部

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# 1.功能 2.解释

@click.command('init-db') # 绑定命令
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)