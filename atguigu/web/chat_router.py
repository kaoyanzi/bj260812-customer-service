import uuid

from fastapi import APIRouter
from loguru import logger

from atguigu.web.schemas import ChatRequest, ChatResponse, ChatBotMessage, HistoryResponse, HistoryMessage

chat_router = APIRouter(tags=["智能客服"])

@chat_router.post("/api/chat")
async def chat(chat_request: ChatRequest):
    logger.info(chat_request)
    #TODO 暂时固定响应客服回复,后续改为调业务层
    return ChatResponse(
        sender_id=chat_request.sender_id,
        message_id=str(uuid.uuid4()),
        messages=[
            ChatBotMessage(
                text="客服固定回复"
            )
        ]
    )

@chat_router.get("/api/chat/history")
async def chat_history(sender_id:str)->HistoryResponse:
    #TODO 后续改为调用业务层从数据库获取对话状态,进一步获取历史
    #1.将接口模型ChatRequest转化为UserMessage

    #2.调用业务层处理消息的方法,将UserMessage作为入参 得到ProcessResult

    #3.将业务层ProcessResult转为ChatResponse
    logger.info(sender_id)
    return HistoryResponse(
        sender_id=sender_id,
        messages=[
            HistoryMessage(
                role="user",
                text="你好"
            ),
            HistoryMessage(
                role="bot",
                text="你好用户,我是你的智能客服,有物流订单商品相关的问题都可以问我"
            )
        ]
    )