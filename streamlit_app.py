import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("💬 Chatbot")
st.write(
    "이 앱은 OpenAI의 GPT 모델을 사용한 간단한 챗봇입니다. "
    "API 키를 입력하고 대화를 시작해보세요!"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")
if not openai_api_key:
    st.info("API 키를 입력해야 대화를 시작할 수 있습니다.", icon="🗝️")
    st.stop()  # 키가 없으면 아래 코드 실행 안 됨

# OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

# 세션 상태에 messages가 없으면 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🗑️ 대화 초기화 버튼 추가
if st.button("🗑️ 대화 초기화"):
    st.session_state.messages = []  # 리스트 비우기
    st.success("대화를 초기화했습니다!")
    st.experimental_rerun()  # 페이지 새로고침 (초기화 반영)

# 지금까지의 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 입력창
if prompt := st.chat_input("무엇이 궁금한가요?"):
    # 사용자 입력 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API로 응답 생성
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # 응답 출력
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
