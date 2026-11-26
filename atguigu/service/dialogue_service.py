from atguigu.domain.messages import UserMessage, ProcessResult
from atguigu.domain.state import DialogueState
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_state_record_repository import DialogueStateRecordRepository


class DialogueService:
    """业务层的职责:1.加载对话状态  2.调用对话引擎(修改对话状态)  3.更新保存对话的状态  4.响应本轮的回复"""

    def __init__(self,dialogue_state_record_repository:DialogueStateRecordRepository,dialogue_engine:DialogueEngine):
        self.dialogue_state_record_repository = dialogue_state_record_repository
        self.dialogue_engine = dialogue_engine




    async def process_message(self,user_message:UserMessage)->ProcessResult:
        """
        业务层处理本轮消息
        :param user_message: 业务模型   参考接口模型ChatRequest来写
        :return: 处理结果对象     参考接口模型ChatResponse来写
        """
        # TODO
        #1.根据用户id调用持久层加载用户的对话状态
        state:DialogueState = await self.dialogue_state_record_repository.load_state(user_message)

        #2.调用对话引擎(修改对话状态)得到本轮次的客服回复
        process_result:ProcessResult = await self.dialogue_engine.process_result(state,user_message)

        #3,保存/更新对话状态
        await self.dialogue_state_record_repository.save_state(state)

        #4.响应本次回复
        return process_result


