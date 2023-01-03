"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op, context
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    schema_upgrades()
    data_upgrades()

def downgrade():
    data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here"""
    ${upgrades if upgrades else "pass"}

def schema_downgrades():
    """schema downgrade migrations go here"""
    ${downgrades if downgrades else "pass"}

def data_upgrades():
    """optional data upgrade migrations go here"""
    pass

def data_downgrades():
    """optional data downgrade migrations go here"""
    pass
