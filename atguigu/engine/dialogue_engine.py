from atguigu.domain.messages import UserMessage, ProcessResult
from atguigu.domain.state import DialogueState


class DialogueEngine:

    def __init__(self):
        pass

    async def process_message(self, state:DialogueState, user_message:UserMessage)->ProcessResult:

        pass