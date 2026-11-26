"""该模块定义对话Service需要的数据类,采用dataclass定义"""
from dataclasses import dataclass, field
from enum import Enum


@dataclass
class MessageObject:
    """业务层卡片对象"""
    type: str#order订单 product商品
    id: str #订单编号或者商品id
    title: str|None = None  #订单标题或者商品标题
    attributes:dict = field(default_factory=dict)#每次产生MessageObject实例的时候,该实例中的attributes会自动调用dict()的构造产生空字典

class MessageType(Enum):
    TEXT = "text"
    OBJECT = "object"

@dataclass
class UserMessage:
    """用于业务层业务处理"""
    sender_id: str
    message_id: str
    type:MessageType    #消息类型  或者文本或者对象
    text: str|None = None
    object: MessageObject|None = None

@dataclass
class BotMessage:
    """客服回复消息"""
    text: str|None = None
    object: MessageObject|None = None

@dataclass
class ProcessResult:
    """引擎调用本轮回复的结果"""
    sender_id: str
    message_id: str
    messages:list[BotMessage]

