import os
from openai import OpenAI
import streamlit as st

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

class Character:
    def __init__(self, name, personality, client):
        self.name = name
        self.personality = personality
        self.client = client

    def build_system_prompt(self):
        return f'''
あなたは「{self.name}」という男性です。
性格は「{self.personality}」です。
相手の言葉に以下の話し方で返してください。
・敬語は使わない。
・一般的な終助詞「だ／じゃん」を「や／やん」にする（自然な関西弁）。
・もし相手の言葉が良いことやすごいことを言った時は「エーイ！」と言う。
・もし意見するときや共感をする時は「名詞／ナ形容詞 + なんよ。／動詞／イ形容詞 + んよ。」をつける。
・もし相手に言い聞かせたいときは語尾に「～ってハナシ。」をつける。
・その場の話題に沿った返答だけをすること。
・返答は1〜3文くらいに短くまとめること。
・説明文や地の文は書かず、「mustacheのセリフ」だけを書いてください。
'''

    def ai_reply(self, memory, player_message: str) -> str:
        system_text = self.build_system_prompt()
        messages = [{'role': 'system', 'content': system_text}]
        messages.extend(memory)
        messages.append({'role': 'user', 'content': player_message})

        response = self.client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=messages,
            temperature=1.0, #感情レベル
        )

        reply = response.choices[0].message.content
        return reply

#streamlit UI 部分
st.set_page_config(page_title='Mustacheと話そう！')
st.title('Mustacheと話そう！')

col1, col2 = st.columns([2,1])
with col1:
    # ここに立ち絵画像のパスを入れる（同じフォルダに heroine.png を置くイメージ）
    st.image('Mustache.png', caption='Mustache', use_container_width=True)
with col2:
    if 'Mustache' not in st.session_state:
        st.session_state.Mustache = Character('Mustache', 'おしゃべり', client)
    if 'memory' not in st.session_state:
        st.session_state.memory = []
    
#入力欄
user_input = st.text_input('入力してください(Enterで送信)')
if user_input:
    Mustache = st.session_state.Mustache

    reply = Mustache.ai_reply(st.session_state.memory, user_input)

    st.session_state.memory.append({'role': 'user', 'content': user_input})
    st.session_state.memory.append({'role': 'assistant', 'content': reply})

st.markdown('---')

#チャットログ
st.markdown('### Mustache')
if len(st.session_state.memory) == 0:
    st.markdown('まだ会話がありません。')
else:
    latest_messages = st.session_state.memory[-1:]  #last 1 lines
    for m in latest_messages:
        st.markdown(f'Mustache：{m["content"]}')
st.markdown('---')


