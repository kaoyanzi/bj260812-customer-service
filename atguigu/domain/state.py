import uuid
from dataclasses import dataclass, field
from typing import List, Any

from atguigu.domain.messages import UserMessage, BotMessage


@dataclass
class Turn:
    """代表一轮对话"""
    turn_id: str#每次对话轮次id
    user_message:UserMessage
    bot_message:list[BotMessage]=field(default_factory=list)#客服的回复

@dataclass
class Session:
    """代表用户的会话 间隔时间的阈值为1小时"""
    session_id: str
    started_at: float#会话创建时间
    last_activity_at: float#活跃时间
    closed_at: float | None = None
    turns: List[Turn] = field(default_factory=list)

@dataclass
class FocusObject:
    """焦点对象"""
    type:str#卡片的类型
    id:str
    title:str|None = None
    attributes:dict[str,Any] = field(default_factory=dict)

@dataclass
class SharedState:
    focus_object:FocusObject | None = None
    sessions:List[Session] = field(default_factory=list)

@dataclass
class TaskInstance:
    """基于yaml流程产生的任务实例"""
    flow_id: str
    step_id: str
    slots: dict[str,Any] = field(default_factory=dict)
    task_id: str= field(default_factory=lambda :str(uuid.uuid4()))

@dataclass
class TaskState:
    """任务的状态"""
    active_task: TaskInstance|None = None
    paused: list[TaskInstance] = field(default_factory=list)


@dataclass
class DialogueState:
    """对话的状态:某个用户所有跟对话有关的信息,将DialogueState跟dialogue_states表中的state_json去对应"""
    # 第一类:任务的状态: 只有任务流程轨道处理所需要的信息  包含:当前正在处理的任务实例;暂停任务实例列表
    # 第二类:三种轨道共享状态: 任务处理,知识检索,闲聊共享
    sender_id: str
    shared_state: SharedState = field(default_factory=SharedState)
    task_state: TaskState = field(default_factory=TaskState)