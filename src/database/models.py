import datetime
from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather"

    id = sa.Column(sa.Integer, primary_key=True)
    location = sa.Column(sa.String, index=True)
    data = sa.Column(JSONB)
