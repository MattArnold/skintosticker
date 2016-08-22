import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SKINS_FOLDER = os.path.join(basedir, 'app/static/skins/')
STICKERS_FOLDER = os.path.join(basedir, 'app/static/stickers/')
CHARACTERS_FOLDER = os.path.join(basedir, 'app/static/characters/')
LABELS_FOLDER = os.path.join(basedir, 'app/static/labels/')
