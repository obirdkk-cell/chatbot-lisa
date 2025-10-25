import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="ChatGPT 사용 가이드 챗봇", page_icon="💬", layout="wide")
st.title("💬 ChatGPT 사용설명 가이드 챗봇")
st.caption("ChatGPT의 기능, 활용법, 프롬프트 작성법 등을 단계별로 안내해주는 챗봇입니다.")

# API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API Key를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 초기 시스템 프롬프트 (챗봇의 성격 설정)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 ChatGPT 사용법을 알려주는 가이드 챗봇이야. "
                    "사용자가 ChatGPT의 기능, 프롬프트 작성 요령, 이미지 생성 방법, "
                    "교육 활용법 등을 물어보면 초보자 눈높이에서 구체적이고 친절하게 설명해줘. "
                    "필요하면 예시 프롬프트도 함께 알려줘."
                ),
            }
        ]

    # 대화 초기화 버튼
    if st.button("🧹 대화 새로 시작하기"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 ChatGPT 사용법을 알려주는 가이드 챗봇이야. "
                    "사용자가 ChatGPT의 기능, 프롬프트 작성 요령, 이미지 생성 방법, "
                    "교육 활용법 등을 물어보면 초보자 눈높이에서 구체적이고 친절하게 설명해줘. "
                    "필요하면 예시 프롬프트도 함께 알려줘."
                ),
            }
        ]
        st.rerun()

    # 이전 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("ChatGPT에 대해 궁금한 점을 입력하세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 표시
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
