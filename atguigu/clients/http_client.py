import asyncio

from httpx import AsyncClient

#声明全局变量 类型:AsyncClient
http_client:AsyncClient|None = None

def init_http_client():
    """对http的客户端赋值 项目启动初始化客户端"""
    global http_client
    http_client = AsyncClient()

async def close_http_client():
    if http_client:
        await http_client.aclose()

if __name__ == '__main__':
    init_http_client()

    async def test():
        response = await http_client.get("http://127.0.0.1:18081/users/u1001/orders")
        print(response.json().get("data").get("orders"))


    asyncio.run(test())