from pathlib import Path

from jinja2 import Template


def load_prompt(name:str)->str:
    prompt_path = Path(__file__).parent/'jinja2'/f'{name}.jinja2'
    return prompt_path.read_text(encoding='utf-8')


if __name__=='__main__':
    prompt_text = load_prompt('chitchat_respond')
    #创建模板对象 传入待渲染的文本
    rendered_text = Template(prompt_text).render({"history":"USER: 你好" "BOT: 你好我是你的AI客服助手",
                                                  "user_message":"我要退单"
                                                  })
    print(rendered_text)