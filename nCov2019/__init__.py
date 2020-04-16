# -*- coding: utf-8 -*-
import os
import click

from flask import Flask, render_template

from nCov2019.settings import config
from nCov2019.extensions import db, csrf
from nCov2019.models import Bless, EverydayData
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
    register_errors(app)

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
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors.html', code=400, info='Bad Request'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors.html', code=403, info='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('errors.html', code=405, info='Method Not Allowed'), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors.html', code=500, info='Server Error'), 500


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Bless=Bless, Data=EverydayData)



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














