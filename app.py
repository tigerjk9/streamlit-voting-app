import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(page_title="투표 시스템", layout="wide")

# Pretendard 폰트 및 추가 스타일 적용
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif !important;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-family: 'Pretendard', sans-serif !important;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        font-family: 'Pretendard', sans-serif !important;
    }
    /* 새로운 표 스타일 */
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: 'Pretendard', sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        width: 100%;
    }
    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 제목
st.title("🗳️ 간편한 투표 시스템")

# 초기화 함수
def reset_poll():
    if 'current_poll' in st.session_state:
        del st.session_state['current_poll']
    st.success("투표가 초기화되었습니다.")

# 사이드바에 투표 생성 기능
with st.sidebar:
    st.header("새 투표 만들기")
    question = st.text_input("투표 질문을 입력하세요:")
    options = st.text_area("선택지를 입력하세요 (각 줄에 하나씩):")
    options = [opt.strip() for opt in options.split('\n') if opt.strip()]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("투표 생성", key="create_poll"):
            if question and options:
                st.session_state['current_poll'] = {'question': question, 'options': options, 'votes': {opt: 0 for opt in options}}
                st.success("새 투표가 생성되었습니다!")
            else:
                st.error("질문과 최소 하나의 선택지를 입력해주세요.")
    with col2:
        if st.button("초기화", key="reset_poll", on_click=reset_poll):
            pass

# 메인 영역에 투표 및 결과 표시
if 'current_poll' in st.session_state:
    poll = st.session_state['current_poll']
    
    st.header(poll['question'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("투표하기")
        vote = st.radio("당신의 선택은?", poll['options'])
        if st.button("투표 제출"):
            poll['votes'][vote] += 1
            st.success("투표가 완료되었습니다!")
    
    with col2:
        st.subheader("투표 결과")
        results = pd.DataFrame.from_dict(poll['votes'], orient='index', columns=['득표수'])
        results = results.sort_values('득표수', ascending=False)
        total_votes = results['득표수'].sum()
        results['득표율'] = results['득표수'] / total_votes * 100
        
        # Plotly를 사용한 차트 생성
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'xy'}]])
        
        # 파이 차트
        fig.add_trace(go.Pie(
            labels=results.index, 
            values=results['득표수'], 
            hole=.3,
            textinfo='label+percent',
            insidetextorientation='radial',
            textfont=dict(family="Pretendard")
        ), 1, 1)
        
        # 막대 그래프
        fig.add_trace(go.Bar(
            x=results.index, 
            y=results['득표수'],
            text=results['득표수'],
            textposition='auto',
            marker_color='royalblue',
            textfont=dict(family="Pretendard")
        ), 1, 2)
        
        fig.update_layout(
            title_text="투표 결과 시각화",
            height=500,
            width=800,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Pretendard"),
        )
        
        fig.update_xaxes(title_text="", showgrid=False)
        fig.update_yaxes(title_text="득표수", showgrid=True, gridcolor='lightgray')
        
        st.plotly_chart(fig)
        
        # 표 형태로 결과 표시 (새로운 스타일 적용)
        st.markdown(results.style.format({'득표율': '{:.1f}%'}).to_html(classes='styled-table'), unsafe_allow_html=True)

else:
    st.info("왼쪽 사이드바에서 새 투표를 생성해주세요.")

# 푸터
st.markdown("---")
st.markdown("Made with by 닷커넥터")
