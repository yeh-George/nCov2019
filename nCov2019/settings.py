# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # bless分页
    NCOV2019_BLESS_PER_PAGE = 7


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('sqlite:///' + os.path.join(basedir, 'data-dev.db'))


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}