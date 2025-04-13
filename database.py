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
    str1 = Column(String)
    str2 = Column(String)
    str3 = Column(String)
    str4 = Column(String)
    str5 = Column(String)
    int1 = Column(Integer, default=0)
    int2 = Column(Integer, default=0)
    int3 = Column(Integer, default=0)
    int4 = Column(Integer, default=0)
    int5 = Column(Integer, default=0)
    int6 = Column(Integer, default=0)
    int7 = Column(Integer, default=0)
    int8 = Column(Integer, default=0)
    int9 = Column(Integer, default=0)
    int10 = Column(Integer, default=0)
    bool1 = Column(Boolean, default=False)
    bool2 = Column(Boolean, default=False)
    bool3 = Column(Boolean, default=False)
    bool4 = Column(Boolean, default=False)
    bool5 = Column(Boolean, default=False)
    bool6 = Column(Boolean, default=False)
    bool7 = Column(Boolean, default=False)
    bool8 = Column(Boolean, default=False)
    bool9 = Column(Boolean, default=False)
    bool10 = Column(Boolean, default=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Sqltest1(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Sqltest1(bot))
