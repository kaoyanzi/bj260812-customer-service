"""定义路由层的入参跟出参"""
from pydantic import BaseModel

class ChatObject(BaseModel):
    type: str   #卡片的类型order,product
    id:str  #卡片中订单的编号或者是商品id
    title: str|None = None #标题
    attributes:dict =  {}  #可变类型 V1版本存在多个实例ii公用同一个字典 V2底层优化问题解决

class ChatRequest(BaseModel):
    """聊天请求的入参"""
    sender_id:str   #用户id 必填
    message_id: str|None = None
    text: str|None = None
    object:ChatObject|None = None


class ChatBotMessage(BaseModel):
    """客服单条回复消息可以是文本可以是对象"""
    text: str|None = None
    object:ChatObject|None = None

class ChatResponse(BaseModel):
    """ai客服的响应可以包含多条回复"""
    sender_id:str
    message_id: str
    messages:list[ChatBotMessage]

class HistoryMessage(BaseModel):
    """用户或者客服的单条历史消息"""
    role:str    #user用户 bot客服
    text: str|None = None
    object:ChatObject|None = None

class HistoryResponse(BaseModel):
    """历史消息的响应对象"""
    sender_id:str
    messages:list[HistoryMessage]

