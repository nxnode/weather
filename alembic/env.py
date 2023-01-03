"""
Configure how alembic runs migrations.
"""
from logging.config import fileConfig

from sqlalchemy.exc import InterfaceError, OperationalError

from alembic import context
from src.database.models import *
from src.database.session import get_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# This line sets up loggers
fileConfig(config.config_file_name)

# add your base model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def exclude_from_config(config_, object_type):
    """Exlcude tables from autogeneration"""
    objects_ = config_.get(object_type, None)
    if objects_ is not None:
        return objects_.split(",")
    return None


exclude_tables = exclude_from_config(config.get_section("alembic:exclude"), "tables")
exclude_schemas = exclude_from_config(config.get_section("alembic:exclude"), "schemas")


def include_object(object, name, type_, reflected, compare_to):
    """Specify what to include in autogeneration"""
    if type_ == "table" and (
        name in exclude_tables or object.schema in exclude_schemas
    ):
        return False
    return True


def run_migrations():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
