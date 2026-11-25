import asyncio

from sqlalchemy import text, Result
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from atguigu.conf.config import settings

#声明模块级变量 初始值为None
engine:AsyncEngine|None = None
session_factory:async_sessionmaker[AsyncSession]|None = None


def init_db_engine():
    """对引擎对象和会话工厂进行赋值:项目启动初始化一次即可"""
    global engine,session_factory
    engine = create_async_engine(url=settings.database_url, echo=True)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

async def close_db_engine():
    """关闭数据库引擎,释放资源:项目关闭时调用"""
    if engine:
        await engine.dispose()


if __name__ == '__main__':
    init_db_engine()

    async def test_session():
        async with session_factory() as session:
            result:Result = await session.execute(text("select 1"))
            print(result.scalar())
        await close_db_engine()
    asyncio.run(test_session())