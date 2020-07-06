from core.database import Base
import sqlalchemy as sa


class Addons(Base):
    __tablename__ = 'addons'
    id = sa.Column(sa.Integer, comment='id', primary_key=True)
    name = sa.Column(sa.String(255), comment='名称', unique=True, nullable=False)
