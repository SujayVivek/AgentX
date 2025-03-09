import click
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import SQLALCHEMY_DATABASE_URL

@click.group()
def cli():
    pass

@cli.command()
def create_db():
    """Create the database"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        click.echo(f"Created database: {engine.url}")
    else:
        click.echo(f"Database already exists: {engine.url}")

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to drop the database?')
def drop_db():
    """Drop the database"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if database_exists(engine.url):
        drop_database(engine.url)
        click.echo(f"Dropped database: {engine.url}")
    else:
        click.echo(f"Database does not exist: {engine.url}")

if __name__ == '__main__':
    cli() 