from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    # 获取项目根目录
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # 明确指定模板和静态文件夹路径
    template_dir = os.path.join(base_dir, 'app', 'templates')
    static_dir = os.path.join(base_dir, 'app', 'static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes
    app.register_blueprint(routes.bp)

    return app