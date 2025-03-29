from discord.ext import commands
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///cmdlab_users.db'  # データベースの種類と名前をここで指定できます
engine = create_engine(DATABASE_URL)  # データベースエンジンを作成
Base = declarative_base()            # データベースの親クラスを作成


class User(Base):
    __tablename__ = 'users'
    no = Column(Integer, primary_key=True)
    userid = Column(Integer)
    username = Column(String)
    allexp = Column(Integer, default=0)
    alladdexp = Column(Integer, default=0)
    allremoveexp = Column(Integer, default=0)
    chatcount = Column(Integer, default=0)
    level = Column(Integer, default=0)
    exp = Column(Integer, default=0)
    noxp = Column(Boolean, default=0)
    selfintro = Column(Boolean, default=False)
    question = Column(Boolean, default=False)
    freechat = Column(Boolean, default=False)
    anotherch = Column(Boolean, default=False)
    dailygivexp = Column(Boolean, default=False)
    dailylogin = Column(Boolean, default=False)
    dailylogincount = Column(Integer, default=0)
    mee6level = Column(Integer, default=0)
    warnpt = Column(Integer, default=0)
    warnreason1 = Column(String)
    warnreason2 = Column(String)
    warnreason3 = Column(String)
    warnreason4 = Column(String)
    warnreason5 = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Sqltest1(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Sqltest1(bot))
