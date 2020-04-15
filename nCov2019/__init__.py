# -*- coding: utf-8 -*-
import os
import click

from flask import Flask

from nCov2019.settings import config
from nCov2019.extensions import db, csrf
from nCov2019.models import Bless
from nCov2019.blueprints.home import home_bp
from nCov2019.blueprints.bless import bless_bp
from nCov2019.fakes import fake_bless

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('nCov2019')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(bless_bp)


def register_template_context(app):
    pass


def register_errors(app):
    pass


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Bless=Bless)



def register_commands(app):
    @app.cli.command()
    def init_db():
        db.drop_all()
        db.create_all()
        click.echo('Database initialized.')

    @app.cli.command()
    def forge():
        fake_bless()
        click.echo('Bless added.')














