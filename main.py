#1.生命fastapi的生命周期
import uvicorn
from fastapi import FastAPI

from atguigu.conf.config import settings
from atguigu.web.chat_router import chat_router

#2.创建fastapi示例

app = FastAPI()
#3.引入路由
app.include_router(chat_router)

def main():
    uvicorn.run("main:app", host="127.0.0.1", port=settings.app_port,reload=True)

if __name__ == "__main__":
    main()
