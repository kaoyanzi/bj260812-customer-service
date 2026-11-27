from dataclasses import dataclass, field
from enum import Enum


class ResponseMode(Enum):
    STATIC = "static"#渲染后直接返回
    REPHRASE = "rephrase"#渲染后调用大模型润色后返回

@dataclass
class ResponseTemplate:
    """获取客服回复文本"""
    mode:ResponseMode = ResponseMode.STATIC
    text:str | None = ""#等待渲染的文本
    prompt:str | None = ""#需要调大模型参考的提示词

@dataclass
class SlotValidation:
    """用于收集槽位节点校验搜集到的槽位信息"""
    condition: str | None = None#用于校验的表达式
    failure_template: ResponseTemplate|None = None#校验失败后响应的文本

@dataclass
class FlowStepLink:
    """节点跳转next连接线对象"""
    target: str = ""

@dataclass
class StaticLink(FlowStepLink):
    """固定跳转的连接线 例如: next: ask_order_number"""
    pass

@dataclass
class ConditionalLink(FlowStepLink):
    """带条件的连接线
        next:
          - if: "slots.get('product_id')"if的值是跳转的条件
            then: respond 后续跳转的id
    """
    condition: str = ""

@dataclass
class FallbackLink(FlowStepLink):
    """最后兜底跳转的连接线
        next:
          - if: "slots.get('product_id')"
            then: respond
          - else: missing_product_context 兜底跳转
    """
    pass

class FlowStepType(Enum):
    """步骤/节点的枚举"""
    START = "start"
    ACTION = "action"
    RESPONSE = "response"
    COLLECT = "collect"
    END = "end"

@dataclass
class FlowStep:
    """流程内固定的步骤父类,包含五种步骤类型公共的属性"""
    id: str
    type: FlowStepType
    next: list[FlowStepLink] = field(default_factory=list)#连接线 决定下一个步骤

@dataclass
class StartFlowStep(FlowStep):
    """开始的步骤/节点"""
    pass


@dataclass
class ActionFlowStep(FlowStep):
    """执行电商后端接口的调用"""
    action: str = ""


@dataclass
class CollectFlowStep(FlowStep):
    slot_name: str = ""
    template: ResponseTemplate = field(default_factory=ResponseTemplate)#要求用户提供信息的文本
    validation: SlotValidation | None = None#收集到的槽位是否校验可选

@dataclass
class RespondFlowStep(FlowStep):
    template: ResponseTemplate = field(default_factory=ResponseTemplate)

@dataclass
class EndFlowStep(FlowStep):
    """结束的步骤"""
    pass

@dataclass
class FlowSlot:
    """槽位信息"""
    name: str = ""
    type: str = "any"
    label: str = ""
    description: str = ""

@dataclass
class Flow:
    """流程定义"""
    id : str
    description : str = ""
    steps: list[FlowStep] = field(default_factory=list)
    slots: list[FlowSlot] = field(default_factory=list)
    name: str | None = None

@dataclass
class FlowCatalog:
    """流程定义清单"""
    flows: dict[str, Flow] = field(default_factory=dict)
    slots: dict[str, FlowSlot] = field(default_factory=dict)
