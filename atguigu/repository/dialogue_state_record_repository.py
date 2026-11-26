import asyncio
from dataclasses import dataclass

from pydantic import TypeAdapter
from sqlalchemy.dialects.mysql import insert, Insert
from sqlalchemy.ext.asyncio import AsyncSession

from atguigu.clients import database
from atguigu.clients.database import init_db_engine
from atguigu.domain.state import DialogueState, SharedState, FocusObject
from atguigu.models.dialogue_state_record import DialogueStateRecord

#DialogueState转换适配器
DIALOGUE_STATE_ADAPTER = TypeAdapter(DialogueState)

class DialogueStateRecordRepository:
    """持久层操作dialogue_states表"""

    def __init__(self,session:AsyncSession):
        self.session = session


    async def load_state(self, sender_id)->DialogueState:
        """
        根据用户的id查询mysql数据库用户的对话状态
        :param sender_id:
        :return: 对话状态
        """
        record:DialogueStateRecord | None = await self.session.get(DialogueStateRecord,sender_id)
        if record is None:
            #该客户是第一次跟客服对话 将用户id封装到DialogueState对象返回即可
            return DialogueState(sender_id=sender_id)
        else:
            #从数据库ORM模型获取state_json字符串 并且转为DialogueState
            return DIALOGUE_STATE_ADAPTER.validate_json(record.state_json)

    async def save_state(self, state:DialogueState):
        """
        保存或者更新对话状态
        :param state:
        :return:
        """
        #将对话状态先序列化为json字符串
        state_json = DIALOGUE_STATE_ADAPTER.dump_json(state).decode("utf-8")
        #创建insert对象
        insert_stmt:Insert = insert(DialogueStateRecord).values(sender_id=state.sender_id,state_json=state_json)
        #调用insert对象on_duplicate_key_update方法指定更新的字段state_json的值
        #insert_stmt.on_duplicate_key_update(state_json=state_json)
        update_stmt = insert_stmt.on_duplicate_key_update(state_json = insert_stmt.inserted.state_json)
        await self.session.execute(update_stmt)
        #提交事务
        await self.session.commit()


if __name__ == '__main__':

    init_db_engine()
    async def test_repository():
        async with database.session_factory() as session:
            repository = DialogueStateRecordRepository(session)
            # state = DialogueState(
            #     sender_id="test1",
            #     shared_state=SharedState(
            #         focus_object=FocusObject(
            #             type="order",
            #             id="A1001",
            #             title="订单笔记本电脑5000元",
            #             attributes={"status":"发货完成"}
            #         )
            #     )
            # )
            # await repository.save_state(state)
            state = await repository.load_state(sender_id="test1")
            print(state)
        await database.close_db_engine()
    asyncio.run(test_repository())



    def test():
        @dataclass
        class UserInfo:
            id: int
            name: str
            age: int
        adapter = TypeAdapter(UserInfo)

        #序列化 将对象转为json字符串     和      反序列化 将json字符串转成对象
        user = UserInfo(1,"jack",15)
        user_str = adapter.dump_json(user).decode("utf-8")

        user1 = adapter.validate_json(user_str)
        print(user1)