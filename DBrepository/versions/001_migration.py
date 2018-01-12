from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('post', VARCHAR(length=140)),
    Column('timeStamp', DATETIME),
    Column('user_id', INTEGER),
)

logs_inf = Table('logs_inf', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('logTime', DateTime),
    Column('logType', Integer),
    Column('logMsg', String(length=64)),
    Column('retStatus', Boolean, default=ColumnDefault(False)),
    Column('logStatus', Boolean, default=ColumnDefault(False)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].drop()
    post_meta.tables['logs_inf'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].create()
    post_meta.tables['logs_inf'].drop()
