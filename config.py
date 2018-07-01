class Base(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///price-tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Development(Base):
    DEBUG = True


class Production(Base):
    DEBUG = False
