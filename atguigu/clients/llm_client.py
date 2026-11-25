from langchain.chat_models import init_chat_model

from atguigu.conf.config import settings

llm = init_chat_model(
    model_provider="openai",
    model=settings.llm_model,
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
    temperature=0.4
)

if __name__ == '__main__':
    print(llm.invoke("简单介绍一下自己").content)