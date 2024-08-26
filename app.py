import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys

# 페이지 설정
st.set_page_config(page_title="투표 시스템", layout="wide")

# 사용자 정의 색상 팔레트 생성 함수
def generate_color_palette(n):
    HSV_tuples = [(x * 1.0 / n, 0.7, 0.9) for x in range(n)]
    RGB_tuples = [colorsys.hsv_to_rgb(*x) for x in HSV_tuples]
    return ['rgb({},{},{})'.format(int(r*255), int(g*255), int(b*255)) for r, g, b in RGB_tuples]

# Pretendard 폰트 및 추가 스타일 적용 (다크모드 대응 포함)
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif !important;
    }
    .stApp {
        background-color: #f0f4f8;
        transition: background-color 0.3s ease;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357abD;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        transition: all 0.3s ease;
    }
    .styled-table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .styled-table thead tr {
        background-color: #4a90e2;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
        transition: background-color 0.3s ease;
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f8f8f8;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #4a90e2;
    }
    .styled-table tbody tr:hover {
        background-color: #f0f0f0;
    }
    /* 다크 모드 대응 */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #1e1e1e;
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #2b2b2b;
            color: #ffffff;
            border-color: #4a4a4a;
        }
        .styled-table {
            box-shadow: 0 4px 6px rgba(255,255,255,0.1);
        }
        .styled-table thead tr {
            background-color: #4a90e2;
        }
        .styled-table tbody tr {
            background-color: #2b2b2b;
            color: #ffffff;
            border-bottom: 1px solid #4a4a4a;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #353535;
        }
        .styled-table tbody tr:hover {
            background-color: #3a3a3a;
        }
        .stMarkdown, .stMarkdown p {
            color: #ffffff;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 제목
st.title("🗳️ 고급 투표 시스템")

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
        
        # 색상 팔레트 생성
        colors = generate_color_palette(len(results))
        
        # Plotly 차트 생성
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{'type':'domain'}, {'type':'xy'}]],
            subplot_titles=('득표율', '득표수'),
        )
        
        fig.add_trace(go.Pie(
            labels=results.index,
            values=results['득표수'],
            hole=.4,
            marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
            textinfo='label+percent',
            insidetextorientation='radial',
            textfont=dict(size=12, color='#ffffff'),
            pull=[0.1 if i == results['득표수'].idxmax() else 0 for i in results.index]
        ), 1, 1)
        
        fig.add_trace(go.Bar(
            x=results.index,
            y=results['득표수'],
            marker=dict(color=colors, line=dict(color='#ffffff', width=1.5)),
            text=results['득표수'],
            textposition='auto',
            hoverinfo='x+y',
            textfont=dict(color='#ffffff')
        ), 1, 2)
        
        # 다크모드 감지 및 적용
        dark_mode = False
        try:
            dark_mode = st.get_theme() == 'dark'
        except:
            pass

        bg_color = '#1e1e1e' if dark_mode else '#ffffff'
        text_color = '#ffffff' if dark_mode else '#333333'
        grid_color = '#3a3a3a' if dark_mode else '#f0f0f0'
        
        fig.update_layout(
            title=dict(text="투표 결과 시각화", x=0.5, font=dict(size=24, color=text_color)),
            height=600,
            width=1000,
            font=dict(family="Pretendard", size=14, color=text_color),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            margin=dict(t=80, b=40, l=40, r=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=text_color)
            )
        )
        
        fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor=grid_color, tickfont=dict(size=12, color=text_color))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, showline=True, linewidth=2, linecolor=grid_color, tickfont=dict(size=12, color=text_color))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 표 형태로 결과 표시 (새로운 스타일 적용)
        st.markdown(results.style.format({'득표율': '{:.1f}%'}).to_html(classes='styled-table'), unsafe_allow_html=True)

else:
    st.info("왼쪽 사이드바에서 새 투표를 생성해주세요.")

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ by 닷커넥터")
