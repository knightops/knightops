#!/usr/bin/env python3
import importlib
import os
from pathlib import Path

import alembic
import click
import sqlalchemy
import uvicorn

from core.config import settings
from core.database import Base

MODELS_DIRECTORY = os.path.join('app', 'models')
EXCLUDE_FILES = ["__init__.py"]


def import_models():
    for dir_path, dir_names, file_names in os.walk(MODELS_DIRECTORY):
        for file_name in file_names:
            if file_name.endswith("py") and file_name not in EXCLUDE_FILES:
                file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
                module_name = file_path_wo_ext.replace(os.sep, ".")
                importlib.import_module(module_name)

@click.group()
def cli():
    pass


def alembic_config():
    """ Generate a Config instance from alembic.ini """
    from alembic.config import Config
    path = Path(__file__).parent.resolve().joinpath('migrations/alembic.ini')
    # path = os.path.join(os.path.dirname(settings.__file__), 'alembic.ini')
    config = Config(path)
    print(settings.SQLALCHEMY_DATABASE_URI)
    config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DATABASE_URI)
    config.set_main_option("script_location", "migrations")
    return config


@cli.command()
def initdb():
    cfg = alembic_config()

    sqlalchemy_url = cfg.get_main_option('sqlalchemy.url')
    engine = sqlalchemy.create_engine(sqlalchemy_url)
    Base.metadata.create_all(engine)

    alembic.command.stamp(cfg, "head")


@cli.command()
def migrate():
    # from app.models.addons import Addons
    cfg = alembic_config()
    import_models()
    alembic.command.revision(cfg, autogenerate=True,)


@cli.command()
def upgrade():
    # from app.models.addons import Addons
    cfg = alembic_config()
    import_models()
    alembic.command.upgrade(cfg, "head")


@cli.command("runserver", short_help="Run a development server.")
@click.option("--host", "-h", default="0.0.0.0", help="The interface to bind to.")
@click.option("--port", "-p", default=8089, help="The port to bind to.")
@click.option(
    "--reload/--no-reload",
    default=True,
    help="Enable or disable the reloader. By default the reloader "
    "is active if debug is enabled.",
)
def runserver(host, port, reload):
    uvicorn.run(app="server:app", host=host, port=port, log_level='info', reload=reload, workers=2)


if __name__ == '__main__':
    cli()
