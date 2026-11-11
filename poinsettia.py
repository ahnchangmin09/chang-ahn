import html

GAME_VERSION = "2026-11-05 · 엔딩 돌아보기판"   # 화면에 표시되는 게임 버전
import json
import random
import uuid
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Page Configuration & Custom CSS (UI)
# ==========================================
st.set_page_config(
    page_title="포인센티아",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Hogwarts & Poinsettia Style Theme CSS
st.markdown("""
<style>
/* Global Styles - 애시포드 겨울밤의 딥 그린 & 네이비 무드 */
.stApp {
    background: linear-gradient(180deg, #070d14 0%, #0c1a13 100%);
    color: #e2e8f0;
    font-family: 'Georgia', serif;
}

/* Header Styling - 포인센티아 무드 */
.title-header {
    background: linear-gradient(135deg, #2b0d12 0%, #113a23 50%, #030a07 100%);
    padding: 30px;
    border-radius: 16px;
    border: 2px solid #8b263e;
    box-shadow: 0 8px 25px rgba(139, 38, 62, 0.25);
    text-align: center;
    margin-bottom: 25px;
}

.title-header h1 {
    color: #ff6b81; /* 포인센티아 레드 포인트 */
    font-family: 'Cinzel', serif;
    font-size: 2.3rem;
    margin-bottom: 8px;
    text-shadow: 0 0 12px rgba(255, 107, 129, 0.4);
}

.title-header p {
    color: #a3c1ad;
    font-size: 0.95rem;
    margin: 0;
    letter-spacing: 0.5px;
}

/* Dialogue Card */
.story-card {
    background-color: rgba(13, 27, 20, 0.85);
    border: 1px solid #1f3d2b;
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    backdrop-filter: blur(5px);
}

.location-tag {
    color: #6ee7b7;
    font-weight: bold;
    font-size: 0.9rem;
    margin-bottom: 12px;
    display: block;
    border-bottom: 1px solid #1f3d2b;
    padding-bottom: 8px;
}

/* 대화창 스타일 */
.dialogue-draco {
    background-color: rgba(10, 31, 20, 0.9);
    border-left: 4px solid #34d399;
    padding: 14px 18px;
    margin: 12px 0;
    border-radius: 0 10px 10px 0;
    color: #d1fae5;
}

.dialogue-hermione {
    background-color: rgba(31, 26, 15, 0.9);
    border-left: 4px solid #f59e0b;
    padding: 14px 18px;
    margin: 12px 0;
    border-radius: 0 10px 10px 0;
    color: #fef3c7;
}

.dialogue-harry {
    background-color: rgba(36, 15, 17, 0.9);
    border-left: 4px solid #ef4444;
    padding: 14px 18px;
    margin: 12px 0;
    border-radius: 0 10px 10px 0;
    color: #fee2e2;
}

.speaker-name {
    font-weight: bold;
    font-size: 0.95rem;
    margin-bottom: 4px;
}

.draco-name { color: #34d399; }
.hermione-name { color: #fbbf24; }
.harry-name { color: #f87171; }

/* 버튼 스타일 */
.stButton > button {
    width: 100%;
    background-color: #0f291d;
    color: #e2e8f0;
    border: 1px solid #1e4d35;
    padding: 14px 18px;
    border-radius: 10px;
    text-align: left;
    transition: all 0.25s ease;
    font-size: 0.95rem;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.stButton > button:hover {
    background-color: #163d2b;
    color: #ffffff;
    border-color: #34d399;
    box-shadow: 0 0 12px rgba(52, 211, 153, 0.3);
}

/* 사이드바·상단 바도 어두운 톤으로 */
[data-testid="stSidebar"] { background: #0b1611; }
[data-testid="stSidebar"][aria-expanded="true"] { min-width: 300px; }
[data-testid="stSidebar"] * { color: #d1e7dd; }
[data-testid="stHeader"] { background: rgba(7,13,20,0.9); }
.stApp h4, .stApp h3 { color: #e2e8f0; }

/* 입력칸·난이도 글자 */
.stApp label, .stApp label p, [data-testid="stWidgetLabel"] p { color: #d1e7dd !important; }

/* 결과 리포트 숫자 */
[data-testid="stMetricValue"] { color: #fda4af; }
[data-testid="stMetricLabel"] * { color: #a3c1ad; }

/* 화면 폭: 그림이 크게 보이도록 넓게 (너무 넓으면 글 읽기가 힘들어 1280px까지) */
.block-container { max-width: 1680px; padding-top: 2.2rem; padding-left: 2rem; padding-right: 2rem; }
.bet-alert {
    background: rgba(127, 29, 29, 0.85); border: 1px solid #f87171; color: #fee2e2;
    padding: 12px 18px; border-radius: 10px; margin-bottom: 12px; font-size: 1.05rem;
}
.story-card p { font-size: 1.12rem !important; }
.dialogue-draco, .dialogue-hermione, .dialogue-harry { font-size: 1.08rem; }

/* 지난 장면에서 이어지는 문장 */
.bridge {
    color: #c9b6e4; font-style: italic; font-size: 1.02rem; line-height: 1.7;
    border-left: 3px solid #8b5cf6; padding: 4px 0 4px 12px; margin-bottom: 12px;
}
.trap-note { color: #fca5a5; font-size: 0.9rem; }

/* 비주얼 노벨 무대 (배경 그림 비율 16:9 그대로, 화면 높이의 80%까지) */
.stage {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    max-height: 80vh;
    min-height: 420px;
    border-radius: 14px;
    background-size: cover;
    background-position: center;
    overflow: hidden;
    border: 1px solid #8b263e;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    margin-bottom: 14px;
}
.stage::after {
    content: "";
    position: absolute; left: 0; right: 0; bottom: 0; height: 30%;
    background: linear-gradient(180deg, rgba(7,13,20,0) 0%, rgba(7,13,20,0.85) 100%);
}
.stage-char {
    position: absolute;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    height: 100%;
    -webkit-mask-image: radial-gradient(ellipse 50% 62% at 50% 48%, #000 62%, transparent 100%);
    mask-image: radial-gradient(ellipse 50% 62% at 50% 48%, #000 62%, transparent 100%);
    z-index: 1;
}
.stage-loc {
    position: absolute; top: 12px; left: 14px; z-index: 2;
    background: rgba(7,13,20,0.7);
    color: #6ee7b7; font-weight: bold; font-size: 0.85rem;
    padding: 5px 12px; border-radius: 20px;
    border: 1px solid #1f3d2b;
}
/* 장면 전환: 새 장면이 검은 화면에서 서서히 밝아짐 */
@keyframes stageFade { from { filter: brightness(0); } to { filter: brightness(1); } }
.stage { animation: stageFade 0.9s ease-out both; }
@keyframes vnIn  { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes vnOut { from { opacity: 1; } to { opacity: 0; } }
@keyframes charIn  { from { opacity: 0; } to { opacity: 1; } }
.stage-char { animation-fill-mode: both; }

/* 그림 위에 겹치는 대사창 */
.vn-box {
    position: absolute; left: 3%; right: 3%; bottom: 3%; z-index: 3;
    max-height: 50%; overflow-y: auto;
    background: rgba(7, 13, 20, 0.80);
    border: 1px solid rgba(253, 164, 175, 0.45);
    border-radius: 14px; padding: 14px 22px;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.55);
    font-size: 1.08rem; line-height: 1.75; color: #f1f5f9;
}
.vn-line { animation: vnIn 0.5s ease both; margin: 2px 0 8px 0; }
.vn-box { cursor: pointer; }
.vn-skip { position: sticky; float: right; bottom: 0; margin-top: -4px; font-size: 0.78rem; color: #94a3b8;
    letter-spacing: 1px; pointer-events: none; }
@keyframes choiceIn { from { opacity: 0; visibility: hidden; transform: translateY(8px); }
    to { opacity: 1; visibility: visible; transform: none; } }
.vn-line:last-child { margin-bottom: 0; }
.vn-narr { color: #cbd5e1; }
.vn-bridge { color: #c9b6e4; font-style: italic; font-size: 0.98rem; }
.vn-name {
    display: inline-block; font-weight: bold; font-size: 0.92rem; margin-right: 8px;
    padding: 1px 10px; border-radius: 12px; background: rgba(255,255,255,0.08);
}
.vn-name.draco { color: #34d399; } .vn-name.hermione { color: #fbbf24; } .vn-name.harry { color: #f87171; }
.vn-stat { color: #fda4af; font-size: 0.92rem; }
/* 선택 직후 수치 변화 표시 (숫자 숨기기를 끄면 나옴) */
.stat-pop { position: absolute; top: 11%; right: 3%; z-index: 4; display: flex;
    flex-direction: column; align-items: flex-end; gap: 12px; pointer-events: none; }
.stat-badge { font-size: 1.6rem; font-weight: bold; color: #fff; padding: 10px 26px; border-radius: 40px;
    background: rgba(7,13,20,0.82); border: 2px solid rgba(255,255,255,0.25);
    text-shadow: 0 2px 6px #000; box-shadow: 0 6px 22px rgba(0,0,0,0.55);
    animation: statPop 0.7s cubic-bezier(.2,1.6,.4,1) both; }
.stat-badge b { font-size: 1.9rem; margin-left: 4px; }
.stat-badge.up { border-color: #34d399; } .stat-badge.up b { color: #6ee7b7; }
.stat-badge.down { border-color: #f87171; } .stat-badge.down b { color: #fca5a5; }
.stat-badge.zero b { color: #cbd5e1; }
@keyframes statPop { 0% { opacity: 0; transform: translateY(18px) scale(.6); }
    100% { opacity: 1; transform: none; } }
@media (max-width: 640px) { .stat-badge { font-size: 1.1rem; padding: 6px 14px; } .stat-badge b { font-size: 1.3rem; } }
.vn-trap { color: #fca5a5; font-weight: bold; }
.credits-wrap { height: 340px; overflow: hidden; position: relative; border-radius: 12px;
    background: rgba(7,13,20,0.75); border: 1px solid #8b263e; margin: 14px 0; }
@keyframes creditsUp { from { transform: translateY(340px); } to { transform: translateY(-100%); } }
.credits { position: absolute; width: 100%; text-align: center; color: #e2e8f0;
    animation: creditsUp 26s linear 0.5s both; line-height: 2.1; }
.credits h4 { color: #ff6b81; margin: 18px 0 2px 0; }
.event-tag { color: #fbbf24; font-weight: bold; }

.stage-label {
    position: absolute; top: 12px; right: 14px; z-index: 2;
    color: #fda4af; font-size: 0.85rem; letter-spacing: 1px;
    background: rgba(7,13,20,0.7); padding: 4px 10px; border-radius: 20px;
}
.avatar {
    width: 64px; height: 64px; border-radius: 50%;
    object-fit: cover; object-position: 50% 15%;
    vertical-align: middle; margin-right: 8px;
    border: 2px solid rgba(255,255,255,0.25);
}
.ending-cg {
    width: 100%; border-radius: 14px; border: 2px solid #8b263e;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5); margin-bottom: 14px;
}
@media (max-width: 640px) { .stage { aspect-ratio: 3 / 4; min-height: 0; } .vn-box { font-size: 0.98rem; max-height: 58%; } }

/* 초상화 */
.portrait-box {
    text-align: center;
    background: radial-gradient(ellipse at 50% 40%, rgba(179,36,60,0.25) 0%, rgba(13,27,20,0) 70%);
    border-radius: 14px;
    padding: 8px 4px 4px 4px;
}
.mood-label {
    color: #fda4af;
    font-size: 0.85rem;
    margin-top: 4px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1-2. 세라피나 표정 그림 (Princess-Maker 스타일 초상화)
#  - 기본: 아래 코드가 직접 그린 그림(SVG)
#  - 직접 그린 그림을 쓰고 싶으면: 이 파일 옆에 images 폴더를 만들고
#    cold.png / shy.png / angry.png / sad.png / smile.png / surprised.png
#    이름으로 넣으면 자동으로 그 그림이 대신 나옵니다.
# ==========================================
# 세라피나 윈터번 표정 그림 (SVG) 생성기
# emotion: cold, shy, angry, sad, smile, surprised

SKIN = "#fde8dc"
SKIN_SH = "#f3cfc0"
HAIR = "#f4e3b0"
HAIR_SH = "#d9c07e"
HAIR_HI = "#fff6d8"
EYE = "#3b6fd1"
EYE_DK = "#1d3b80"
NAVY = "#1f2a44"
NAVY_SH = "#151d31"
RED = "#b3243c"
LINE = "#5a3b2e"


def _eye(cx, cy, emo, side):
    """side: -1 왼쪽 눈(화면 기준), 1 오른쪽 눈"""
    s = []
    if emo == "smile":
        # 눈웃음: 위로 볼록한 곡선
        s.append(f'<path d="M{cx-15},{cy+4} Q{cx},{cy-12} {cx+15},{cy+4}" fill="none" stroke="{LINE}" stroke-width="3.5" stroke-linecap="round"/>')
        s.append(f'<path d="M{cx+side*15},{cy+3} l{side*5},-4" stroke="{LINE}" stroke-width="2.5" stroke-linecap="round"/>')
        return "".join(s)

    h = 17          # 눈 세로 반경
    lid = 0         # 윗눈꺼풀이 내려온 정도
    if emo == "cold":
        lid = 8
    elif emo == "angry":
        lid = 6
    elif emo == "surprised":
        h = 19
    elif emo == "sad":
        lid = 3

    w = 14
    # 흰자 + 홍채
    clip = f"clip{side}{emo}"
    top = cy - h + lid
    s.append(f'<clipPath id="{clip}"><path d="M{cx-w-2},{cy+2} Q{cx-w},{top} {cx},{top} Q{cx+w},{top} {cx+w+2},{cy+2} Q{cx+w},{cy+h} {cx},{cy+h} Q{cx-w},{cy+h} {cx-w-2},{cy+2}Z"/></clipPath>')
    s.append(f'<g clip-path="url(#{clip})">')
    s.append(f'<rect x="{cx-w-3}" y="{cy-h-3}" width="{2*w+6}" height="{2*h+6}" fill="#ffffff"/>')
    ir = 11 if emo != "surprised" else 9
    s.append(f'<ellipse cx="{cx}" cy="{cy+2}" rx="{ir}" ry="{ir+3}" fill="url(#iris)"/>')
    s.append(f'<ellipse cx="{cx}" cy="{cy+3}" rx="{ir*0.5:.1f}" ry="{(ir+3)*0.55:.1f}" fill="{EYE_DK}"/>')
    s.append(f'<circle cx="{cx-4}" cy="{cy-4}" r="3.6" fill="#ffffff"/>')
    s.append(f'<circle cx="{cx+4}" cy="{cy+8}" r="1.8" fill="#ffffff" opacity="0.85"/>')
    s.append('</g>')
    # 윗눈꺼풀 라인 (속눈썹)
    s.append(f'<path d="M{cx-w-3},{cy+3} Q{cx-w},{top-1} {cx},{top-1} Q{cx+w},{top-1} {cx+w+3},{cy+1}" fill="none" stroke="{LINE}" stroke-width="3.6" stroke-linecap="round"/>')
    s.append(f'<path d="M{cx+side*(w+2)},{cy+1} l{side*5},-5" stroke="{LINE}" stroke-width="2.6" stroke-linecap="round"/>')
    # 아랫눈꺼풀
    s.append(f'<path d="M{cx-w+3},{cy+h-1} Q{cx},{cy+h+2} {cx+w-3},{cy+h-1}" fill="none" stroke="{LINE}" stroke-width="1.3" opacity="0.6"/>')
    return "".join(s)


def _brows(emo):
    L, R = 125, 175
    y = 122
    shapes = {
        "cold":      ((-4, 2), (4, -2)),     # 살짝 치켜올림 (도도함)
        "angry":     ((-6, -4), (6, 4)),      # 안쪽이 내려감
        "sad":       ((-4, 5), (4, -5)),      # 안쪽이 올라감
        "shy":       ((-3, 3), (3, -3)),
        "smile":     ((-1, 0), (1, 0)),
        "surprised": ((0, -6), (0, -6)),
    }
    (a, b), _ = shapes[emo], None
    # a: 바깥쪽 높이 변화, b: 안쪽 높이 변화
    out_dy, in_dy = shapes[emo][0][0], shapes[emo][0][1]
    if emo == "surprised":
        out_dy, in_dy = -6, -6
    if emo == "angry":
        out_dy, in_dy = -5, 5
    if emo == "sad":
        out_dy, in_dy = 2, -6
    if emo == "cold":
        out_dy, in_dy = -4, 1
    if emo == "shy":
        out_dy, in_dy = 0, -3
    if emo == "smile":
        out_dy, in_dy = -1, -1
    s = []
    for cx, side in ((L, -1), (R, 1)):
        x_out = cx + side * 15
        x_in = cx - side * 11
        s.append(f'<path d="M{x_out},{y+out_dy} Q{cx},{y-5+min(out_dy,in_dy)} {x_in},{y+in_dy}" fill="none" stroke="#a9843f" stroke-width="3.8" stroke-linecap="round"/>')
    return "".join(s)


def _mouth(emo):
    cx, cy = 150, 197
    if emo == "smile":
        return (f'<path d="M{cx-11},{cy-2} Q{cx},{cy+10} {cx+11},{cy-2} Q{cx},{cy+3} {cx-11},{cy-2}Z" fill="#c4505f" stroke="{LINE}" stroke-width="1.6" stroke-linejoin="round"/>')
    if emo == "shy":
        return f'<path d="M{cx-6},{cy+1} Q{cx-3},{cy-2} {cx},{cy+1} Q{cx+3},{cy-2} {cx+6},{cy+1}" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
    if emo == "angry":
        return f'<path d="M{cx-9},{cy+3} Q{cx},{cy-4} {cx+9},{cy+3}" fill="none" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round"/>'
    if emo == "sad":
        return f'<path d="M{cx-8},{cy+3} Q{cx},{cy-3} {cx+8},{cy+3}" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'
    if emo == "surprised":
        return f'<ellipse cx="{cx}" cy="{cy+1}" rx="5" ry="6.5" fill="#a8414f" stroke="{LINE}" stroke-width="1.6"/>'
    # cold: 살짝 비스듬한 일자
    return f'<path d="M{cx-8},{cy+1} Q{cx+2},{cy+2} {cx+9},{cy-1}" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>'


def _extras(emo):
    s = []
    if emo in ("shy", "smile"):
        op = 0.55 if emo == "shy" else 0.3
        for x in (118, 182):
            s.append(f'<ellipse cx="{x}" cy="178" rx="14" ry="7" fill="#f58ea0" opacity="{op}"/>')
        if emo == "shy":
            for x in (110, 118, 174, 182):
                s.append(f'<line x1="{x}" y1="174" x2="{x+5}" y2="181" stroke="#e0607a" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/>')
    if emo == "sad":
        s.append('<path d="M112,170 Q107,184 112,190 Q117,184 112,170Z" fill="#bfe3ff" stroke="#7fb5e6" stroke-width="1"/>')
        s.append('<path d="M186,166 Q182,176 186,181 Q190,176 186,166Z" fill="#bfe3ff" stroke="#7fb5e6" stroke-width="1"/>')
    if emo == "angry":
        # 만화식 분노 표시
        s.append('<g transform="translate(205,92)" stroke="#d6334d" stroke-width="3.5" stroke-linecap="round" fill="none">'
                 '<path d="M-10,-3 Q-3,-3 -3,-10"/><path d="M3,-10 Q3,-3 10,-3"/>'
                 '<path d="M10,3 Q3,3 3,10"/><path d="M-3,10 Q-3,3 -10,3"/></g>')
        for x in (118, 182):
            s.append(f'<ellipse cx="{x}" cy="178" rx="12" ry="5" fill="#f58ea0" opacity="0.3"/>')
    if emo == "surprised":
        s.append(f'<g stroke="{LINE}" stroke-width="2.5" stroke-linecap="round">'
                 '<line x1="92" y1="70" x2="84" y2="58"/><line x1="100" y1="64" x2="98" y2="50"/>'
                 '<line x1="208" y1="70" x2="216" y2="58"/><line x1="200" y1="64" x2="202" y2="50"/></g>')
    return "".join(s)


def portrait_svg(emo="cold"):
    if emo not in ("cold", "shy", "angry", "sad", "smile", "surprised"):
        emo = "cold"
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 380" width="300" height="380">')
    p.append('<defs>'
             f'<radialGradient id="iris" cx="50%" cy="35%" r="70%"><stop offset="0" stop-color="#9fd0ff"/><stop offset="0.55" stop-color="{EYE}"/><stop offset="1" stop-color="{EYE_DK}"/></radialGradient>'
             f'<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR_HI}"/><stop offset="0.5" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_SH}"/></linearGradient>'
             f'<linearGradient id="coat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_SH}"/></linearGradient>'
             '</defs>')

    # 뒷머리 (긴 생머리)
    p.append(f'<path d="M92,120 Q78,40 150,30 Q222,40 208,120 Q216,200 226,290 Q232,330 214,350 L86,350 Q68,330 74,290 Q84,200 92,120Z" fill="url(#hair)"/>')

    p.append(f'<path d="M88,180 Q84,250 82,330 M212,180 Q216,250 218,330" fill="none" stroke="{HAIR_SH}" stroke-width="2" opacity="0.6"/>')
    # 몸 / 겨울 교복
    p.append(f'<path d="M40,380 Q44,292 112,262 L188,262 Q256,292 260,380Z" fill="url(#coat)"/>')
    # 흰 망토 칼라(겨울 퍼 트림 느낌)
    p.append('<path d="M100,268 Q150,300 200,268 Q214,280 222,300 Q150,334 78,300 Q86,280 100,268Z" fill="#f4f6fb" stroke="#d8dce8" stroke-width="1.5"/>')
    # 목
    p.append(f'<path d="M138,212 L137,262 Q150,274 163,262 L162,212Z" fill="{SKIN_SH}"/>')
    # 셔츠 칼라
    p.append('<path d="M126,256 L150,286 L174,256 L166,250 L150,272 L134,250Z" fill="#ffffff" stroke="#cfd4e0" stroke-width="1.2"/>')
    # 붉은 리본 (포인센티아)
    p.append(f'<path d="M150,284 L128,274 Q124,286 128,296Z" fill="{RED}"/><path d="M150,284 L172,274 Q176,286 172,296Z" fill="{RED}"/>'
             f'<path d="M146,284 L140,310 L148,306Z" fill="#8f1b30"/><path d="M154,284 L160,310 L152,306Z" fill="#8f1b30"/>'
             '<circle cx="150" cy="285" r="5" fill="#d23a52"/>')

    # 얼굴
    p.append(f'<path d="M104,118 Q102,186 150,228 Q198,186 196,118 Q196,66 150,64 Q104,66 104,118Z" fill="{SKIN}"/>')
    # 귀
    p.append(f'<ellipse cx="103" cy="150" rx="7" ry="12" fill="{SKIN_SH}"/><ellipse cx="197" cy="150" rx="7" ry="12" fill="{SKIN_SH}"/>')
    p.append('<circle cx="103" cy="164" r="2.6" fill="#9fd0ff" stroke="#ffffff" stroke-width="1"/><circle cx="197" cy="164" r="2.6" fill="#9fd0ff" stroke="#ffffff" stroke-width="1"/>')

    # 눈, 눈썹, 코, 입
    p.append(_eye(125, 150, emo, -1))
    p.append(_eye(175, 150, emo, 1))
    p.append(_brows(emo))
    p.append(f'<path d="M150,172 l-2,7 l3,0" fill="none" stroke="{SKIN_SH}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(_mouth(emo))

    # 앞머리 (옆으로 넘긴 뱅)
    p.append('<path d="M96,128 Q92,58 150,46 Q210,52 206,128 Q198,104 188,96 Q186,112 176,118 Q178,98 166,86 Q154,110 132,116 Q142,100 140,86 Q124,104 106,110 Q102,118 96,128Z" fill="url(#hair)"/>')
    p.append(f'<path d="M110,70 Q140,52 178,62" fill="none" stroke="{HAIR_HI}" stroke-width="5" stroke-linecap="round" opacity="0.9"/>')
    # 옆머리
    p.append('<path d="M98,112 Q90,170 98,214 Q104,180 108,140Z" fill="url(#hair)"/>')

    # 오른쪽 어깨로 내려오는 땋은 머리
    braid = [(200, 196), (205, 214), (208, 232), (208, 250), (205, 268), (200, 286), (195, 303)]
    p.append(f'<path d="M194,120 Q206,160 200,196" fill="none" stroke="{HAIR}" stroke-width="16" stroke-linecap="round"/>')
    for (x, y) in braid:
        p.append(f'<path d="M{x-12},{y-8} Q{x-4},{y+12} {x+1},{y+12} Q{x+6},{y+12} {x+12},{y-8} Q{x},{y+2} {x-12},{y-8}Z" fill="url(#hair)" stroke="{HAIR_SH}" stroke-width="1.3"/>')
        p.append(f'<path d="M{x-6},{y-2} Q{x},{y+6} {x+6},{y-2}" fill="none" stroke="{HAIR_HI}" stroke-width="1.6" opacity="0.8"/>')
    p.append(f'<path d="M188,312 L195,306 L202,312 L195,318Z" fill="{RED}"/>')
    p.append(f'<path d="M193,318 Q190,332 186,340 M197,318 Q200,332 203,340" stroke="{HAIR}" stroke-width="5" stroke-linecap="round" fill="none"/>')

    # 머리 장식: 작은 포인센티아 꽃
    cx, cy = 116, 74
    for k in range(5):
        ang = k * 72
        p.append(f'<ellipse cx="{cx}" cy="{cy-8}" rx="4.5" ry="9" fill="{RED}" transform="rotate({ang} {cx} {cy})"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#f2c94c"/>')

    p.append(_extras(emo))
    p.append('</svg>')
    return "".join(p)


EMOTIONS = {
    "cold": "새침",
    "shy": "수줍음",
    "angry": "화남",
    "sad": "슬픔",
    "smile": "미소",
    "surprised": "놀람",
}



import base64
import io
import os

# 그림 파일을 찾는 위치: 게임 파일과 같은 폴더 → images 폴더 → character_portraits 폴더
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIRS = [BASE_DIR,
               os.path.join(BASE_DIR, "images"),
               os.path.join(BASE_DIR, "character_portraits"),
               os.path.join(BASE_DIR, "sounds")]

# 날짜별 세라피나의 장면 분위기 (None = 세라피나가 등장하지 않는 장면)
DAY_MOOD = {
    1: "cold", 2: "cold", 3: "angry", 4: "sad", 5: "shy",
    6: "surprised", 7: "angry", 8: "surprised", 9: "sad", 10: None,
    11: "sad", 12: "shy", 13: None, 14: "smile", 15: "smile",
    16: "surprised", 17: "shy", 18: "surprised", 19: "smile", 20: "shy",
    21: "cold", 22: "angry", 23: "sad", 24: "sad", 25: "sad",
    26: "surprised", 27: "smile", 28: "smile", 29: "shy", 30: "smile",
}

# 세라피나가 없는 날 무대에 서는 인물
DAY_OTHER = {10: "clara_normal", 13: "ethan_normal"}

# 대화창 옆 작은 얼굴 (대사 스타일 → 그림 파일)
AVATAR = {"draco": "seraphina_50", "hermione": "clara_normal", "harry": "ethan_normal"}

# 호감도 단계별 세라피나 표정 이름
LEVEL_LABEL = {10: "차가움", 20: "슬픔", 30: "경계", 40: "의심", 50: "무심",
               60: "옅은 미소", 70: "수줍음", 80: "편안함", 90: "애정", 100: "행복"}

# 엔딩별 그림: (엔딩 CG, 없을 때 쓸 배경, 표정 단계)
ENDING_ART = {
    1: ("ending_happy", "bg_14", 100),
    2: ("ending_happy", "bg_14", 90),
    3: (None, "bg_15", 80),
    4: ("ending_sad", "bg_18", 20),
    5: ("ending_sad", "bg_04", 50),
    6: ("ending_sad", "bg_18", 10),
}


def mood_for_day(day):
    mood = DAY_MOOD.get(day)
    if mood is None:
        return None
    # 24일차: 23일차에 솔직하지 않았다면 차가운 표정
    if day == 24 and not st.session_state.flags.get("day23_honest"):
        return "cold"
    # 관계가 크게 틀어졌다면 웃는 장면에서도 새침한 표정
    if mood in ("smile", "shy") and st.session_state.distance >= 50:
        return "cold"
    # 아직 서먹한 사이라서 장면이 서먹한 버전으로 바뀐 날: 설레는 표정 대신 새침한 표정
    if day in DISTANT and mood in ("smile", "shy", "surprised") and is_distant(day):
        return "cold"
    return mood


def seraphina_level(mood):
    """현재 호감도 → 세라피나 표정 단계(10~100), 장면 분위기는 보조로만 반영

    표정 순서: 10 차가움 → 50 무심 → 60 옅은 미소 → 70 수줍음 → 80 편안함 → 90 애정 → 100 행복
    20 슬픔 · 30 경계 · 40 의심은 슬픈 장면, 다툼 장면, 상처를 준 직후에만 씁니다.
    """
    aff = st.session_state.affection
    level = min(100, max(10, int(round(aff / 10.0)) * 10))

    # 호감도가 그대로 드러나는 '기본 표정'
    if level >= 50:
        base = level
    elif level >= 30:
        base = 50          # 경계가 풀리기 시작: 무심한 표정
    else:
        base = 10          # 아직 차가운 표정

    # 바로 전 선택으로 상처를 줬다면, 다음 장면에서는 경계하는 표정
    if st.session_state.get("last_mistake") and mood != "sad":
        return 30

    if mood == "sad":
        return 20
    if mood == "angry":
        return 30 if level < 60 else 40
    if mood == "cold":
        return 10 if level < 40 else 50
    return base            # 수줍음·미소·놀람 장면: 호감도 그대로


def find_image(name):
    for d in SEARCH_DIRS:
        for ext in ("png", "jpg", "jpeg", "webp"):
            path = os.path.join(d, f"{name}.{ext}")
            if os.path.exists(path):
                return path
    return None


@st.cache_data(show_spinner=False)
def _image_uri(path, max_w, mtime):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_w, max_w * 2))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def image_uri(name, max_w=1280):
    path = find_image(name)
    if not path:
        return None
    return _image_uri(path, max_w, os.path.getmtime(path))


def svg_uri(mood):
    return "data:image/svg+xml;base64," + base64.b64encode(portrait_svg(mood).encode("utf-8")).decode()


def stage_html(bg_code, char_name, label, loc_text, fallback_mood=None):
    """배경 위에 인물을 세운 비주얼 노벨 무대"""
    bg = image_uri(bg_code, 1672) if bg_code else None
    char = image_uri(char_name, 1086) if char_name else None
    if char is None and fallback_mood:
        char = svg_uri(fallback_mood)
    bg_style = f"background-image:url('{bg}');" if bg else "background:linear-gradient(180deg,#0b1a2e,#0c1a13);"
    char_tag = f'<img class="stage-char" src="{char}">' if char else ""
    label_tag = f'<span class="stage-label">{label}</span>' if label else ""
    return (f'<div class="stage" style="{bg_style}">'
            f'<span class="stage-loc">{loc_text}</span>{char_tag}{label_tag}</div>')


@st.cache_data(show_spinner=False)
def _backdrop_uri(path, mtime):
    """화면 양옆을 채울 배경: 장면 그림을 작게 줄여 흐리고 어둡게 만든 것"""
    from PIL import Image, ImageEnhance, ImageFilter
    im = Image.open(path).convert("RGB")
    im.thumbnail((640, 640))
    im = im.filter(ImageFilter.GaussianBlur(10))
    im = ImageEnhance.Brightness(im).enhance(0.55)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def backdrop_css(name):
    """지금 장면 그림을 흐리게 깔아서 화면 전체 배경으로 씀"""
    path = find_image(name) if name else None
    if not path:
        return ""
    uri = _backdrop_uri(path, os.path.getmtime(path))
    return ("<style>.stApp{background:"
            "linear-gradient(180deg,rgba(7,13,20,0.35) 0%,rgba(7,13,20,0.65) 100%),"
            f"url('{uri}') center / cover fixed !important;}}</style>")


# 대사 속도: 글자 하나당 기다리는 시간(초), 한 줄 최소 시간
TEXT_SPEED = {"즉시": (0, 0), "빠르게": (0.012, 0.35), "보통": (0.022, 0.6), "느리게": (0.04, 1.0)}

# 대사 스타일 → 그 인물이 말할 때 무대에 서는 그림 (세라피나는 표정 단계로 따로 정함)
SPEAKER_IMG = {"hermione": "clara_normal", "harry": "ethan_normal"}


def vn_stage(bg_code, loc_text, label, lines, first_char=None, fallback_mood=None, overlay=""):
    """그림 위에 대사창이 겹쳐진 무대.
    lines: [{"kind": bridge|narr|say|stat|trap, "text", "speaker", "cls", "char"}]
    대사가 한 줄씩 차례로 나타나고, 말하는 사람이 바뀌면 무대 위 인물도 바뀜"""
    per_char, min_t = TEXT_SPEED.get(st.session_state.get("text_speed", "보통"), TEXT_SPEED["보통"])
    t = 0.7
    segments = []                     # (그림 이름, 시작 시간)
    if first_char:
        segments.append((first_char, 0.0))
    html_lines = []
    for ln in lines:
        if ln["kind"] == "say" and ln.get("char") and (not segments or segments[-1][0] != ln["char"]):
            segments.append((ln["char"], t if segments else 0.0))
        delay = f"animation-delay:{t:.2f}s;"
        if ln["kind"] == "say":
            body = (f'<span class="vn-name {ln["cls"]}">{ln["speaker"]}</span>'
                    f'<span>"{ln["text"]}"</span>')
            cls = "vn-line"
        elif ln["kind"] == "bridge":
            body, cls = ln["text"], "vn-line vn-bridge"
        elif ln["kind"] == "stat":
            body, cls = ln["text"], "vn-line vn-stat"
        elif ln["kind"] == "trap":
            body, cls = ln["text"], "vn-line vn-trap"
        else:
            body, cls = ln["text"], "vn-line vn-narr"
        html_lines.append(f'<div class="{cls}" style="{delay}">{body}</div>')
        t += max(min_t, per_char * len(ln["text"])) if per_char else 0

    # 인물 그림: 차례대로 나타났다가, 다음 인물이 나오면 사라짐
    imgs = []
    for i, (name, start) in enumerate(segments):
        uri = image_uri(name, 1086)
        if uri is None and name.startswith("seraphina") and fallback_mood:
            uri = svg_uri(fallback_mood)
        if uri is None:
            continue
        anim = f"charIn 0.6s ease {start:.2f}s both"
        if i + 1 < len(segments):
            anim += f", vnOut 0.5s ease {segments[i + 1][1]:.2f}s forwards"
        imgs.append(f'<img class="stage-char" src="{uri}" style="animation:{anim};">')

    bg = image_uri(bg_code, 1672) if bg_code else None
    bg_style = f"background-image:url('{bg}');" if bg else "background:linear-gradient(180deg,#0b1a2e,#0c1a13);"
    label_tag = f'<span class="stage-label">{label}</span>' if label else ""
    VN_END[0] = t + 0.3                # 대사가 다 나오는 시각 → 그 뒤에 선택지가 나타남
    skip = (f'<span class="vn-skip" style="animation:vnOut .4s ease {t:.2f}s forwards;">▶▶ 대사창을 누르면 바로 넘어가요</span>'
            if t > 1.2 else "")
    return (f'<div class="stage" style="{bg_style}"><span class="stage-loc">{loc_text}</span>'
            + "".join(imgs) + label_tag
            + overlay + f'<div class="vn-box">{"".join(html_lines)}{skip}</div></div>')


VN_END = [0.0]


def choices_after_text():
    """선택지(버튼)를 대사가 다 나온 뒤에 나타나게 하는 스타일.
    대사창을 누르면 바로 나타남 (화면 쪽 스크립트가 처리)"""
    d = VN_END[0]
    return (f"<style>.stButton, .choice-head {{ animation: choiceIn .5s ease {d:.2f}s both; }}"
            "[data-testid='stSidebar'] .stButton { animation: none !important; }</style>")


# ==========================================
# 에필로그 영상 (해피 엔딩 1·2)
#  그림들이 천천히 확대되며 넘어가고, 자막과 함께 꽃잎·눈이 내림.
#  트루 엔딩: 졸업 → 정원 → 프러포즈 → 별밤 위로 제작진 자막 → 결혼식 그림(epilogue_wedding.jpg)
#  해피 엔딩: 졸업 → 정원 → 여전히 연애 중 → 약속의 반지 + 제작진 자막
#  영상 안의 '에필로그 다시 보기' 버튼을 누르면 영상과 노래가 처음부터 다시 나옴.
#  직접 만든 그림을 쓰고 싶으면 이 폴더에 epilogue_1.jpg ~ epilogue_3.jpg 를 넣으면
#  그 순서의 장면이 그 그림으로 바뀜 (인물 그림 없이 그 그림만 나옴)
# ==========================================
EP_SCENE = 6.5      # 장면 하나 길이(초)
EP_FADE = 1.3       # 장면이 겹치며 넘어가는 시간(초)
EP_CREDITS = 24.0   # 트루 엔딩 자막 장면 길이(초)
EP_REVEAL = 11.0    # 결혼식 그림이 얼굴부터 전체로 천천히 펼쳐지는 시간(초)

# 결혼식 그림 속 '에필로그 다시 보기' 버튼 자리 (그림 크기에 대한 비율, %)
WEDDING_BTN = {"left": 73.2, "top": 88.3, "width": 24.6, "height": 4.2}


def epilogue_scenes(ending_id, raw_name):
    p = html.escape(raw_name)
    p_wa = p + josa(raw_name, "과", "와")       # 민준과 / 레오와
    if ending_id == 1:      # 결혼
        return [
            {"bg": "bg_14", "char": "seraphina_90", "small": "1년 후",
             "cap": f"졸업식 날, {p_wa} 세라피나는 다시 눈 덮인 천문탑에 올랐다."},
            {"bg": "bg_12", "char": "seraphina_100", "small": "3년 후",
             "cap": "둘이 함께 가꾼 정원에, 올해도 붉은 포인센티아가 피었다."},
            {"bg": "ending_happy", "char": None, "small": "5년 후 · 첫눈 오는 날",
             "cap": "'30일 내기, 이번엔 평생으로 하자.' 세라피나는 울면서 웃었다."},
            # 결혼식 그림이 없을 때만 쓰는 장면
            {"bg": "bg_03", "char": "seraphina_100", "small": "그리고, 겨울의 끝",
             "cap": f"💍 결혼을 축하합니다 · {p} ♥ 세라피나", "wedding": True},
        ]
    return [                # 엔딩 2: 계속 연애
        {"bg": "bg_14", "char": "seraphina_80", "small": "1년 후",
         "cap": "새침한 말투는 그대로지만, 세라피나는 이제 먼저 손을 내민다."},
        {"bg": "bg_12", "char": "seraphina_90", "small": "2년 후",
         "cap": "정원 벤치는 어느새 둘만의 약속 장소가 되었다."},
        {"bg": "ending_happy", "char": None, "small": "3년 후 · 여전히 연애 중",
         "cap": f"'{p}, 내년 첫눈도 같이 보는 거다?'"},
        {"bg": "bg_15", "char": "seraphina_100", "small": "그리고 오늘 밤",
         "cap": "새끼손가락에 끼운 작은 약속의 반지. 둘의 겨울은 계속된다.", "wedding": True},
    ]


def _falling(rnd, start, petals, snow, spread=6.0):
    out = []
    for _ in range(petals):       # 떨어지는 포인센티아 꽃잎
        out.append(f'<span class="ep-petal" style="left:{rnd.uniform(0, 100):.1f}%;'
                   f'animation-duration:{rnd.uniform(5, 9):.1f}s;'
                   f'animation-delay:{start + rnd.uniform(0, spread):.1f}s;"></span>')
    for _ in range(snow):         # 내리는 눈
        out.append(f'<span class="ep-snow" style="left:{rnd.uniform(0, 100):.1f}%;'
                   f'animation-duration:{rnd.uniform(6, 11):.1f}s;'
                   f'animation-delay:{start + rnd.uniform(0, spread):.1f}s;"></span>')
    return "".join(out)


def _ep_scene(i, sc, start, show, rnd, cap_anim):
    """그림 + 인물 + 자막 한 장면"""
    custom = image_uri(f"epilogue_{i + 1}", 1672) if i < 3 else None
    bg = custom or image_uri(sc["bg"], 1672)
    char = None if custom or not sc["char"] else image_uri(sc["char"], 1086)
    inner = [f'<div class="ep-bg" style="background-image:url(\'{bg}\');'
             f'animation:epZoom {EP_SCENE + 4}s ease-out {start:.2f}s both;"></div>']
    if sc.get("wedding"):
        inner.append('<div class="ep-glow"></div>')
    if char:
        inner.append(f'<img class="ep-char" src="{char}">')
    if sc.get("wedding"):
        inner.append('<div class="ep-ring">💍</div>')
    inner.append(_falling(rnd, start, 26 if sc.get("wedding") else 0, 18))
    inner.append(f'<div class="ep-cap" style="animation:{cap_anim};"><small>{sc["small"]}</small>{sc["cap"]}</div>')
    return f'<div class="ep-scene" style="animation:{show};">{"".join(inner)}</div>'


def _replay_btn(extra_class, delay, style=""):
    return (f'<div class="ep-replay {extra_class}" role="button" title="에필로그 다시 보기" '
            f'style="animation:epBtn 1.2s ease {delay:.2f}s both;{style}">'
            f'<span class="ep-replay-icon">⟳</span> 에필로그 다시 보기</div>')


EP_STYLE = """<style>
.ep-stage{position:relative;width:100%;aspect-ratio:4/3;max-height:88vh;min-height:460px;overflow:hidden;
  border-radius:14px;border:1px solid #8b263e;background:#000;box-shadow:0 8px 25px rgba(0,0,0,.5);margin-bottom:14px}
.ep-scene{position:absolute;inset:0;opacity:0;overflow:hidden}
.ep-bg{position:absolute;inset:0;background-size:cover;background-position:center}
.ep-char{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:100%;
  -webkit-mask-image:radial-gradient(ellipse 50% 62% at 50% 48%,#000 62%,transparent 100%);
  mask-image:radial-gradient(ellipse 50% 62% at 50% 48%,#000 62%,transparent 100%)}
.ep-cap{position:absolute;left:4%;right:4%;bottom:6%;text-align:center;color:#fff;font-size:1.45rem;
  line-height:1.6;text-shadow:0 2px 10px #000,0 0 4px #000;z-index:6;opacity:0}
.ep-cap small{display:block;color:#fda4af;font-size:.95rem;letter-spacing:3px;margin-bottom:4px}
.ep-glow{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 35%,rgba(255,214,140,.38),transparent 62%);
  animation:epPulse 3s ease-in-out infinite alternate;z-index:1}
.ep-ring{position:absolute;top:10%;left:26%;font-size:3.6rem;z-index:3;
  filter:drop-shadow(0 0 14px #ffd27a);animation:epPulse 2.4s ease-in-out infinite alternate}
.ep-portrait{position:absolute;top:0;bottom:0;left:0;right:0;margin:auto;height:100%;aspect-ratio:1024/1536;
  z-index:2;transform-origin:50% 22%;box-shadow:0 0 60px rgba(0,0,0,.7)}
.ep-portrait img{width:100%;height:100%;display:block}
.ep-petal{position:absolute;top:-6%;width:15px;height:10px;background:#c81e3a;border-radius:70% 0 70% 0;
  opacity:0;z-index:4;animation-name:epFall;animation-timing-function:linear;animation-iteration-count:infinite;animation-fill-mode:backwards}
.ep-snow{position:absolute;top:-4%;width:6px;height:6px;background:#fff;border-radius:50%;opacity:0;z-index:3;
  animation-name:epFall;animation-timing-function:linear;animation-iteration-count:infinite;animation-fill-mode:backwards}
.ep-credits{position:absolute;inset:0;z-index:5;opacity:0;
  background:linear-gradient(90deg,rgba(7,13,20,0) 0%,rgba(7,13,20,.62) 30%,rgba(7,13,20,.62) 70%,rgba(7,13,20,0) 100%)}
.ep-roll{position:absolute;left:0;right:0;top:100%;text-align:center;color:#fff;line-height:2.1;text-shadow:0 2px 6px #000;z-index:5}
.ep-roll h3{color:#ff6b81;margin:0 0 10px 0}.ep-roll h4{color:#fda4af;margin:20px 0 2px 0}.ep-roll p{margin:0}
.ep-end{position:absolute;left:0;right:0;top:44%;text-align:center;color:#fff;font-size:2rem;opacity:0;
  text-shadow:0 2px 10px #000;letter-spacing:6px}
/* 진짜로 눌리는 '에필로그 다시 보기' 버튼 (그림 속 버튼과 같은 모양) */
.ep-replay{position:absolute;z-index:8;display:flex;align-items:center;justify-content:center;gap:.5em;
  box-sizing:border-box;cursor:pointer;user-select:none;white-space:nowrap;
  background:linear-gradient(180deg,rgba(52,44,40,.96),rgba(28,23,21,.96));color:#f6e7c8;
  border:1.5px solid #c9a66b;border-radius:12px;box-shadow:0 0 0 1px rgba(0,0,0,.5),0 4px 14px rgba(0,0,0,.5);
  font-family:'Noto Serif KR','Nanum Myeongjo',Georgia,serif;font-size:14px;transition:box-shadow .2s,filter .2s;
  visibility:hidden;opacity:0}
.ep-stage *{pointer-events:none}   /* 자막·꽃잎 등이 버튼 클릭을 가리지 않도록 */
.ep-stage .ep-replay{pointer-events:auto}
.ep-replay:hover{box-shadow:0 0 0 1px rgba(0,0,0,.5),0 0 18px rgba(255,210,122,.8);filter:brightness(1.12)}
.ep-replay-icon{color:#e8c27a;font-size:1.25em;line-height:1}
.ep-replay-img{font-size:clamp(10px,1.45vh,17px)}
.ep-replay-corner{right:3%;bottom:5%;padding:10px 22px;font-size:16px}
@keyframes epShow{0%{opacity:0}18%{opacity:1}82%{opacity:1}100%{opacity:0}}
@keyframes epShowLong{0%{opacity:0}6%{opacity:1}94%{opacity:1}100%{opacity:0}}
@keyframes epStay{from{opacity:0}to{opacity:1}}
@keyframes epOut{from{opacity:1}to{opacity:0}}
@keyframes epBtn{from{opacity:0;visibility:visible}to{opacity:1;visibility:visible}}
@keyframes epZoom{from{transform:scale(1.14)}to{transform:scale(1.0)}}
@keyframes epReveal{from{transform:scale(2.15)}to{transform:scale(1.0)}}
@keyframes epPulse{from{opacity:.65}to{opacity:1}}
@keyframes epFall{0%{top:-6%;opacity:0;transform:translateX(0) rotate(0)}8%{opacity:.9}
  100%{top:106%;opacity:.9;transform:translateX(60px) rotate(620deg)}}
@keyframes epRoll{from{top:100%;transform:translateY(0)}to{top:0;transform:translateY(-100%)}}
@media (max-width:640px){.ep-stage{aspect-ratio:3/4}.ep-cap{font-size:1.1rem}}
</style>"""


def epilogue_movie(ending_id, raw_name, credits_html):
    scenes = [localize(sc) for sc in epilogue_scenes(ending_id, raw_name)]
    rnd = random.Random(7)
    step = EP_SCENE - EP_FADE
    parts = []
    wedding_path = find_image("epilogue_wedding")

    if ending_id == 1 and wedding_path:
        # 1~3: 졸업 · 정원 · 프러포즈
        for i, sc in enumerate(scenes[:3]):
            start = step * i
            parts.append(_ep_scene(i, sc, start, f"epShow {EP_SCENE}s ease {start:.2f}s both", rnd,
                                   f"epStay 1.2s ease {start + 0.8:.2f}s both"))
        # 4: 별이 쏟아지는 밤하늘 위로 제작진 자막
        c0 = step * 3
        night = image_uri("bg_15", 1672)
        parts.append(
            f'<div class="ep-scene" style="animation:epShowLong {EP_CREDITS}s ease {c0:.2f}s both;">'
            f'<div class="ep-bg" style="background-image:url(\'{night}\');filter:brightness(.45);'
            f'animation:epZoom {EP_CREDITS + 2}s ease-out {c0:.2f}s both;"></div>'
            + _falling(rnd, c0, 0, 24, 10) +
            f'<div class="ep-roll" style="animation:epRoll {EP_CREDITS - 3}s linear {c0 + 1.5:.2f}s both;">'
            f'{credits_html}</div></div>')
        # 5: 결혼식 그림 — 신부의 얼굴에서 시작해 천천히 전체가 펼쳐짐
        w0 = c0 + EP_CREDITS - EP_FADE
        wed = _image_uri(wedding_path, 1536, os.path.getmtime(wedding_path))
        fill = backdrop_uri("epilogue_wedding")
        b = WEDDING_BTN
        p = html.escape(raw_name)
        cap = T(f"<small>그리고, 겨울의 끝</small>💍 {p} ♥ 세라피나, 결혼을 축하합니다")
        parts.append(
            f'<div class="ep-scene" style="animation:epStay 1.6s ease {w0:.2f}s both;">'
            f'<div class="ep-bg" style="background-image:url(\'{fill}\');"></div>'
            f'<div class="ep-glow"></div>'
            f'<div class="ep-portrait" style="animation:epReveal {EP_REVEAL}s ease-in-out {w0:.2f}s both;">'
            f'<img src="{wed}">'
            + _replay_btn("ep-replay-img", w0 + EP_REVEAL + 0.6,
                          f"left:{b['left']}%;top:{b['top']}%;width:{b['width']}%;height:{b['height']}%;")
            + '</div>'
            + _falling(rnd, w0, 30, 16, 8) +
            f'<div class="ep-cap" style="animation:epStay 1.2s ease {w0 + 1.0:.2f}s both, '
            f'epOut 1.2s ease {w0 + EP_REVEAL - 2.5:.2f}s forwards;">{cap}</div></div>')
    else:
        # 해피 엔딩(또는 결혼식 그림이 없을 때): 마지막 장면 위로 제작진 자막
        n = len(scenes)
        last_start = step * (n - 1)
        credits_start = last_start + 8.5
        for i, sc in enumerate(scenes):
            start = step * i
            last = i == n - 1
            show = (f"epStay 1.4s ease {start:.2f}s both" if last
                    else f"epShow {EP_SCENE}s ease {start:.2f}s both")
            cap_anim = f"epStay 1.2s ease {start + 0.8:.2f}s both"
            if last:
                cap_anim += f", epOut 1s ease {credits_start:.2f}s forwards"
            parts.append(_ep_scene(i, sc, start, show, rnd, cap_anim))
        parts.append(
            f'<div class="ep-credits" style="animation:epStay 2s ease {credits_start:.2f}s both;">'
            f'<div class="ep-roll" style="animation:epRoll 30s linear {credits_start + 0.5:.2f}s both;">{credits_html}</div>'
            f'<div class="ep-end" style="animation:epStay 2s ease {credits_start + 30:.2f}s both;">— 끝 —</div></div>'
            + _replay_btn("ep-replay-corner", credits_start + 31))

    style = EP_STYLE
    return style + '<div class="ep-stage">' + "".join(parts) + "</div>"


def wedding_ending(ending_id):
    """결혼식 그림과 문구가 나오는 엔딩인지.
    쉬움·보통: 트루 엔딩만 / 어려움: 해피 엔딩과 트루 엔딩"""
    if st.session_state.get("difficulty") == "어려움":
        return ending_id in (1, 2)
    return ending_id == 1


def wedding_frame(caption=""):
    """에필로그 화면: 결혼식 그림이 바로 보이고 꽃잎이 내림.
    그림 속 버튼 자리에 진짜 '에필로그 다시 보기' 버튼 (누르면 연출과 노래가 처음부터)"""
    path = find_image("epilogue_wedding")
    if not path:
        return ""
    wed = _image_uri(path, 1536, os.path.getmtime(path))
    fill = backdrop_uri("epilogue_wedding")
    b = WEDDING_BTN
    rnd = random.Random(3)
    btn = (f'<div class="ep-replay ep-replay-img" role="button" title="에필로그 다시 보기" '
           f'style="animation:epBtn 1s ease 2.5s both;left:{b["left"]}%;top:{b["top"]}%;'
           f'width:{b["width"]}%;height:{b["height"]}%;">'
           f'<span class="ep-replay-icon">⟳</span> 에필로그 다시 보기</div>')
    cap = (f'<div class="wed-cap" style="animation:epStay 1.4s ease 1.2s both;">{caption}</div>'
           if caption else "")
    return (EP_STYLE +
            '<style>.wed-cap{position:absolute;top:3%;left:0;right:0;text-align:center;z-index:6;color:#fff;'
            'font-size:clamp(15px,2.4vh,26px);line-height:1.5;text-shadow:0 2px 10px #000,0 0 4px #000;opacity:0}'
            '.wed-cap small{display:block;color:#fda4af;font-size:.62em;letter-spacing:3px}</style>'
            '<div class="ep-stage" style="animation:stageFade 1.2s ease-out both;">'
            '<div class="ep-scene" style="opacity:1;">'
            f'<div class="ep-bg" style="background-image:url(\'{fill}\');"></div><div class="ep-glow"></div>'
            f'<div class="ep-portrait"><img src="{wed}" alt="결혼식">{btn}</div>'
            + _falling(rnd, 0.3, 28, 16, 6) + cap + '</div></div>')


def backdrop_uri(name):
    path = find_image(name)
    return _backdrop_uri(path, os.path.getmtime(path)) if path else ""


def avatar_tag(style_class):
    uri = image_uri(AVATAR.get(style_class, ""), 240)
    return f'<img class="avatar" src="{uri}">' if uri else "🗣️"



# ==========================================
# 1-3. 이름 모드: "원작" (해리 포터 세계관) / "오리지널" (애시포드 세계관)
#  - 이야기 글은 오리지널 이름으로 적혀 있고, 원작 모드일 때 화면에 보여주기 직전에 바꿉니다.
#  - 받침이 달라지는 이름은 조사(이/가, 을/를 등)까지 함께 바꿉니다.
# ==========================================
NAME_MODES = ["원작", "오리지널"]

TO_ORIGINAL = [
    # 화면 제목·소개
    ("애시포드 마법학원 로맨스 노벨", "호그와트 학창 시절 로맨스 노벨"),
    ("주인공 x 세라피나 윈터번", "주인공 x 여성 드레이코 말포이"),
    ("<b>세라피나 윈터번</b>", "<b>여성 드레이코 말포이</b>"),
    # 세라피나 윈터번 → 드레이코 말포이 (받침 있음 → 없음)
    ("세라피나 윈터번이", "드레이코 말포이가"), ("세라피나 윈터번과", "드레이코 말포이와"),
    ("세라피나 윈터번", "드레이코 말포이"),
    ("윈터번 가문", "말포이 가문"), ("윈터번 저택", "말포이 저택"), ("윈터번,", "말포이,"),
    ("윈터번", "말포이"),
    ("세라피나", "드레이코"),
    # 에단 애시비 → 해리 포터 (받침 있음 → 없음)
    ("에단 애시비가", "해리 포터가"), ("애시비 주제에", "포터 주제에"),
    ("에단에게", "해리에게"), ("에단이", "해리가"), ("에단은", "해리는"), ("에단을", "해리를"),
    ("에단과", "해리와"), ("에단의", "해리의"), ("에단", "해리"),
    # 클라라 → 헤르미온느
    ("클라라", "헤르미온느"),
    # 학교·기숙사
    ("애시포드", "호그와트"),
    ("불꽃과 서리의 충돌", "그리핀도르와 슬리데린의 충돌"),
    ("불꽃과 서리, 두 기숙사의 벽", "그리핀도르와 슬리데린, 두 기숙사의 벽"),
    ("불꽃과 서리 기숙사의 마찰", "그리핀도르와 슬리데린의 마찰"),
    ("서리와 불꽃 기숙사의 경계", "슬리데린과 그리핀도르의 국경"),
    ("서리 기숙사", "슬리데린"), ("불꽃 기숙사", "그리핀도르"),
    # 장소·인물·설정
    ("그레이브스 교수", "스네이프 교수"), ("연금술 교실", "마법약 교실"),
    ("속삭이는 숲", "금지된 숲"),
    ("도서관 봉인 서고", "도서관의 오래된 금서 구역"), ("봉인 서고", "금서 구역"),
    ("가문의 압박 때문에", "순혈주의 압박 때문에"),
    ("엄격한 규율과 압박을", "엄격한 규율과 순혈주의 압박을"),
    ("명문 귀족 가문", "순혈 가문"), ("다른 명문 귀족", "순혈 귀족"),
]


def name_mode():
    # 게임 중에는 시작할 때 고른 값, 시작 화면에서는 지금 고르고 있는 값
    if st.session_state.get("game_started"):
        return st.session_state.get("name_mode") or "원작"
    return st.session_state.get("name_mode_pick") or "원작"


def T(text):
    """현재 이름 모드에 맞게 글을 바꿈"""
    if not isinstance(text, str) or name_mode() != "원작":
        return text
    for a, b in TO_ORIGINAL:
        text = text.replace(a, b)
    return text


def localize(obj):
    """이야기 데이터(사전·리스트·튜플 안의 모든 글)를 한꺼번에 바꿈"""
    if isinstance(obj, str):
        return T(obj)
    if isinstance(obj, dict):
        return {k: localize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [localize(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(localize(v) for v in obj)
    return obj

# ==========================================
# 2. Session State Initialization
# ==========================================
def init_game():
    st.session_state.game_started = False
    st.session_state.player_name = ""
    st.session_state.day = 1
    st.session_state.affection = 20     # 호감도 (0 ~ 100)
    st.session_state.trust = 20         # 신뢰도 (0 ~ 100)
    st.session_state.distance = 0       # 거리감/서먹함 (0 ~ 100)
    st.session_state.clues = 0          # 수집한 단서 수
    st.session_state.game_over = False
    st.session_state.pending_toast = None

    # Major Choice Flags
    st.session_state.flags = {
        "told_reason_early": False,
        "kept_malfoy_secret": False,
        "hermione_advised": False,
        "harry_jealous_event": False,
        "day23_honest": False,
        "day23_defensive": False,
        "manor_visited": False,
        "defended_draco_public": False
    }
    st.session_state.history = []
    st.session_state.scars = 0
    st.session_state.last_mistake = False
    st.session_state.last_bridge = ""      # 지난 선택에서 다음 장면으로 이어지는 문장
    st.session_state.traps_hit = 0         # 빠진 함정 수
    st.session_state.last_choice = None    # (날짜, 고른 번호, 함정 여부) → 다음 날 선택지가 바뀜
    st.session_state.bet_penalty = 0       # 21일차 내기 들통으로 떨어진 호감도
    st.session_state.phase = "day"         # day 하루 장면 / react 반응 장면 / event 주말 이벤트 / epilogue
    st.session_state.reaction = None       # 반응 장면에 보여 줄 내용
    st.session_state.events_done = []      # 이미 지나간 주말 이벤트
    st.session_state.moments = []          # 함정·실수 기록 (엔딩의 '이번 판 돌아보기'용)
    st.session_state.run_id = uuid.uuid4().hex[:8]   # 이번 판 고유 번호 (선택지 섞기·엔딩 사운드용)
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "어려움"


if 'game_started' not in st.session_state:
    init_game()

# ==========================================
# 3. Helper Functions
# ==========================================
# ------------------------------------------
# 난이도 설정
#  gain    : 좋은 선택으로 오르는 수치 배율 (작을수록 조금씩 오름)
#  loss    : 나쁜 선택으로 깎이는 수치 배율 (클수록 많이 깎임)
#  dist    : 거리감이 늘어나는 배율
#  penalty : 잘못된 선택 1번마다 호감도·신뢰도 추가 감소 + 거리감 증가
#  scar_trust / scar_aff : '마음의 상처' 1개마다 신뢰도·호감도 최대치가 줄어드는 양
#   → 한 번 상처를 주면 끝까지 회복이 안 되는 부분이 남음
# ------------------------------------------
#  trap    : 함정 단계 (0 = 함정 없음, 2 = 보통 함정까지, 3 = 어려움 함정까지 전부)
#  shuffle : 선택지 순서를 섞을지
DIFFICULTY = {
    "쉬움":   {"gain": 1.0,  "loss": 1.0, "dist": 1.0, "penalty": 0,  "scar_trust": 0,  "scar_aff": 0,
              "trap": 0, "shuffle": False,
              "desc": "함정이 없어요. 이야기를 편하게 즐기고 싶을 때."},
    "보통":   {"gain": 0.4,  "loss": 1.5, "dist": 1.5, "penalty": 5,  "scar_trust": 15, "scar_aff": 5,
              "trap": 2, "shuffle": False,
              "desc": "호감도가 천천히 올라요. 가끔 좋아 보이는 선택이 함정이에요. 상처를 주면 트루 엔딩은 어려워져요."},
    "어려움": {"gain": 0.25, "loss": 2.0, "dist": 2.0, "penalty": 10, "scar_trust": 20, "scar_aff": 10,
              "trap": 3, "shuffle": True,
              "desc": "함정이 아주 많아요. 적극적으로 다가가도 때와 방법이 틀리면 세라피나가 싫어해요. 선택지 순서도 매번 섞여요."},
}


def scale_change(value, mult):
    """배율을 곱하고 반올림 (부호 유지)"""
    if value >= 0:
        return int(value * mult + 0.5)
    return -int(-value * mult + 0.5)


def stat_caps():
    d = DIFFICULTY[st.session_state.difficulty]
    scars = st.session_state.scars
    return 100 - d["scar_aff"] * scars, 100 - d["scar_trust"] * scars


def apply_choice(stat_changes):
    """선택지의 원래 수치에 난이도를 적용해 반영하고, 실제 변화량을 돌려줌"""
    d = DIFFICULTY[st.session_state.difficulty]
    raw_aff = stat_changes.get("aff", 0)
    raw_tru = stat_changes.get("tru", 0)
    raw_dist = stat_changes.get("dist", 0)
    clue = stat_changes.get("clue", 0)

    aff = scale_change(raw_aff, d["gain"] if raw_aff > 0 else d["loss"])
    tru = scale_change(raw_tru, d["gain"] if raw_tru > 0 else d["loss"])
    dist = scale_change(raw_dist, d["dist"]) if raw_dist > 0 else raw_dist

    mistake = raw_aff < 0 or raw_tru < 0
    if mistake and d["penalty"]:
        aff -= d["penalty"]
        tru -= d["penalty"]
        dist += d["penalty"]
    if mistake:
        st.session_state.scars += 1

    before_aff, before_tru = st.session_state.affection, st.session_state.trust
    cap_aff, cap_tru = stat_caps()
    st.session_state.affection = max(0, min(cap_aff, before_aff + aff))
    st.session_state.trust = max(0, min(cap_tru, before_tru + tru))
    st.session_state.distance = max(0, min(100, st.session_state.distance + dist))
    st.session_state.clues = max(0, st.session_state.clues + clue)
    return (st.session_state.affection - before_aff,
            st.session_state.trust - before_tru, mistake)


def update_stats(aff=0, tru=0, dist=0, clue=0):
    st.session_state.affection = max(0, min(100, st.session_state.affection + aff))
    st.session_state.trust = max(0, min(100, st.session_state.trust + tru))
    st.session_state.distance = max(0, min(100, st.session_state.distance + dist))
    st.session_state.clues = max(0, st.session_state.clues + clue)


def log_history(day, choice_text):
    st.session_state.history.append(f"Day {day}: {choice_text}")


def get_relationship_status():
    aff = st.session_state.affection
    tru = st.session_state.trust
    dist = st.session_state.distance

    if dist >= 70:
        return "❄️ 깊어진 오해와 이질감"
    elif aff >= 80 and tru >= 80:
        return "💖 서로에게 대체 불가능한 존재"
    elif aff >= 60 and tru >= 60:
        return "🌿 설렘과 깊은 신뢰"
    elif aff >= 40:
        return "💬 기대를 품은 호기심"
    elif tru < 30:
        return "🔍 강한 경계심과 의심"
    else:
        return "🧊 쌀쌀맞은 평범한 재학생"

def josa(word, with_batchim, without_batchim):
    """이름 끝 글자의 받침에 맞는 조사를 골라 줌 (예: 민준'을' / 레오'를')"""
    if not word:
        return without_batchim
    ch = word[-1]
    if "가" <= ch <= "힣":
        return with_batchim if (ord(ch) - 0xAC00) % 28 else without_batchim
    return f"{with_batchim}({without_batchim})"


# ==========================================
# 4. 30-Day Complete Story Data Structure
# ==========================================
def get_story_data(day):
    flags = st.session_state.flags
    # 이름이 HTML 안에 그대로 들어가므로 특수문자를 안전하게 변환
    p = html.escape(st.session_state.player_name)
    p_eul = p + josa(st.session_state.player_name, "을", "를")   # 레오를 / 민준을
    p_i = p + josa(st.session_state.player_name, "이", "가")     # 레오가 / 민준이

    story_db = {
        1: {
            "title": "첫 만남, 서늘한 눈빛",
            "bg": "bg_03 (애시포드 대연회장)",
            "desc": f"애시포드 대연회장의 아침. 서리 기숙사 테이블 끝자리에서 긴 백금발을 땋아 내린 세라피나 윈터번이 찻잔을 들고 있다. 어젯밤 친구들과 한 내기가 떠올라 그쪽을 바라보던 순간, 그녀의 차가운 눈빛이 {p_eul} 향한다.",
            "dialogue": [
                ("세라피나", "뭘 그렇게 빤히 봐? 불꽃 기숙사 학생이 왜 아침부터 서리 기숙사 테이블을 기웃거려?", "draco"),
                ("클라라", "(옆에서 속삭이며) 괜히 건드리지 마. 윈터번 가문 아가씨라 엄청 까다롭고 자존심도 세거든.", "hermione")
            ],
            "choices": [
                ("당당하게 눈을 맞추며 인사한다.", {"aff": +5, "tru": +2}, "세라피나가 눈썹을 찌푸렸지만, 당신에게 조금 흥미를 느낀 것 같습니다."),
                ("클라라 말대로 조용히 자리를 피한다.", {"aff": -2, "tru": 0}, "세라피나는 금세 당신에게서 관심을 거둡니다."),
                ("비꼬는 듯한 미소로 맞받아친다.", {"aff": -5, "dist": +5}, "세라피나가 차가운 눈빛으로 당신을 노려봅니다.")
            ]
        },
        2: {
            "title": "도서관의 신경전",
            "bg": "bg_06 (애시포드 도서관)",
            "desc": "마법약 과제를 하러 도서관에 왔다. 높은 책장에서 오래된 마법서를 꺼내려는 순간, 반대편에서 같은 책을 잡은 세라피나와 손끝이 닿았다.",
            "dialogue": [
                ("세라피나", "손 치워. 내가 먼저 잡았어. 그리고 네가 이렇게 어려운 책을 읽을 수나 있겠어?", "draco")
            ],
            "choices": [
                ("웃으면서 책을 먼저 양보한다.", {"aff": +5, "tru": +5}, "세라피나가 당황한 듯 책을 낚아채고는 고개를 홱 돌립니다."),
                ("내가 먼저 잡았다며 물러서지 않는다.", {"aff": -2, "dist": +3}, "실랑이를 벌이다 사서 선생님께 조용히 하라고 혼이 납니다."),
                ("같이 보자고 제안한다.", {"aff": +8, "tru": +3}, "세라피나가 콧방귀를 뀌면서도 옆자리를 내어 줍니다.")
            ]
        },
        3: {
            "title": "마법약 수업의 짝꿍",
            "bg": "bg_16 (연금술 교실)",
            "desc": "그레이브스 교수의 마법약 수업. 무작위로 짝을 정했는데, 하필 세라피나 윈터번과 한 조가 되었다. 그녀는 잔뜩 찌푸린 얼굴이다.",
            "dialogue": [
                ("세라피나", "내 재료에 손대지 마. 계량 하나 제대로 못 해서 내 점수까지 깎아 먹기만 해 봐.", "draco"),
                ("에단", "(지나가다) 윈터번, 그 불친절한 말투 좀 고치지 그래?", "harry")
            ],
            "choices": [
                ("에단 편을 들며 세라피나의 말투를 지적한다.", {"aff": -8, "dist": +5}, "세라피나가 입술을 깨물고는 수업 내내 당신을 쳐다보지도 않습니다."),
                ("세라피나의 지시대로 묵묵히, 완벽하게 해낸다.", {"aff": +8, "tru": +5}, "꼼꼼하게 재료를 손질하는 모습에 세라피나가 속으로 놀랍니다."),
                ("세라피나에게 슬쩍 장난을 건다.", {"aff": +3, "tru": 0}, "피식 웃던 세라피나가 금세 다시 차가운 표정으로 돌아갑니다.")
            ]
        },
        4: {
            "title": "창가에 홀로 선 그녀",
            "bg": "bg_18 (애시포드 복도 창가)",
            "desc": "수업이 끝난 늦은 오후. 복도 창가에 기대어 쓸쓸한 얼굴로 밖을 내다보는 세라피나가 보인다. 손에는 편지 한 장이 꽉 쥐어져 있다.",
            "dialogue": [
                ("세라피나", "...남 몰래 훔쳐보는 게 취미야? 보기 싫으니까 가던 길이나 가.", "draco")
            ],
            "choices": [
                ("무슨 일 있냐며 따뜻한 코코아를 건넨다.", {"aff": +10, "tru": +5}, "머뭇거리던 세라피나가 코코아를 받아 들고 작게 고맙다고 말합니다."),
                ("그 편지가 뭐냐고 묻는다.", {"aff": -5, "dist": +5}, "남의 집안일에 참견하지 말라며 차갑게 쏘아붙입니다."),
                ("조금 떨어져 서서 말없이 함께 창밖을 바라본다.", {"aff": +5, "tru": +8}, "말없이 곁을 지켜 주자 세라피나의 어깨에서 조금씩 힘이 빠집니다.")
            ]
        },
        5: {
            "title": "조금 누그러진 눈빛",
            "bg": "bg_05 (애시포드 계단)",
            "desc": ("계단에서 세라피나와 마주쳤다. 어제 복도에서 있었던 일 때문인지, 그녀의 눈빛이 다시 얼음장 같다."
                     if st.session_state.get("last_mistake") else
                     "계단에서 세라피나와 마주쳤다. 어제 복도에서 있었던 일 때문인지, 그녀의 눈빛이 묘하게 누그러져 있다."),
            "dialogue": [
                ("세라피나", "...어제 일은 잊을게. 너한테 뭘 기대한 내가 바보였지.", "draco")
                if st.session_state.get("last_mistake") else
                ("세라피나", "...어제 일, 딱히 고마웠던 건 아니야. 그냥 예의상 하는 말이야.", "draco"),
                ("클라라", f"(귓속말로) 세라피나가 먼저 말을 걸다니! {p}, 너 대체 무슨 마법을 쓴 거야?", "hermione")
            ],
            "choices": [
                ("솔직하게 더 친해지고 싶다고 말한다.", {"aff": +8, "tru": +5}, "세라피나가 얼굴을 붉히며 시선을 피합니다."),
                ("'너 사실 츤데레지?' 하고 놀린다.", {"aff": +2, "dist": +2}, "버럭 화를 내더니 계단을 먼저 올라가 버립니다."),
                ("에단한테는 비밀로 하겠다며 웃어 준다.", {"aff": +6, "tru": +10, "clue": +1}, "자기 편이 되어 주는 것 같아 세라피나가 안심합니다.")
            ]
        },
        6: {
            "title": "온실의 비밀",
            "bg": "bg_19 (애시포드 온실)",
            "desc": "주말 오후, 한적한 온실을 둘러보다가 혼자 마법 식물을 정성껏 돌보고 있는 세라피나를 발견했다.",
            "dialogue": [
                ("세라피나", "미리 말해 두는데, 내가 이런 꽃 키우는 거 좋아한다고 서리 기숙사 애들한테 말하면 가만 안 둬.", "draco")
            ],
            "choices": [
                ("새끼손가락을 걸고 비밀을 꼭 지키겠다고 약속한다.", {"aff": +10, "tru": +10}, "세라피나가 손가락을 걸며 수줍게 미소 짓습니다. (비밀을 지키기로 약속했다)", "kept_malfoy_secret"),
                ("의외로 다정한 면이 있다며 웃는다.", {"aff": +5, "tru": +3}, "얼굴이 빨개진 세라피나가 괜히 화분만 만지작거립니다."),
                ("친구들한테 다 말해야겠다며 장난친다.", {"aff": -10, "tru": -10}, "눈가가 붉어진 세라피나가 당장 나가라고 소리칩니다.")
            ]
        },
        7: {
            "title": "불꽃과 서리의 충돌",
            "bg": "bg_11 (애시포드 안뜰)",
            "desc": "안뜰에서 에단과 세라피나가 날 선 말다툼을 벌이고 있다. 세라피나는 가문의 명예를 들먹이고, 에단은 앙숙답게 한 치도 물러서지 않는다.",
            "dialogue": [
                ("에단", f"윈터번, 넌 맨날 남을 깔보기만 하지! {p}까지 괴롭히지 마!", "harry"),
                ("세라피나", "제대로 받아치지도 못하면서 입만 살아 있는 애시비 주제에!", "draco")
            ],
            "choices": [
                ("세라피나 편을 들며 에단을 말린다.", {"aff": +10, "tru": +5}, "세라피나가 놀란 얼굴로 당신을 바라봅니다. 대신 에단과는 조금 서먹해졌습니다.", "defended_draco_public"),
                ("에단 편을 들며 세라피나를 몰아세운다.", {"aff": -10, "tru": -5}, "상처받은 눈빛으로 당신을 노려보던 세라피나가 자리를 떠납니다."),
                ("어느 편도 들지 않고 두 사람을 진정시킨다.", {"aff": +3, "tru": +5}, "소란이 크게 번지지 않고 조용히 마무리됩니다.")
            ]
        },
        8: {
            "title": "봉인 서고의 밤",
            "bg": "bg_07 (도서관 봉인 서고)",
            "desc": "늦은 밤, 도서관 봉인 서고에 몰래 들어갔다가, 촛불 하나를 켜 두고 낡은 책을 살펴보던 세라피나와 딱 마주쳤다.",
            "dialogue": [
                ("세라피나", "꺅! ...너였어? 놀랐잖아. ...여기서 뭐 하는 거야?", "draco")
            ],
            "choices": [
                ("너 찾으러 왔다고 솔직하게 말한다.", {"aff": +12, "tru": +3}, "세라피나가 터질 듯 붉어진 얼굴을 두 손으로 감쌉니다."),
                ("무슨 책인지 같이 들여다본다.", {"aff": +5, "tru": +5, "clue": +1}, "윈터번 가문의 오래된 마법 문양에 대한 단서를 함께 찾아냅니다."),
                ("이러다 선생님께 걸리면 어쩌냐고 걱정한다.", {"aff": +3, "tru": +2}, "잔소리하지 말라며 세라피나가 툴툴거립니다.")
            ]
        },
        9: {
            "title": "달밤의 호숫가",
            "bg": "bg_13 (호숫가)",
            "desc": "저녁 무렵, 안개가 내려앉은 호숫가. 버드나무 아래 혼자 앉아 있는 세라피나에게 다가갔다. 잔잔한 물결 위로 달빛이 일렁인다.",
            "dialogue": [
                ("세라피나", "가끔은 명문 귀족 가문이니, 서리 기숙사의 기대니 하는 것들에서 전부 벗어나고 싶어...", "draco")
            ],
            "choices": [
                ("옆에 앉아 조용히 손을 잡아 준다.", {"aff": +12, "tru": +8}, "손을 빼지 않던 세라피나가 살며시 당신 어깨에 머리를 기댑니다."),
                ("언제든 털어놓으라고 다정하게 말한다.", {"aff": +8, "tru": +10}, "세라피나가 당신을 조금씩 믿기 시작합니다."),
                ("그래도 가문에 대한 책임은 중요하다고 충고한다.", {"aff": -2, "tru": +2}, "너무 현실적인 말에 세라피나가 한숨을 쉬며 일어납니다.")
            ]
        },
        10: {
            "title": "클라라의 조언",
            "bg": "bg_08 (불꽃 기숙사 휴게실)",
            "desc": "기숙사 휴게실 벽난로 앞. 클라라가 걱정스러운 얼굴로 다가와 말을 건넨다.",
            "dialogue": [
                ("클라라", f"{p}, 요즘 세라피나랑 자주 붙어 다니더라. 그 애, 가문의 압박 때문에 속앓이가 심하대. 솔직하고 다정하게 대하는 게 제일 중요해.", "hermione")
            ],
            "choices": [
                ("클라라의 조언을 마음에 새긴다.", {"aff": +5, "tru": +5}, "세라피나의 마음을 이해하는 데 큰 도움이 됩니다.", "hermione_advised"),
                ("내 일은 내가 알아서 하겠다고 한다.", {"aff": 0, "tru": 0}, "클라라는 어깨를 으쓱하고 물러납니다."),
                ("세라피나에 대한 소문을 더 자세히 물어본다.", {"aff": 0, "clue": +1}, "윈터번 가문의 비밀에 대한 단서를 하나 더 얻었습니다.")
            ]
        },
        11: {
            "title": "집에서 온 편지",
            "bg": "bg_04 (애시포드 복도)",
            "desc": "복도 구석에서 부엉이가 물어다 준 편지를 읽던 세라피나의 눈시울이 붉어져 있다. 집에서 온, 엄한 꾸중이 담긴 편지인 것 같다.",
            "dialogue": [
                ("세라피나", "보지 마... 이렇게 우는 모습, 아무한테도 보여 주기 싫었는데...", "draco")
            ],
            "choices": [
                ("아무 말 없이 꼭 안아 준다.", {"aff": +15, "tru": +10}, "굳어 있던 세라피나가 이내 당신 품에 얼굴을 묻고 눈물을 흘립니다."),
                ("손수건을 건네며 다정하게 달래 준다.", {"aff": +10, "tru": +8}, "고개를 숙인 세라피나가 손수건을 꼭 쥡니다."),
                ("무슨 내용인지 보여 달라고 한다.", {"aff": -8, "dist": +5}, "무례하다며 편지를 구겨 쥐고 달려가 버립니다.")
            ]
        },
        12: {
            "title": "빈 교실의 비밀 연습",
            "bg": "bg_17 (빈 교실)",
            "desc": "방과 후 빈 교실에서 세라피나와 단둘이 방어 마법을 연습하기로 했다.",
            "dialogue": [
                ("세라피나", "너랑 단둘이 마법 연습을 하게 될 줄은 몰랐어. ...생각보다 나쁘지 않네.", "draco")
            ],
            "choices": [
                ("지팡이 쥐는 법을 알려 주며 손을 살짝 잡아 준다.", {"aff": +10, "tru": +5}, "얼굴이 새빨개진 세라피나가 주문을 엉뚱하게 외웁니다."),
                ("진지하게 마법 대결에 집중한다.", {"aff": +5, "tru": +8}, "서로의 실력을 인정하며 호흡을 맞춰 갑니다."),
                ("장난치다 지팡이를 놓치고 둘이 함께 넘어진다.", {"aff": +12, "tru": +2}, "숨결이 닿을 만큼 가까운 거리. 서로의 심장 소리가 들릴 것만 같습니다.")
            ]
        },
        13: {
            "title": "에단의 경고",
            "bg": "bg_04 (애시포드 복도)",
            "desc": "에단이 복도에서 당신을 불러 세운다. 요즘 세라피나와 가까워진 당신이 영 못마땅한 표정이다.",
            "dialogue": [
                ("에단", f"{p}, 너 진짜 세라피나 좋아하는 거야? 우리랑 한 내기 때문에 시작한 거잖아. 괜히 일 커지기 전에 그만둬.", "harry")
            ],
            "choices": [
                ("세라피나를 진심으로 좋아한다고 분명히 말한다.", {"aff": +10, "tru": +10}, "에단은 한숨을 쉬면서도 당신의 진심을 인정합니다.", "harry_jealous_event"),
                ("그냥 적당히 친하게 지내는 것뿐이라고 둘러댄다.", {"aff": -5, "tru": -5}, "마침 지나가다 이 말을 들은 세라피나의 표정이 차갑게 식습니다."),
                ("네가 상관할 일 아니라고 쏘아붙인다.", {"aff": 0, "dist": +2}, "에단과 사이가 어색해집니다.")
            ]
        },
        14: {
            "title": "눈 덮인 정원의 저녁",
            "bg": "bg_12 (애시포드 정원)",
            "desc": "달빛이 내려앉은 저녁, 눈 덮인 정원 벤치. 세라피나가 당신 어깨에 기대어 잠시 눈을 감고 있다.",
            "dialogue": [
                ("세라피나", "너랑 있으면... 가문의 기대도, 사람들 시선도 다 잊게 돼.", "draco")
            ],
            "choices": [
                ("머리카락을 부드럽게 쓸어 넘겨 준다.", {"aff": +10, "tru": +8}, "세라피나가 눈을 감은 채 옅게 미소 짓습니다."),
                ("앞으로도 계속 곁에 있겠다고 약속한다.", {"aff": +12, "tru": +10}, "두근거리는 마음을 숨기지 못한 세라피나가 당신 손을 꼭 잡습니다."),
                ("기숙사 들어갈 시간이라며 깨운다.", {"aff": +2, "tru": +2}, "분위기 깬다며 세라피나가 입을 삐죽입니다.")
            ]
        },
        15: {
            "title": "윈터번 가문의 비밀",
            "bg": "bg_24 (고대 마법 서고)",
            "desc": "세라피나가 아무도 없는 고대 마법 서고로 당신을 불러, 가문의 문양이 새겨진 낡은 책을 펼쳐 보인다.",
            "dialogue": [
                ("세라피나", "이건 우리 가문의 비밀 기록이야. 정말 믿는 사람한테만 보여 주는 거야.", "draco")
            ],
            "choices": [
                ("믿어 줘서 고맙다고 진심을 전한다.", {"aff": +10, "tru": +15, "clue": +2}, "세라피나가 당신에게 완전히 마음을 엽니다."),
                ("기록에 담긴 마법을 함께 풀어 본다.", {"aff": +5, "tru": +8, "clue": +1}, "두 사람은 오래된 마법의 비밀을 하나 함께 풀어냅니다."),
                ("절대 다른 사람에게 말하지 않겠다고 약속한다.", {"aff": +8, "tru": +10}, "세라피나가 고개를 끄덕이며 안도합니다.")
            ]
        },
        16: {
            "title": "진눈깨비와 우산",
            "bg": "bg_11 (애시포드 안뜰)",
            "desc": "눈 덮인 안뜰에 갑자기 차가운 진눈깨비가 쏟아진다. 처마 밑에 선 세라피나가 난감한 얼굴로 하늘을 올려다보고 있다.",
            "dialogue": [
                ("세라피나", "하필 지금 진눈깨비라니... 옷 젖는 건 정말 질색인데.", "draco")
            ],
            "choices": [
                ("마법 우산을 펼쳐 세라피나 쪽으로 기울여 씌워 준다.", {"aff": +10, "tru": +5}, "한쪽 어깨가 흠뻑 젖은 당신을 보고 세라피나가 감동한 눈치입니다."),
                ("손을 잡고 진눈깨비 속을 함께 달린다.", {"aff": +8, "tru": +3}, "세라피나가 아이처럼 깔깔 웃습니다."),
                ("진눈깨비가 그칠 때까지 기다리자고 한다.", {"aff": +3, "tru": +2}, "두 사람은 처마 밑에서 조용히 이야기를 나눕니다.")
            ]
        },
        17: {
            "title": "기숙사 앞, 깊은 밤",
            "bg": "bg_09 (서리 기숙사 휴게실)",
            "desc": "밤이 깊었다. 세라피나를 서리 기숙사 지하 휴게실 입구까지 바래다주었다.",
            "dialogue": [
                ("세라피나", "잘 가... 솔직히 말하면, 들어가기 싫어. 너랑 조금만 더 있고 싶어.", "draco")
            ],
            "choices": [
                ("이마에 살며시 입을 맞춘다.", {"aff": +15, "tru": +8}, "얼굴이 새빨개진 세라피나가 이마를 감싸 쥐고 문 안으로 쏙 들어갑니다."),
                ("손을 잡고 조금만 더 밤하늘을 보자고 한다.", {"aff": +10, "tru": +10}, "세라피나가 행복한 얼굴로 손을 놓지 않습니다."),
                ("내일 아침 일찍 보자며 인사한다.", {"aff": +5, "tru": +5}, "세라피나가 아쉬운 듯 고개를 끄덕입니다.")
            ]
        },
        18: {
            "title": "속삭이는 숲의 위기",
            "bg": "bg_20 (속삭이는 숲 입구)",
            "desc": "세라피나가 잃어버린 가문의 은 브로치를 찾으러 함께 속삭이는 숲 입구에 갔다가, 사나운 마법 생물과 맞닥뜨렸다!",
            "dialogue": [
                ("세라피나", "위험해! 내 뒤로 물러서!", "draco")
            ],
            "choices": [
                ("세라피나 앞을 막아서며 대신 공격을 막아 낸다.", {"aff": +15, "tru": +15}, "당신이 다칠까 봐 세라피나의 눈에 눈물이 맺힙니다."),
                ("둘이 완벽하게 호흡을 맞춰 마법 생물을 쫓아낸다.", {"aff": +10, "tru": +10}, "두 사람이 최고의 짝꿍이라는 걸 확인한 순간입니다."),
                ("겁이 나서 뒤로 물러선다.", {"aff": -10, "tru": -10}, "실망한 얼굴로 세라피나가 혼자 주문을 외웁니다.")
            ]
        },
        19: {
            "title": "천문탑의 밤",
            "bg": "bg_15 (천문탑 - 밤)",
            "desc": "별이 쏟아질 듯한 밤, 천문탑 꼭대기. 세라피나와 나란히 서서 밤바람을 맞으며 야경을 내려다본다.",
            "dialogue": [
                ("세라피나", "이렇게 아름답고 평화로운 밤은 처음이야... 다 네 덕분이야.", "draco")
            ],
            "choices": [
                ("너는 저 별보다 더 빛난다고 말한다.", {"aff": +15, "tru": +10}, "세라피나가 수줍게 웃으며 당신에게 살며시 기댑니다."),
                ("너와 함께 있는 시간이 가장 특별하다고 말한다.", {"aff": +12, "tru": +12}, "눈시울이 붉어진 세라피나가 진심 어린 눈빛으로 당신을 바라봅니다."),
                ("바람이 차다며 겉옷을 벗어 덮어 준다.", {"aff": +10, "tru": +8}, "따뜻한 온기에 세라피나가 살며시 기대어 옵니다.")
            ]
        },
        20: {
            "title": "함박눈 오는 날",
            "bg": "bg_18 (애시포드 복도 창가)",
            "desc": f"창밖으로 올겨울 들어 가장 탐스러운 함박눈이 내리기 시작한다. 어제부터 '{p_i} 내기 때문에 세라피나에게 접근했다'는 소문이 돌아 둘 사이가 어색해졌지만, 나란히 눈을 바라보는 지금만큼은 묘한 감정이 차오른다.",
            "dialogue": [
                ("세라피나", "...눈이 펑펑 오네. ...이런 날 너랑 같이 보게 될 줄은 몰랐어.", "draco"),
                ("클라라", f"(멀리서 지켜보며) 이렇게 눈 오는 날엔 세라피나도 마음이 좀 풀릴 거야, {p}. 지금이 기회야!", "hermione")
            ],
            "choices": [
                ("조용히 다가가 목도리를 둘러 주며 다정하게 말을 건넨다.", {"aff": +12, "tru": +10}, "귀 끝까지 빨개진 세라피나가 눈을 피하지만, 미소는 숨기지 못합니다."),
                ("쌓이는 눈처럼 너와의 추억도 하나씩 쌓여 간다고 말한다.", {"aff": +15, "tru": +12}, "세라피나가 두근거리는 가슴을 누르듯 두 손으로 볼을 감쌉니다."),
                ("눈 구경은 그만하고 공부하러 가자고 한다.", {"aff": +3, "tru": +2}, "낭만이라고는 하나도 모른다며 세라피나가 툴툴거립니다.")
            ]
        },
        21: {
            "title": "다시 차가워진 눈빛",
            "bg": "bg_04 (애시포드 복도)",
            "desc": "소문이 점점 커지자, 세라피나는 다시 당신의 눈길을 피하며 예전처럼 차갑게 굴기 시작했다.",
            "dialogue": [
                ("세라피나", "아는 척하지 마. 네 진짜 목적이 뭐였든, 이제 더는 안 속아.", "draco")
            ],
            "choices": [
                ("앞을 가로막고 제발 내 진심을 들어 달라고 한다.", {"aff": +5, "tru": +5}, "차가운 눈빛 너머로 흔들리는 마음이 비칩니다."),
                ("시간을 주고 기다리기로 한다.", {"aff": 0, "tru": +2}, "돌아서는 당신의 뒷모습을 세라피나가 쓸쓸히 바라봅니다."),
                ("억울하다며 화를 낸다.", {"aff": -10, "dist": +10}, "세라피나가 마음의 문을 완전히 닫아 버립니다.")
            ]
        },
        22: {
            "title": "폭풍 전야",
            "bg": "bg_06 (애시포드 도서관)",
            "desc": "도서관 구석에서 세라피나와 마주쳤다. 그녀의 손에는 30일 전 그날 밤, 당신이 친구들과 내기하며 적었던 쪽지가 들려 있다. 내기에 끼었던 친구 하나가 휴게실에 흘린 것을, 서리 기숙사 학생이 주워 그녀에게 가져다준 모양이다.",
            "dialogue": [
                ("세라피나", "이 쪽지... '30일 안에 세라피나 윈터번 꼬시기.' 이거 네 글씨 맞지?", "draco")
            ],
            "choices": [
                ("숨기지 않고 내기였다는 걸 인정한다.", {"aff": 0, "tru": +10}, "상처받았지만, 솔직한 대답에 세라피나가 대화를 이어 갑니다."),
                ("내기 같은 건 아니라고 거짓말한다.", {"aff": -10, "tru": -20}, "거짓말이라는 걸 알아챈 세라피나가 차갑게 비웃습니다."),
                ("처음엔 그랬지만 지금은 진심으로 좋아한다고 호소한다.", {"aff": +10, "tru": +10}, "세라피나의 눈동자가 크게 흔들립니다.")
            ]
        },
        23: {
            "title": "★ 진실의 순간",
            "bg": "bg_18 (애시포드 복도 창가)",
            "desc": "창밖으로 눈보라가 몰아치는 복도. 세라피나가 눈물을 참으며 당신을 똑바로 바라본다.",
            "dialogue": [
                ("세라피나", "처음부터... 날 내기 상대로 이용한 거였어? 내 마음 가지고 장난친 거냐고!", "draco")
            ],
            "choices": [
                ("처음엔 장난이었지만, 진짜 너를 알게 되면서 정말로 좋아하게 됐다고 솔직하게 고백한다.", {"aff": +20, "tru": +20}, "세라피나가 울음을 터뜨리며 당신의 가슴을 콩 칩니다. 진심이 전해졌습니다.", "day23_honest"),
                ("내기 같은 건 처음부터 없었다고 끝까지 잡아뗀다.", {"aff": -30, "tru": -30, "dist": +30}, "세라피나가 당신의 뺨을 때리고 완전히 돌아섭니다.", "day23_defensive"),
                ("미안하다고 사과하며, 네가 원하면 떠나겠다고 한다.", {"aff": -10, "tru": +5}, "세라피나가 당황한 얼굴로 당신을 바라봅니다.")
            ]
        },
        24: {
            "title": "호숫가에서",
            "bg": "bg_13 (호숫가)",
            "desc": "어제 일이 있은 뒤, 호숫가에 홀로 앉아 생각에 잠긴 세라피나를 발견했다.",
            "dialogue": [
                ("세라피나", "...상처받은 건 맞아. 그래도 네 눈빛이 거짓말이 아니라는 건 알아.", "draco") if flags.get("day23_honest")
                else ("세라피나", "...다시는 내 앞에 나타나지 마.", "draco") if flags.get("day23_defensive")
                else ("세라피나", "...지금은 아무 말도 하고 싶지 않아.", "draco")
            ],
            "choices": [
                ("마음이 풀릴 때까지 조용히 곁을 지킨다.", {"aff": +10, "tru": +10}, "닫혔던 마음의 문이 조금씩 다시 열립니다."),
                ("진심을 담은 편지를 건네고 자리를 비켜 준다.", {"aff": +8, "tru": +8}, "세라피나가 편지를 조심스럽게 펼쳐 읽습니다."),
                ("멀리서 지켜보기만 한다.", {"aff": +2, "tru": +2}, "둘 사이의 거리는 좀처럼 좁혀지지 않습니다.")
            ]
        },
        25: {
            "title": "윈터번 가문의 압박",
            "bg": "bg_25 (윈터번 저택)",
            "desc": "윈터번 저택에서 날아온 편지 한 통에 세라피나가 깊은 고민에 빠졌다. 가문이 정해 둔 정략결혼 이야기다.",
            "dialogue": [
                ("세라피나", "우리 집에서 나를 다른 명문 귀족 집안과 정략결혼시키려고 해... 나 어떻게 해야 해?", "draco")
            ],
            "choices": [
                ("무슨 일이 있어도 내가 너를 지키겠다고 말한다.", {"aff": +15, "tru": +15}, "당당한 당신의 모습에 세라피나가 꼭 안겨 옵니다."),
                ("함께 학교를 떠나 도망치자고 한다.", {"aff": +5, "tru": +5}, "세라피나는 현실적인 어려움 앞에서 망설입니다."),
                ("가문의 뜻을 따르는 게 안전할 수도 있다고 말한다.", {"aff": -15, "dist": +10}, "세라피나가 당신에게 깊이 실망합니다.")
            ]
        },
        26: {
            "title": "모두 앞에서의 고백",
            "bg": "bg_03 (애시포드 대연회장)",
            "desc": "전교생이 모인 대연회장. 서리 기숙사 귀족 학생들이 세라피나를 비웃는 가운데, 당신이 자리에서 일어선다.",
            "dialogue": [
                ("세라피나", "(당황하며) 잠깐... 너 지금 뭐 하려는 거야?", "draco")
            ],
            "choices": [
                ("모두가 듣는 앞에서 세라피나를 좋아한다고 당당히 외친다.", {"aff": +20, "tru": +15}, "연회장이 발칵 뒤집히고, 세라피나는 빨개진 얼굴로 미소 짓습니다."),
                ("세라피나의 손을 잡고 연회장을 빠져나간다.", {"aff": +15, "tru": +12}, "두 사람은 둘만의 비밀 산책로로 향합니다."),
                ("조용히 상황을 수습한다.", {"aff": +3, "tru": +3}, "소란은 별일 없이 가라앉습니다.")
            ]
        },
        27: {
            "title": "비밀 아지트의 약속",
            "bg": "bg_22 (오래된 마법 유적)",
            "desc": "학교 지하의 오래된 마법 유적. 둘만의 아지트가 된 이곳에서 세라피나와 앞날을 이야기한다.",
            "dialogue": [
                ("세라피나", "30일이 이렇게 빨리 지나갈 줄 몰랐어. 이제 며칠 안 남았네...", "draco")
            ],
            "choices": [
                ("30일이 지나도, 30년이 지나도 내 마음은 그대로일 거라고 약속한다.", {"aff": +15, "tru": +15}, "세라피나가 수줍게 다가와 당신에게 살짝 입을 맞춥니다."),
                ("너와 함께한 모든 순간이 마법 같았다고 말한다.", {"aff": +10, "tru": +10}, "눈시울이 붉어진 세라피나가 고맙다고 말합니다."),
                ("남은 시간이라도 최선을 다하자고 한다.", {"aff": +5, "tru": +5}, "세라피나가 고개를 끄덕입니다.")
            ]
        },
        28: {
            "title": "세라피나의 편지",
            "bg": "bg_18 (애시포드 복도 창가)",
            "desc": "이른 아침, 부엉이가 은은한 향기가 밴 편지 한 통을 물어다 주었다. 세라피나의 편지다.",
            "dialogue": [
                ("세라피나", f"(편지) '처음엔 너를 경계했어. 네가 나를 내기 상대로 삼았다는 걸 알았을 땐 세상이 무너지는 것 같았고. 그런데 지금 내 마음속엔 온통 너뿐이야, {p}.'", "draco")
            ],
            "choices": [
                ("편지를 가슴에 품고 당장 세라피나에게 달려가 안아 준다.", {"aff": +15, "tru": +15}, "두 사람은 서로의 진심을 완전히 확인합니다."),
                ("변하지 않을 마음을 담아 답장을 보낸다.", {"aff": +10, "tru": +10}, "답장을 받은 세라피나가 하루 종일 미소를 짓습니다."),
                ("편지를 소중히 주머니에 넣는다.", {"aff": +5, "tru": +5}, "기분 좋은 하루가 시작됩니다.")
            ]
        },
        29: {
            "title": "D-1, 약속 전날 밤",
            "bg": "bg_15 (천문탑 - 밤)",
            "desc": "30일째를 하루 앞둔 밤. 천문탑에서 손을 꼭 잡고 은하수를 함께 올려다본다.",
            "dialogue": [
                ("세라피나", "내일이면 딱 30일째야. 넌 나한테 어떤 대답을 해 줄 거야?", "draco")
            ],
            "choices": [
                ("내일 정식으로 사귀자고 말하겠다고 한다.", {"aff": +15, "tru": +15}, "세라피나가 눈물을 글썽이며 고개를 끄덕입니다."),
                ("어떤 시련이 와도 함께 헤쳐 나가겠다고 다짐한다.", {"aff": +12, "tru": +12}, "세라피나가 당신의 손을 더 꼭 쥡니다."),
                ("내일이 오는 게 아쉽다고 말한다.", {"aff": +5, "tru": +5}, "세라피나가 조용히 어깨에 기댑니다.")
            ]
        },
        30: {
            "title": "D-Day, 눈 내리는 천문탑",
            "bg": "bg_14 (천문탑 - 눈 오는 날)",
            "desc": f"운명의 30일째. 학교 전체에 하얀 눈이 소복소복 쌓이는 가운데, 천문탑 위에서 세라피나 윈터번이 {p_eul} 기다리고 있다. 온 세상이 하얗게 반짝인다.",
            "dialogue": [
                ("세라피나", f"눈이 오네... 마지막 날에 이렇게 눈이 올 줄이야. 자, {p}. 30일 동안 나를 꼬시겠다던 그 내기... 이제 대답을 들려줘.", "draco")
            ],
            "choices": [
                ("눈꽃이 내려앉은 세라피나의 손을 꼭 잡고 진심을 고백한다.", {"aff": +15, "tru": +15}, "고백을 들은 세라피나가 숨을 멈춥니다. 눈 내리는 소리만 들리는 가운데, 그녀가 천천히 입을 엽니다—"),
                ("내 마음은 처음부터 끝까지 너를 향해 있었다고 눈을 맞추며 말한다.", {"aff": +12, "tru": +12}, "세라피나가 당신의 눈을 오래도록 바라보다가, 마침내 대답하려 입을 엽니다—"),
                ("말없이 세라피나를 안아 주며 함께 눈 내리는 하늘을 바라본다.", {"aff": +15, "tru": +15}, "말없이 안긴 세라피나가 작게 숨을 고릅니다. 그리고 천천히 입을 엽니다—")
            ]
        }
    }

    return apply_distant(day, story_db.get(day, story_db[30]))


# ==========================================
# 4-1. 장면 잇기: 고른 선택지에 따라 다음 날 장면 맨 위에 나오는 문장
#  NEXT[날짜] = [1번 선택 뒤, 2번 선택 뒤, 3번 선택 뒤]
# ==========================================
NEXT = {
    1: ["당당한 인사에 세라피나는 대꾸 없이 고개를 돌렸지만, 그날 내내 그녀의 시선이 가끔 당신 쪽을 스쳤다. 다음 날, 과제 때문에 들른 도서관에서 다시 그녀를 마주친다.",
        "조용히 물러난 탓에 세라피나는 당신을 금세 잊은 듯했다. 그렇게 하루가 지나고, 과제를 하러 간 도서관에서 뜻밖에 그녀와 다시 마주친다.",
        "비꼬는 미소를 본 세라피나가 친구들 앞에서 '불꽃 기숙사다운 무례함'이라며 당신을 깎아내렸다. 다음 날 도서관, 하필이면 그녀와 또 마주치고 만다."],
    2: ["책을 낚아채 간 세라피나는 사서 몰래 책갈피 하나를 당신 책상에 슬쩍 밀어 두고 갔다. 이튿날 그레이브스 교수의 수업, 짝 배정표에 두 사람의 이름이 나란히 적혀 있다.",
        "사서에게 혼난 뒤 세라피나는 '너 때문에 망신당했잖아'라며 쌀쌀맞게 자리를 떴다. 그리고 다음 날, 하필 수업 짝으로 그녀가 배정된다.",
        "나란히 앉아 책을 읽는 동안, 세라피나는 몇 번이나 당신이 책장을 넘길 때까지 기다려 주었다. 다음 날 연금술 교실에서 두 사람은 같은 조가 된다."],
    3: ["수업 내내 등을 돌린 세라피나는 종이 울리자마자 교실을 빠져나갔다. 다음 날 늦은 오후, 복도를 지나다 창가에 혼자 선 그녀를 발견한다.",
        "완벽하게 끝낸 과제로 두 사람은 반에서 가장 높은 점수를 받았다. '운이 좋았네'라던 세라피나의 표정은 나쁘지 않았다. 그런데 다음 날 오후, 창가의 그녀는 전혀 다른 얼굴을 하고 있었다.",
        "웃음을 참던 세라피나의 얼굴이 머릿속에서 떠나지 않는다. 다음 날 늦은 오후, 복도 창가에서 편지를 쥔 채 서 있는 그녀를 보게 된다."],
    4: ["코코아 컵을 두 손으로 감싼 세라피나는 한참 뒤에야 '...달아'라고 중얼거렸다. 다음 날 아침, 계단에서 그녀와 마주친다.",
        "편지 이야기를 꺼내자 세라피나는 등을 돌려 버렸다. 괜한 말을 했다는 후회 속에 하루가 지나고, 다음 날 계단에서 그녀와 맞닥뜨린다.",
        "해가 질 때까지 두 사람은 아무 말 없이 창밖만 바라보았다. 다음 날 아침, 계단에서 다시 그녀를 만난다."],
    5: ["얼굴을 붉힌 채 계단을 뛰어 올라가던 세라피나가, 꼭대기에서 한 번 뒤를 돌아보았다. 다음 날 오후, 온실 쪽에서 익숙한 백금발이 보인다.",
        "'츤데레'라는 말이 꽤 거슬렸는지, 세라피나는 하루 종일 당신을 투명 인간 취급했다. 그러다 다음 날 오후 들른 온실에서 그녀를 발견한다.",
        "'비밀'이라는 말에 세라피나의 입꼬리가 아주 살짝 올라갔다. 다음 날 오후, 온실에서 그녀의 또 다른 비밀을 마주하게 된다."],
    6: ["새끼손가락을 건 세라피나의 손끝은 차가웠지만, 먼저 놓지는 않았다. 다음 날 안뜰에서 큰 목소리가 들려온다. 에단과 세라피나가 맞붙었다.",
        "괜히 화분만 만지작거리던 세라피나가 '너, 내일 또 와도 돼'라고 작게 말했다. 그런데 다음 날, 안뜰에서 그녀와 에단이 말다툼을 벌이고 있다.",
        "온실에서 쫓겨난 뒤, 서리 기숙사 쪽 분위기가 눈에 띄게 싸늘해졌다. 다음 날 안뜰, 세라피나와 에단의 날 선 목소리가 울려 퍼진다."],
    7: ["에단은 '너 대체 누구 편이야'라며 등을 돌렸고, 세라피나는 저녁 내내 당신 쪽을 힐끔거렸다. 다음 날 밤 잠이 오지 않아, 도서관 봉인 서고로 몰래 숨어든다.",
        "자리를 떠나는 세라피나의 눈가가 젖어 있었던 것 같다. 마음이 무거워 잠들지 못한 밤, 당신은 몰래 도서관 봉인 서고로 향한다.",
        "소동은 가라앉았지만 두 사람 모두 당신에게 서운한 눈치였다. 다음 날 밤, 머리를 식히려 몰래 봉인 서고에 들어간다."],
    8: ["두 손으로 얼굴을 감쌌던 세라피나는 '아무한테도 말하지 마'라는 말만 남기고 사라졌다. 다음 날 저녁, 안개 낀 호숫가에서 그녀를 다시 만난다.",
        "새벽까지 문양을 해독하다 보니, 둘은 어느새 같은 촛불 아래 머리를 맞대고 있었다. 다음 날 저녁, 호숫가 버드나무 아래 그녀가 앉아 있다.",
        "잔소리 그만하라던 세라피나는 결국 당신 말대로 촛불을 끄고 서고를 나왔다. 다음 날 저녁, 호숫가에서 그녀를 다시 발견한다."],
    9: ["세라피나의 머리가 닿았던 어깨가 오래도록 따뜻했다. 다음 날 저녁, 기숙사 휴게실에서 클라라가 조심스레 말을 걸어온다.",
        "'언제든'이라는 말을 세라피나는 몇 번이나 되뇌었다. 둘이 함께 있는 모습을 본 클라라가 다음 날 휴게실에서 당신을 불러 세운다.",
        "현실적인 충고에 세라피나는 '너도 결국 다른 사람들이랑 똑같네'라며 자리를 떴다. 다음 날 저녁, 그 모습을 멀리서 본 클라라가 당신을 찾아온다."],
    10: ["클라라의 말을 곱씹으며 잠든 다음 날, 복도 구석에서 부엉이 한 마리가 세라피나에게 편지를 떨어뜨리는 것을 본다.",
         "클라라는 더 말하지 않았다. 다음 날, 복도 구석에서 편지를 읽던 세라피나의 어깨가 떨리고 있다.",
         "클라라에게 들은 윈터번 가문의 엄격한 가훈이 마음에 걸린다. 바로 다음 날, 그 집에서 온 편지를 든 세라피나를 복도에서 마주친다."],
    11: ["한참을 울던 세라피나는 '이번 한 번만이야'라며 눈가를 닦았다. 다음 날, 그녀가 먼저 빈 교실에서 방어 마법 연습을 같이 하자고 했다.",
         "손수건은 다음 날 깨끗하게 접힌 채 돌아왔다. 그 안에는 '방과 후, 빈 교실'이라고 적힌 쪽지가 끼워져 있었다.",
         "편지를 구겨 쥔 세라피나는 하루 종일 당신을 피했다. 그러다 다음 날, 방어 마법 실습 짝이 정해지면서, 빈 교실에 둘만 남게 된다."],
    12: ["엉뚱한 주문 때문에 교실 커튼이 분홍색으로 변했고, 세라피나는 다음 날까지 당신과 눈도 못 마주쳤다. 그 모습을 본 에단이 복도에서 당신을 불러 세운다.",
         "연습이 끝나고 세라피나가 '다음 주에도'라고 말했다. 그런데 빈 교실을 나서는 두 사람을 에단이 지켜보고 있었다.",
         "넘어진 채 마주 본 몇 초가 영원 같았다. 서둘러 교실을 나서는데, 복도 끝에서 에단이 굳은 얼굴로 당신을 기다리고 있다."],
    13: ["에단은 '네 진심이면 됐어'라며 어깨를 툭 쳤다. 다음 날 저녁, 눈 덮인 정원 벤치에서 세라피나를 만난다.",
         "그 말을 들은 세라피나는 아무 말 없이 지나갔다. 하지만 다음 날 저녁, 정원 벤치에 앉은 그녀는 마치 당신을 기다린 것처럼 보였다.",
         "에단과는 어색해졌지만, 다음 날 저녁 눈 덮인 정원 벤치에서 세라피나가 옆자리를 툭툭 두드렸다."],
    14: ["머리카락을 넘겨 주자 세라피나가 '...보여 주고 싶은 게 있어'라고 속삭였다. 다음 날, 그녀가 당신을 고대 마법 서고로 데려간다.",
         "'계속'이라는 말에 세라피나는 오래 고민하는 얼굴이었다. 그리고 다음 날, 아무에게도 보여 준 적 없는 것을 보여 주겠다며 당신을 고대 서고로 부른다.",
         "투덜거리며 돌아가던 세라피나가 '내일 고대 서고로 와. 늦지 마'라고 말했다."],
    15: ["서고를 나서며 세라피나는 처음으로 먼저 당신의 소매를 잡았다. 다음 날, 안뜰을 지나던 중 하늘에서 진눈깨비가 쏟아진다.",
         "풀어낸 문양은 '서리 아래 피는 붉은 꽃', 포인센티아를 가리키고 있었다. 그 뜻을 곱씹으며 안뜰을 걷던 날, 진눈깨비가 쏟아지기 시작한다.",
         "약속의 표시로 세라피나는 작은 은 단추 하나를 건넸다. 다음 날 안뜰, 처마 밑에서 하늘을 원망하는 그녀를 발견한다."],
    16: ["젖은 어깨를 마법으로 말려 주던 세라피나가 '바보 아니야?'라며 웃었다. 다음 날 밤, 그녀를 서리 기숙사 입구까지 바래다주기로 한다.",
         "흠뻑 젖은 채 깔깔 웃던 세라피나는 '감기 걸리면 네 책임이야'라고 했다. 다음 날 밤 늦게, 그녀를 기숙사 입구까지 데려다준다.",
         "처마 밑에서 나눈 이야기는 밤이 깊을 때까지 이어졌다. 결국 당신은 그녀를 서리 기숙사 입구까지 바래다준다."],
    17: ["문 안으로 사라진 세라피나에게서 다음 날 아침 부엉이 편지가 왔다. '숲 근처에서 가문의 브로치를 잃어버렸어. 같이 찾아 줄래?'",
         "별을 세다 보니 통금 시간을 훌쩍 넘겼다. 다음 날, 세라피나가 숲 근처에서 잃어버린 가문의 브로치를 같이 찾아 달라고 부탁한다.",
         "아쉬운 듯 고개를 끄덕이던 세라피나가 다음 날 아침 먼저 찾아왔다. 숲 근처에서 잃어버린 가문의 브로치를 같이 찾아 달라는 부탁이었다."],
    18: ["팔의 상처에 붕대를 감아 주며 세라피나는 몇 번이나 '다신 그러지 마'라고 했다. 다음 날 밤, 붕대 감은 팔이 걱정된다며 그녀가 천문탑으로 당신을 부른다.",
         "브로치를 되찾은 세라피나가 '우린 꽤 괜찮은 짝이야'라며 웃었다. 다음 날 밤, 둘은 축하 삼아 천문탑에 오른다.",
         "'괜찮아, 무서울 수도 있지.' 세라피나의 목소리는 차가웠다. 다음 날 밤 천문탑, 어색함을 풀 기회가 찾아온다."],
    19: ["세라피나가 기대 온 순간, 계단 아래에서 누군가 '내기'라고 속삭이는 소리가 들렸다. 다음 날부터, 학교에 이상한 소문이 돌기 시작한다.",
         "그 말 뒤의 침묵이 따뜻했다. 하지만 다음 날부터 복도에는 '그 말도 내기 때문'이라는 수군거림이 떠돌기 시작한다.",
         "겉옷 속에서 세라피나가 '너한테서 눈 냄새가 나'라며 웃었다. 그 행복은 오래가지 않았다. 다음 날, 학교에 묘한 소문이 퍼지기 시작한다."],
    20: ["목도리를 두른 세라피나가 웃었지만, 다음 날 아침 서리 기숙사 친구들이 그녀를 둘러싸고 귓속말을 했다. 그날부터 그녀가 당신을 피하기 시작한다.",
         "그 말에 세라피나는 대답 대신 눈을 감았다. 그러나 이튿날, 소문은 '내기 쪽지가 있다'는 이야기로까지 번졌다.",
         "툴툴거리는 세라피나와 공부하러 간 사이, 소문은 걷잡을 수 없이 커졌다. 다음 날, 그녀의 눈빛이 다시 얼어붙어 있었다."],
    21: ["당신을 밀치고 지나간 세라피나의 책상 위에, 그날 밤 누군가 낡은 쪽지 하나를 올려 두었다.",
         "기다리는 사이, 누군가 내기하던 날 밤 당신이 적었던 쪽지를 찾아내 세라피나에게 건넸다.",
         "화를 낸 다음 날, 잃어버린 줄 알았던 내기 쪽지가 세라피나 손에 들어갔다는 이야기를 듣는다."],
    22: ["'솔직하네'라는 말을 남기고 떠난 세라피나는 다음 날, 눈보라 치는 복도에서 당신을 기다리고 있었다. 마지막으로 묻겠다는 얼굴이었다.",
         "거짓말을 들은 세라피나는 쪽지를 구겨 버렸다. 그리고 다음 날, 눈보라가 몰아치는 복도에서 마지막으로 당신을 불러 세운다.",
         "흔들리던 세라피나는 '하루만 생각할게'라고 했다. 다음 날, 눈보라 치는 복도 창가에서 그녀가 대답 대신 질문을 던진다."],
    23: ["울음을 그친 세라피나는 '조금만 시간을 줘'라고 했다. 이튿날, 호숫가에 홀로 앉은 그녀를 발견한다.",
         "얼얼한 뺨보다 등을 돌린 세라피나의 뒷모습이 더 아팠다. 다음 날, 그래도 발걸음은 호숫가로 향한다.",
         "'떠나겠다'는 말에 세라피나는 대답하지 못했다. 다음 날, 호숫가에서 생각에 잠긴 그녀를 본다."],
    24: ["해 질 녘까지 곁을 지키자, 세라피나가 '고마워'라고 작게 말했다. 그런데 다음 날, 윈터번 저택에서 그녀를 뒤흔드는 편지 한 통이 날아든다.",
         "편지를 다 읽은 세라피나가 멀리서 당신 쪽으로 고개를 끄덕였다. 그 무렵, 집에서 온 편지 한 통이 그녀를 다시 흔들어 놓는다.",
         "멀리서 지켜보는 사이 하루가 지났다. 그리고 세라피나에게 집에서 무거운 편지 한 통이 도착한다."],
    25: ["품에 안긴 세라피나가 '정말이지?'라고 몇 번이나 물었다. 다음 날, 정략결혼 소문이 퍼진 대연회장에서 서리 기숙사 귀족 학생들이 그녀를 비웃기 시작한다.",
         "도망치자는 말에 세라피나는 쓸쓸하게 웃었다. 다음 날 대연회장, 정략결혼 소문을 들은 학생들이 그녀를 놀려 댄다.",
         "실망한 세라피나는 혼자 저녁을 먹으러 갔다. 그리고 대연회장에서 정략결혼을 비웃는 소리가 그녀를 향해 쏟아진다."],
    26: ["연회장의 소란이 가라앉은 뒤, 세라피나가 당신을 학교 지하의 오래된 유적으로 이끌었다. '여긴 아무도 몰라. 우리 둘만의 장소야.'",
         "비밀 산책로 끝에서 세라피나가 오래된 유적으로 내려가는 계단을 보여 주었다. 그날부터 그곳은 둘만의 아지트가 되었다.",
         "조용히 수습한 당신에게 세라피나는 '...그래도 고마워'라고 했다. 다음 날, 그녀가 학교 지하의 오래된 유적으로 당신을 부른다."],
    27: ["입맞춤 뒤, 세라피나는 '이건 내기랑 상관없어'라며 웃었다. 다음 날 이른 아침, 부엉이 한 마리가 창문을 두드린다.",
         "아지트를 나서며 세라피나가 '내일 아침, 창문 열어 둬'라고 말했다.",
         "고개를 끄덕이던 세라피나는 무언가 결심한 얼굴이었다. 다음 날 아침, 그녀의 편지가 도착한다."],
    28: ["아침부터 달려온 당신을 세라피나는 꼭 안아 주었다. 그리고 30일째를 하루 앞둔 밤, 둘은 다시 천문탑에 오른다.",
         "답장을 받은 세라피나가 하루 종일 웃는 바람에 서리 기숙사 친구들이 수군거렸다. 다음 날 밤, 천문탑에서 그녀가 기다린다.",
         "편지를 넣은 주머니가 하루 종일 따뜻했다. 다음 날 밤, 30일째를 하루 앞두고 천문탑으로 향한다."],
    29: ["'내일'이라는 약속을 품고 내려온 밤, 첫눈 같은 함박눈이 내리기 시작했다.",
         "꼭 쥔 손을 놓지 않은 채 밤이 지나고, 마침내 30일째 아침이 밝았다.",
         "어깨에 기댄 세라피나의 숨소리를 들으며 마지막 밤이 저물었다."],
}


# ==========================================
# 4-2. 함정 선택지
#  (날짜, 선택지 번호 0~2) → 함정
#   lv   : 2 = 보통·어려움에서 함정 / 3 = 어려움에서만 함정
#   need : 이 조건을 넘으면 함정이 풀림 (관계가 충분히 깊으면 적극적인 행동도 통함)
#          없으면 그 난이도에서는 항상 함정
#   s / r / next : 함정에 걸렸을 때의 수치 변화 / 결과 메시지 / 다음 장면으로 잇는 문장
# ==========================================
TRAPS = {
    (2, 2): {"lv": 3, "s": {"aff": -4, "dist": +3},
             "r": "'누가 너랑 같이 본대?' 세라피나가 책을 탁 덮고 다른 테이블로 가 버립니다. 아직 그럴 사이가 아니었어요.",
             "next": "'친한 척하지 마'라는 말이 귓가에 맴돈다. 다음 날 연금술 교실, 하필 그녀와 같은 조가 된다."},
    (3, 2): {"lv": 2, "s": {"aff": -6, "tru": -2},
             "r": "장난을 거는 순간 재료가 엎질러졌고, 그레이브스 교수가 두 사람 모두 감점했습니다. 성적에 예민한 세라피나가 이를 갈아요.",
             "next": "감점된 점수표를 노려보던 세라피나는 종이 울리자마자 나가 버렸다. 다음 날 늦은 오후, 복도 창가에서 그녀를 다시 본다."},
    (4, 0): {"lv": 3, "s": {"aff": -5, "tru": -3},
             "r": "'동정하는 거야? 필요 없어.' 자존심이 상한 세라피나가 코코아를 창턱에 내려놓고 가 버립니다.",
             "next": "창턱에 남겨진 코코아가 식어 가는 걸 보며 하루가 저물었다. 다음 날 아침, 계단에서 그녀와 마주친다."},
    (5, 0): {"lv": 3, "need": {"tru": 30}, "s": {"aff": -3, "dist": +4},
             "r": "'갑자기 왜 이래? 무슨 꿍꿍이야?' 너무 빨리 다가간 탓에 세라피나가 오히려 경계합니다.",
             "next": "'꿍꿍이'라는 말이 마음에 걸린 채 하루를 보냈다. 다음 날 오후, 온실에서 그녀를 발견한다."},
    (6, 1): {"lv": 2, "s": {"aff": -4, "tru": -3},
             "r": "'의외'라는 말에 세라피나의 얼굴이 굳습니다. '내가 다정한 게 그렇게 웃겨?' 놀리는 말로 들렸나 봐요.",
             "next": "온실 문이 쾅 닫혔다. 다음 날 안뜰에서는 세라피나와 에단의 다툼이 벌어지고 있다."},
    (7, 0): {"lv": 3, "need": {"tru": 35}, "s": {"aff": -5, "tru": -4},
             "r": "'내가 네 도움이 필요해 보여?' 서리 기숙사 애들 앞에서 불꽃 기숙사 학생에게 감싸지는 꼴이 되자, 세라피나가 오히려 모욕감을 느낍니다.",
             "next": "에단에게는 서운하다는 말을, 세라피나에게는 '참견 마'라는 말을 들은 날. 다음 날 밤에도 잠이 오지 않아, 봉인 서고로 숨어든다."},
    (8, 0): {"lv": 2, "need": {"aff": 40}, "s": {"aff": -6, "tru": -4, "dist": +4},
             "r": "'날 찾으러 왔다고? 이 한밤중에? ...소름 돋아.' 아직 그럴 사이가 아닌데 너무 앞서 나갔어요.",
             "next": "'다시는 뒤 밟지 마'라는 말과 함께 촛불이 꺼졌다. 다음 날 저녁, 호숫가에서 그녀를 다시 마주친다."},
    (9, 0): {"lv": 2, "need": {"aff": 45}, "s": {"aff": -5, "tru": -3},
             "r": "세라피나가 손을 홱 빼냅니다. '누가 손 잡아도 된대?' 속마음을 털어놓던 분위기가 단번에 깨졌어요.",
             "next": "그날 뒤로 세라피나는 당신을 피했다. 그 모습을 본 클라라가 다음 날 휴게실에서 말을 건넨다."},
    (11, 0): {"lv": 3, "need": {"tru": 50}, "s": {"aff": -4, "tru": -6},
              "r": "갑작스러운 포옹에 세라피나가 당신을 밀어냅니다. '우는 걸 들킨 것도 싫은데... 이러지 마.' 아직 그만큼 믿지는 않았나 봐요.",
              "next": "밀려난 손이 허공에 머문 채 하루가 지났다. 다음 날, 방어 마법 실습에서 하필 둘이 짝이 된다."},
    (12, 0): {"lv": 2, "s": {"aff": -6, "tru": -2},
              "r": "'지금 나한테 지팡이 쥐는 법을 가르치겠다고?' 학년 수석인 세라피나의 자존심을 정면으로 건드렸어요.",
              "next": "'가르치려 드는 사람은 질색이야.' 세라피나는 연습을 일찍 끝냈다. 교실을 나서자 에단이 당신을 기다리고 있다."},
    (12, 2): {"lv": 3, "need": {"aff": 55}, "s": {"aff": -5, "dist": +5},
              "r": "넘어지자마자 세라피나가 벌떡 일어나 옷을 털어 냅니다. '장난도 정도껏 해.' 아직 그런 장난을 받아 줄 사이가 아니었어요.",
              "next": "어색하게 교실을 나서는데, 복도 끝에서 에단이 굳은 얼굴로 당신을 부른다."},
    (14, 0): {"lv": 3, "s": {"aff": -3, "tru": -3},
              "r": "세라피나가 눈을 번쩍 뜹니다. '머리는 건드리지 마. 땋는 데 한 시간 걸렸단 말이야.' 그녀가 제일 아끼는 머리였어요.",
              "next": "흐트러진 머리를 다시 땋는 세라피나 옆에서 한참을 사과했다. 다음 날, 그래도 그녀는 고대 서고로 당신을 부른다."},
    (16, 1): {"lv": 2, "s": {"aff": -6, "tru": -2},
              "r": "옷 젖는 건 질색이라고 방금 말했는데! 흠뻑 젖은 세라피나가 이를 딱딱 부딪치며 당신을 노려봅니다.",
              "next": "기숙사까지 걸어가는 내내 세라피나는 한마디도 하지 않았다. 그래도 입구 앞에서 그녀가 걸음을 멈춘다."},
    (17, 0): {"lv": 2, "need": {"aff": 65, "tru": 55}, "s": {"aff": -6, "tru": -5, "dist": +5},
              "r": "세라피나가 한 걸음 물러섭니다. '...너무 빨라. 우리가 그런 사이야?' 문이 차갑게 닫혀요.",
              "next": "닫힌 문 앞에 한참을 서 있었다. 다음 날, 세라피나가 사무적인 말투로 숲 근처에서 잃어버린 브로치를 같이 찾아 달라고 한다."},
    (18, 0): {"lv": 3, "s": {"aff": +4, "tru": -6},
              "r": "공격을 대신 맞은 당신을 보고 세라피나가 소리칩니다. '내 뒤로 물러서라고 했잖아! 내 말은 귓등으로도 안 들어?' 자기를 못 믿은 걸로 느꼈나 봐요.",
              "next": "붕대를 감아 주면서도 세라피나는 화가 풀리지 않았다. 다음 날, 그녀가 천문탑에서 이야기 좀 하자고 한다."},
    (19, 0): {"lv": 2, "s": {"aff": -3, "dist": +3},
              "r": "세라피나가 풉 하고 웃음을 터뜨립니다. '그런 싸구려 대사는 어디서 배웠어?' 분위기가 와장창 깨졌어요.",
              "next": "웃음은 금방 그쳤지만 어색함은 남았다. 그리고 다음 날부터, 학교에 묘한 소문이 퍼지기 시작한다."},
    (20, 1): {"lv": 3, "need": {"tru": 60}, "s": {"aff": -4, "tru": -6},
              "r": "소문이 도는 와중의 달콤한 말은 오히려 의심을 키웁니다. '그것도 내기의 일부야?' 세라피나의 눈빛이 식어요.",
              "next": "의심 어린 눈빛을 남긴 채 세라피나가 돌아섰다. 다음 날, 소문은 더 커져 있었다."},
    (21, 0): {"lv": 3, "s": {"aff": -5, "tru": -4, "dist": +5},
              "r": "복도 한가운데서 앞을 가로막자 구경꾼이 몰려듭니다. 구경거리가 된 세라피나가 이를 악물고 당신을 밀치고 지나가요.",
              "next": "구경꾼들 사이로 사라진 세라피나의 책상 위에, 그날 밤 누군가 낡은 쪽지 하나를 올려 두었다."},
    (25, 1): {"lv": 2, "s": {"aff": -5, "tru": -5},
              "r": "'도망? 그게 네 대답이야?' 가족을 다 버리라는 말이 세라피나에겐 무책임하게 들렸어요.",
              "next": "실망한 세라피나가 혼자 걸어간 다음 날, 대연회장에 정략결혼 소문이 퍼진다."},
    (26, 0): {"lv": 3, "need": {"tru": 70}, "s": {"aff": -6, "tru": -6, "dist": +6},
              "r": "연회장이 웃음바다가 됩니다. 가문의 눈과 귀가 가득한 곳에서 구경거리가 된 세라피나가 얼굴을 가리고 뛰쳐나가요.",
              "next": "그날 밤 늦게, 눈이 퉁퉁 부은 세라피나가 학교 지하 유적에서 당신을 기다리고 있었다. '...할 말 있어.'"},
    (30, 2): {"lv": 3, "s": {"aff": -5, "tru": -5},
              "r": "세라피나가 당신을 살며시 밀어냅니다. '...대답을 들려 달라고 했잖아. 끝까지 말로는 안 해 줄 거야?'"},
}


# ==========================================
# 4-3. 이어지는 선택지: 어제 무엇을 골랐는지에 따라 오늘 '↪' 선택지가 하나 더 생김
#  FOLLOW[(어제 날짜, 어제 고른 번호 0~2)] = 오늘 나오는 추가 선택지
#  어제 함정에 걸렸다면 대신 APOLOGY(사과하기) 선택지가 나옴
#  t: 선택지 글 / s: 수치 / r: 결과 메시지 / next: 다음 장면으로 잇는 문장
#  flag: 얻는 플래그 / trap: 이 선택지 자체의 함정 (TRAPS와 같은 모양)
# ==========================================
def F(t, s, r, next="", flag=None, trap=None):
    return {"t": t, "s": s, "r": r, "next": next, "flag": flag, "trap": trap}


FOLLOW = {
    # Day 1 → Day 2 (도서관)
    (1, 0): F("어제 인사를 기억하냐고 웃으며 묻는다.", {"aff": +6, "tru": +2},
              "'그런 걸 왜 기억해.' 그렇게 말하면서도 세라피나가 책에서 손을 떼고 자리를 비켜 줍니다.",
              "책을 사이에 두고 오간 몇 마디가 생각보다 길게 이어졌다. 다음 날, 연금술 교실에서 그녀와 같은 조가 된다."),
    (1, 1): F("어제 피한 게 마음에 걸려, 이번엔 먼저 이름을 밝히며 인사한다.", {"aff": +5, "tru": +3},
              "'...어제는 도망치더니.' 세라피나가 당신의 이름을 한 번 작게 따라 말합니다.",
              "이름이 불렸다는 것만으로 하루 종일 기분이 이상했다. 다음 날, 연금술 교실에서 그녀와 같은 조가 된다."),
    (1, 2): F("어제 비꼰 일을 먼저 사과한다.", {"aff": +4, "tru": +6},
              "세라피나가 의외라는 듯 눈썹을 올립니다. '불꽃 기숙사도 사과할 줄은 아네.'",
              "사과 한마디에 세라피나의 말투가 아주 조금 부드러워졌다. 다음 날, 연금술 교실에서 그녀와 같은 조가 된다."),
    # Day 2 → Day 3 (연금술 수업)
    (2, 0): F("어제 그 책 다 읽었냐고 묻는다.", {"aff": +6, "tru": +3},
              "'당연하지.' 세라피나가 책에서 본 재료 손질법을 은근히 자랑하며 알려 줍니다.",
              "어제의 책 덕분에 둘은 의외로 손발이 잘 맞았다. 다음 날 늦은 오후, 복도 창가에서 혼자 선 그녀를 본다."),
    (2, 1): F("어제 도서관에서 소란 피운 걸 사과하고, 재료 손질을 도맡겠다고 한다.", {"aff": +5, "tru": +5},
              "'...좋아. 대신 하나라도 틀리면 끝이야.' 세라피나가 마지못해 칼을 건넵니다.",
              "실수 하나 없이 재료를 손질하자 세라피나의 잔소리가 조금씩 줄었다. 다음 날 늦은 오후, 복도 창가에서 그녀를 다시 본다."),
    (2, 2): F("어제처럼 같이 보자며 교과서를 가운데 펼친다.", {"aff": +7, "tru": +3},
              "세라피나가 '이번만이야'라며 교과서를 당신 쪽으로 조금 밀어 줍니다.",
              "같은 페이지를 들여다본 지 이틀째, 어색함이 조금 덜했다. 다음 날 늦은 오후, 복도 창가에서 그녀를 다시 본다."),
    # Day 3 → Day 4 (창가의 편지)
    (3, 0): F("어제 수업 때 에단 편을 든 건 미안했다고 먼저 말한다.", {"aff": +5, "tru": +6},
              "'...알면 됐어.' 창밖을 보던 세라피나가 고개를 아주 조금 당신 쪽으로 돌립니다.",
              "사과를 받은 세라피나는 편지를 주머니에 넣으며 '오늘은 그냥 그런 날'이라고만 했다. 다음 날 아침, 계단에서 그녀와 마주친다."),
    (3, 1): F("어제 받은 최고 점수 얘기를 꺼내며 '우리 꽤 잘 맞지?' 하고 웃는다.", {"aff": +4, "tru": +2},
              "세라피나가 피식 웃습니다. '운이 좋았던 거야.'",
              "점수 얘기로 잠깐 웃었지만, 그녀 손의 편지가 계속 마음에 걸렸다. 다음 날 아침, 계단에서 그녀와 마주친다.",
              trap={"lv": 2, "s": {"aff": -4, "tru": -2},
                    "r": "'지금 점수 얘기가 하고 싶어?' 눈치 없는 말에 세라피나가 편지를 꽉 움켜쥡니다.",
                    "next": "눈치 없던 한마디가 하루 종일 마음에 걸렸다. 다음 날 아침, 계단에서 그녀와 마주친다."}),
    (3, 2): F("어제처럼 살짝 웃긴 표정을 지어 보인다.", {"aff": +5, "tru": +2},
              "참으려던 웃음이 새어 나오며 세라피나의 굳은 얼굴이 조금 풀립니다.",
              "그녀가 잠깐이라도 웃었다는 게 다행이었다. 다음 날 아침, 계단에서 그녀와 마주친다."),
    # Day 4 → Day 5 (계단)
    (4, 0): F("코코아 맛은 괜찮았냐고 묻는다.", {"aff": +7, "tru": +3},
              "'...너무 달았어. 다음엔 덜 달게 해.' 다음이 있다는 뜻이었습니다.",
              "'다음엔'이라는 말이 이상하게 오래 남았다. 다음 날 오후, 온실 쪽에서 익숙한 백금발이 보인다."),
    (4, 1): F("어제 편지 얘기는 꺼내지 말았어야 했다고 사과한다.", {"aff": +4, "tru": +7},
              "세라피나가 잠시 멈칫하더니 '...다신 묻지 마'라고 하고는 계단을 나란히 걸어 내려갑니다.",
              "다시 묻지 않겠다는 약속이 둘 사이의 작은 규칙이 되었다. 다음 날 오후, 온실에서 그녀를 발견한다."),
    (4, 2): F("어제처럼 말없이, 그녀 옆 계단에 잠깐 같이 선다.", {"aff": +5, "tru": +6},
              "세라피나가 '또 그거야?'라며 툴툴대지만 먼저 자리를 뜨지는 않습니다.",
              "말없이 함께 있는 게 둘만의 인사처럼 되어 갔다. 다음 날 오후, 온실에서 그녀를 발견한다."),
    # Day 5 → Day 6 (온실)
    (5, 0): F("'친해지자'던 어제 말의 증거라며 꽃에 물 주는 걸 돕겠다고 한다.", {"aff": +7, "tru": +5},
              "세라피나가 물뿌리개를 내밀며 '잎에 직접 뿌리면 가만 안 둬'라고 경고합니다.",
              "흙 묻은 손으로 함께 물을 준 오후였다. 다음 날, 안뜰에서 세라피나와 에단의 말다툼이 벌어진다."),
    (5, 1): F("어제 '츤데레'라고 놀린 걸 사과한다.", {"aff": +4, "tru": +5},
              "'...두 번 다시 그 단어 쓰지 마.' 그래도 세라피나는 온실 문을 닫지 않았습니다.",
              "금지어가 하나 생겼지만, 대신 온실 문은 열려 있었다. 다음 날, 안뜰에서 세라피나와 에단의 말다툼이 벌어진다."),
    (5, 2): F("'비밀이 하나 더 늘었네' 하고 웃는다.", {"aff": +6, "tru": +7},
              "세라피나가 입술을 삐죽이며 '네가 비밀 지키는 거 보고 판단할 거야'라고 합니다.",
              "둘만의 비밀이 하나, 둘 쌓여 갔다. 다음 날, 안뜰에서 세라피나와 에단의 말다툼이 벌어진다."),
    # Day 6 → Day 7 (안뜰 다툼)
    (6, 0): F("온실 일은 입 밖에도 내지 않고, 둘 사이에 조용히 끼어들어 말린다.", {"aff": +7, "tru": +7},
              "당신의 눈짓을 알아챈 세라피나가 말끝을 흐립니다. 다툼이 금세 잦아들어요.",
              "비밀을 지키며 다툼을 말린 당신을 보고 세라피나가 작게 고개를 끄덕였다. 다음 날 밤, 잠이 오지 않아 봉인 서고로 숨어든다."),
    (6, 1): F("'다정한 사람이 왜 이렇게 날을 세워?' 하고 세라피나에게 묻는다.", {"aff": +3, "tru": +1},
              "세라피나가 얼굴을 붉히며 '시끄러워'라고 하고는 다툼에서 빠져나옵니다.",
              "다툼은 흐지부지 끝났다. 다음 날 밤, 잠이 오지 않아 봉인 서고로 숨어든다."),
    (6, 2): F("에단 앞에서, 어제 온실 일은 농담이었다고 세라피나에게 분명히 말한다.", {"aff": +5, "tru": +6},
              "세라피나가 당신을 노려보다가 '...두고 볼 거야'라며 칼끝 같던 목소리를 거둡니다.",
              "농담이었다는 말을 믿어 줄지는 아직 알 수 없었다. 다음 날 밤, 머리를 식히러 봉인 서고로 향한다."),
    # Day 7 → Day 8 (봉인 서고)
    (7, 0): F("'낮에 편들어 준 거, 고맙단 말 들으러 온 건 아니야'라고 농담한다.", {"aff": +7, "tru": +3},
              "세라피나가 촛불 너머로 웃음을 참습니다. '...그래, 고마웠어. 됐지?'",
              "고맙다는 말 한마디에 밤 서고의 공기가 따뜻해졌다. 다음 날 저녁, 호숫가에서 그녀를 다시 만난다."),
    (7, 1): F("낮에 에단 편만 든 걸 사과하러 찾아왔다고 말한다.", {"aff": +5, "tru": +6},
              "세라피나가 책을 덮습니다. '...여기까지 사과하러 온 거야? 바보 같아.'",
              "밤늦게 찾아온 사과는 생각보다 효과가 있었다. 다음 날 저녁, 호숫가에서 그녀를 다시 만난다."),
    (7, 2): F("낮의 소동 얘기는 꺼내지 않고 촛불 하나를 더 켜 준다.", {"aff": +4, "tru": +4},
              "환해진 책장 위로 세라피나가 '눈치는 있네'라고 중얼거립니다.",
              "말 대신 켜 준 촛불이 둘 사이를 조금 밝혀 주었다. 다음 날 저녁, 호숫가에서 그녀를 다시 만난다."),
    # Day 8 → Day 9 (호숫가)
    (8, 0): F("어젯밤 일은 아무한테도 말하지 않았다고 먼저 안심시킨다.", {"aff": +5, "tru": +8},
              "세라피나가 작게 웃습니다. '...알아. 소문이 안 났으니까.'",
              "지켜진 비밀 하나가 세라피나를 조금 더 솔직하게 만들었다. 다음 날, 클라라가 휴게실에서 말을 건넨다."),
    (8, 1): F("어젯밤 찾은 문양 얘기를 꺼내며, 가문이 정말 그렇게 무섭냐고 묻는다.", {"aff": +4, "tru": +5},
              "세라피나가 물수제비를 뜨며 처음으로 가문의 엄격한 가훈 이야기를 조금 들려줍니다.",
              "가문 이야기를 털어놓은 뒤 세라피나의 얼굴이 조금 가벼워 보였다. 다음 날, 클라라가 휴게실에서 말을 건넨다.",
              trap={"lv": 3, "s": {"aff": -3, "tru": -4},
                    "r": "'오늘은 가문 얘기 하기 싫다고 했잖아.' 세라피나가 등을 돌립니다.",
                    "next": "괜한 질문에 다시 벽이 생긴 것 같았다. 다음 날, 클라라가 휴게실에서 말을 건넨다."}),
    (8, 2): F("어젯밤처럼, 너무 늦게까지 혼자 있지 말라고 걱정해 준다.", {"aff": +5, "tru": +4},
              "'또 잔소리.' 그래도 세라피나는 당신이 기숙사로 돌아갈 때까지 함께 걸어 줍니다.",
              "잔소리라던 말과 달리 그녀는 끝까지 함께 걸었다. 다음 날, 클라라가 휴게실에서 말을 건넨다."),
    # Day 9 → Day 10 (클라라의 조언)
    (9, 0): F("클라라에게 어젯밤 세라피나와 손을 잡았다고 털어놓는다.", {"aff": +3, "tru": +3},
              "클라라가 놀라면서도 '그럼 더더욱 조심해서 다가가'라며 진지하게 조언해 줍니다.",
              "클라라의 조언이 머릿속을 맴돌았다. 다음 날, 복도 구석에서 편지를 든 세라피나를 본다.",
              trap={"lv": 3, "s": {"aff": -4, "tru": -5},
                    "r": "마침 휴게실 밖을 지나던 서리 기숙사 학생이 그 말을 들었습니다. 소문이 세라피나 귀에 들어가는 건 시간문제예요.",
                    "next": "다음 날, 복도 구석의 세라피나가 '누구한테 떠벌린 거야?'라고 차갑게 물을 것만 같았다. 그런데 그녀는 편지를 든 채 울고 있었다."}),
    (9, 1): F("비밀은 빼고, 털어놓은 고민을 어떻게 들어 줘야 할지 클라라에게 묻는다.", {"aff": +5, "tru": +6},
              "클라라가 '잘 들어 주는 게 먼저야'라며 웃습니다. 당신은 세라피나의 비밀을 끝까지 지켰어요.",
              "비밀을 지키면서 도움을 구한 자신이 조금 대견했다. 다음 날, 복도 구석에서 편지를 든 세라피나를 본다."),
    (9, 2): F("어젯밤 너무 현실적인 말을 했다며, 어떻게 사과하면 좋을지 클라라에게 묻는다.", {"aff": +4, "tru": +5},
              "클라라가 '말보다 행동'이라며 쿠키 상자를 건네줍니다. 세라피나가 좋아하는 맛이래요.",
              "쿠키 상자를 들고 세라피나를 찾아갈 기회를 엿보던 다음 날, 복도 구석에서 편지를 든 그녀를 본다."),
    # Day 10 → Day 11 (집에서 온 편지)
    (10, 0): F("클라라 말대로, 억지로 묻지 않고 '다 울 때까지 여기 있을게'라고만 한다.", {"aff": +8, "tru": +8},
               "세라피나가 고개를 묻은 채 작게 끄덕입니다.",
               "말을 아낀 덕분에 세라피나는 처음으로 남 앞에서 마음껏 울었다. 다음 날, 빈 교실에서 방어 마법 연습을 같이 하게 된다."),
    (10, 1): F("'울지 마, 별일 아니잖아'라고 씩씩하게 달랜다.", {"aff": +2, "tru": +1},
               "세라피나가 눈물을 닦으며 '...말은 쉽지'라고 중얼거립니다.",
               "위로가 서툴렀다는 걸 알면서도 어쩔 수 없었다. 다음 날, 빈 교실에서 방어 마법 연습을 같이 하게 된다.",
               trap={"lv": 2, "s": {"aff": -5, "tru": -4},
                     "r": "'별일 아니라고? 네가 뭘 안다고!' 세라피나가 편지를 움켜쥐고 돌아섭니다.",
                     "next": "'네가 뭘 안다고'라는 말이 귀에 박혔다. 다음 날, 방어 마법 실습에서 하필 둘이 짝이 된다."}),
    (10, 2): F("클라라에게 들은 가훈 이야기를 꺼내며 '혹시 그것 때문이야?'라고 조심스레 묻는다.",
               {"aff": +4, "tru": +6, "clue": +1},
               "세라피나가 놀란 눈으로 당신을 봅니다. '...알고 있었어?' 그리고 처음으로 편지 내용을 조금 털어놓아요.",
               "편지에 적힌 말들이 당신 마음에도 무겁게 남았다. 다음 날, 빈 교실에서 방어 마법 연습을 같이 하게 된다."),
    # Day 11 → Day 12 (빈 교실 연습)
    (11, 0): F("'저번 일은 잊어 줄게'라며 먼저 장난스럽게 말을 건다.", {"aff": +6, "tru": +4},
               "'잊긴 뭘 잊어!' 세라피나가 얼굴을 붉히며 지팡이를 휘두릅니다.",
               "연습 내내 세라피나의 귀가 빨갰다. 교실을 나서자 에단이 당신을 불러 세운다."),
    (11, 1): F("돌려받은 손수건 이야기를 하며 고맙다고 말한다.", {"aff": +6, "tru": +5},
               "'빨아서 준 것뿐이야.' 손수건에서 꽃향기가 났다고 하자 세라피나가 시선을 피합니다.",
               "손수건의 꽃향기 이야기는 둘만의 농담이 되었다. 교실을 나서자 에단이 당신을 불러 세운다."),
    (11, 2): F("편지를 보여 달라고 했던 건 무례했다고 사과한다.", {"aff": +5, "tru": +7},
               "'...응. 무례했어.' 세라피나가 잠시 머뭇거리다 지팡이를 들어 연습 자세를 잡습니다.",
               "사과를 받은 뒤부터 연습은 한결 부드러워졌다. 교실을 나서자 에단이 당신을 불러 세운다."),
    # Day 12 → Day 13 (에단의 경고)
    (12, 0): F("'세라피나는 가르쳐 줄 필요도 없을 만큼 잘해'라고 에단에게 말한다.", {"aff": +5, "tru": +5},
               "에단이 의아해하는 사이, 복도 모퉁이에서 그 말을 들은 세라피나가 몰래 웃습니다.",
               "칭찬은 돌고 돌아 결국 세라피나 귀에 들어갔다. 다음 날 저녁, 눈 덮인 정원에서 그녀를 만난다."),
    (12, 1): F("에단에게 '실력 있는 애야, 편견은 버려'라고 담담하게 말한다.", {"aff": +5, "tru": +6},
               "에단이 '네가 그렇게까지 말하면...'이라며 한발 물러섭니다.",
               "에단을 설득했다는 이야기를 들은 세라피나가 다음 날 저녁 정원에서 먼저 손을 흔들었다."),
    (12, 2): F("어제 넘어진 일로 에단이 놀리자 '그게 뭐 어때서'라고 당당히 말한다.", {"aff": +6, "tru": +4},
               "에단이 말문이 막히고, 근처에 있던 세라피나가 고개를 푹 숙입니다.",
               "'그게 뭐 어때서'라는 말이 세라피나에게도 들렸던 모양이다. 다음 날 저녁, 정원 벤치에서 그녀를 만난다."),
    # Day 13 → Day 14 (눈 덮인 정원)
    (13, 0): F("에단에게 한 말을 세라피나에게도 그대로 전한다.", {"aff": +8, "tru": +6},
               "세라피나가 놀라 고개를 들었다가, 이내 다시 당신 어깨에 기댑니다. '...바보.'",
               "어깨 위의 무게가 조금 더 무거워졌다. 좋은 쪽으로. 다음 날, 그녀가 고대 서고로 당신을 부른다.",
               trap={"lv": 3, "need": {"aff": 60}, "s": {"aff": -3, "tru": -3, "dist": +3},
                     "r": "'...그 말, 에단한테 먼저 했다고?' 그런 말을 다른 사람에게 먼저 했다는 사실에 세라피나가 토라집니다.",
                     "next": "순서가 틀렸다는 걸 너무 늦게 깨달았다. 그래도 다음 날, 그녀는 고대 서고로 당신을 부른다."}),
    (13, 1): F("복도에서 한 말은 진심이 아니었다고 해명한다.", {"aff": +4, "tru": +5},
               "세라피나가 한참 말이 없다가 '...그럼 진심은 뭔데?'라고 묻습니다.",
               "'그럼 진심은 뭔데'라는 질문이 숙제처럼 남았다. 다음 날, 그녀가 고대 서고로 당신을 부른다."),
    (13, 2): F("에단과 다툰 일을 털어놓으며 기분을 푼다.", {"aff": +3, "tru": +4},
               "세라피나가 '에단과 싸웠어? ...잘했네'라며 처음으로 편을 들어 줍니다.",
               "같은 사람 흉을 보며 둘은 조금 더 가까워졌다. 다음 날, 그녀가 고대 서고로 당신을 부른다."),
    # Day 14 → Day 15 (가문의 비밀 기록)
    (14, 0): F("어젯밤처럼 다정하게, '보여 줘서 고마워'라고 미리 말한다.", {"aff": +5, "tru": +6},
               "세라피나가 '아직 보여 주지도 않았거든?'이라며 웃습니다.",
               "웃음과 함께 비밀 기록의 첫 장이 넘어갔다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
    (14, 1): F("'계속 곁에 있겠다'던 약속처럼, 이 비밀도 함께 짊어지겠다고 한다.", {"aff": +7, "tru": +7},
               "세라피나가 기록을 쥔 손에 힘을 줍니다. '...그 말, 책임져.'",
               "약속은 하나 더 무거워졌고, 그만큼 단단해졌다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
    (14, 2): F("어제 분위기 깬 걸 만회하려고 서고에 먼저 와서 촛불을 켜 둔다.", {"aff": +6, "tru": +4},
               "세라피나가 들어서다 멈칫합니다. '...늦지 말랬더니 먼저 와 있네.'",
               "먼저 기다려 준 일이 세라피나에게는 꽤 큰 의미였다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
    # Day 15 → Day 16 (진눈깨비)
    (15, 0): F("옷 젖는 게 싫다니, 두르고 있던 목도리를 그녀 머리 위에 씌워 준다.", {"aff": +7, "tru": +4},
               "'이게 뭐야, 촌스럽게.' 그래도 세라피나는 목도리를 벗지 않습니다.",
               "촌스럽다던 목도리는 그날 밤까지 그녀 목에 둘려 있었다. 밤이 깊어 그녀를 기숙사 입구까지 바래다준다."),
    (15, 1): F("기록에서 배운 서리 막이 주문을 둘이 함께 외워 본다.", {"aff": +6, "tru": +6, "clue": +1},
               "투명한 얼음막이 머리 위에 펼쳐지자 세라피나가 '우리 가문 주문을 벌써 외웠어?'라며 놀랍니다.",
               "둘만 아는 주문이 생겼다는 사실에 세라피나는 내내 들떠 있었다. 밤이 깊어 그녀를 기숙사 입구까지 바래다준다."),
    (15, 2): F("받은 은 단추를 보여 주며 '약속 잘 지키고 있어'라고 한다.", {"aff": +6, "tru": +5},
               "세라피나가 단추를 보고는 입꼬리를 올립니다. '잃어버리기만 해 봐.'",
               "주머니 속 은 단추가 오늘따라 묵직했다. 밤이 깊어 그녀를 기숙사 입구까지 바래다준다."),
    # Day 16 → Day 17 (기숙사 앞)
    (16, 0): F("'어깨는 다 말랐어?' 하며 그녀가 말려 준 쪽 어깨를 툭툭 친다.", {"aff": +6, "tru": +4},
               "'그걸 왜 지금 꺼내.' 세라피나가 웃음을 참느라 입술을 깨뭅니다.",
               "웃음을 참던 얼굴이 문 너머로 사라졌다. 다음 날, 그녀가 숲 근처에서 잃어버린 브로치를 같이 찾아 달라고 한다."),
    (16, 1): F("'감기 안 걸렸지?' 하며 따뜻한 차 한 병을 건넨다.", {"aff": +7, "tru": +5},
               "'...책임진다더니 진짜네.' 세라피나가 병을 두 손으로 감쌉니다.",
               "따뜻한 차 한 병이 그날 밤의 마지막 선물이었다. 다음 날, 그녀가 숲 근처에서 잃어버린 브로치를 같이 찾아 달라고 한다."),
    (16, 2): F("처마 밑에서 하던 이야기의 끝을 마저 들려 달라고 한다.", {"aff": +5, "tru": +6},
               "세라피나가 문 앞 계단에 걸터앉아 이야기를 이어 갑니다. 들어가기 싫다는 말은 진심이었나 봐요.",
               "이야기는 통금 종이 울릴 때까지 이어졌다. 다음 날, 그녀가 숲 근처에서 잃어버린 브로치를 같이 찾아 달라고 한다."),
    # Day 17 → Day 18 (숲의 위기)
    (17, 0): F("'어젯밤 일은 후회 안 해'라고 말하며 그녀 옆에 나란히 선다.", {"aff": +6, "tru": +6},
               "얼굴이 붉어진 채로도 세라피나가 지팡이를 고쳐 잡습니다. '...지금 그런 말 할 때야?'",
               "위기 속에서도 세라피나는 당신의 말을 잊지 않았다. 다음 날 밤, 그녀가 천문탑으로 당신을 부른다."),
    (17, 1): F("어젯밤 별을 보며 정한 대로 '왼쪽은 내가, 오른쪽은 네가' 하고 신호를 보낸다.", {"aff": +6, "tru": +8},
               "세라피나가 곧바로 알아듣고 오른쪽을 맡습니다. 손발이 척척 맞아요.",
               "별을 보며 정한 신호가 숲에서 둘을 지켜 주었다. 다음 날 밤, 둘은 천문탑에 오른다."),
    (17, 2): F("'아침 일찍 오길 잘했지?' 하고 그녀의 긴장을 풀어 준다.", {"aff": +5, "tru": +5},
               "세라피나가 '지금 농담이 나와?' 하면서도 어깨에 들어간 힘을 뺍니다.",
               "농담 한마디에 굳어 있던 세라피나의 손이 풀렸다. 다음 날 밤, 그녀가 천문탑으로 당신을 부른다."),
    # Day 18 → Day 19 (천문탑)
    (18, 0): F("붕대 감은 팔을 흔들어 보이며 '하나도 안 아파'라고 웃는다.", {"aff": +6, "tru": +6},
               "세라피나가 붕대 위에 살짝 손을 얹습니다. '...거짓말.'",
               "붕대 위에 남은 온기가 오래갔다. 그런데 다음 날부터, 학교에 이상한 소문이 돌기 시작한다."),
    (18, 1): F("되찾은 브로치를 그녀 망토에 직접 달아 준다.", {"aff": +8, "tru": +5},
               "브로치를 다는 동안 세라피나는 숨도 제대로 못 쉬는 것 같았습니다.",
               "망토의 브로치가 별빛에 반짝였다. 그런데 다음 날부터, 학교에 이상한 소문이 돌기 시작한다.",
               trap={"lv": 3, "need": {"aff": 65}, "s": {"aff": -3, "tru": -3},
                     "r": "'그건 내가 할게.' 세라피나가 브로치를 낚아챕니다. 가문의 물건에 손대는 건 아직 일렀나 봐요.",
                     "next": "브로치를 낚아챈 손이 조금 떨리고 있었다. 그리고 다음 날부터, 학교에 이상한 소문이 돌기 시작한다."}),
    (18, 2): F("숲에서 겁먹었던 걸 솔직하게 사과한다.", {"aff": +5, "tru": +7},
               "'...솔직하게 말해 줘서 다행이야. 다음엔 내가 지켜 줄게.' 세라피나의 목소리가 풀립니다.",
               "약한 모습을 보인 뒤에야 둘 사이가 오히려 편해졌다. 그런데 다음 날부터, 학교에 이상한 소문이 돌기 시작한다."),
    # Day 19 → Day 20 (함박눈, 소문)
    (19, 0): F("천문탑에서 들은 '내기'라는 속삭임을 떠올리며, 소문이 무슨 내용인지 먼저 솔직하게 묻는다.",
               {"aff": +3, "tru": +7},
               "세라피나가 잠시 굳더니 '...너도 들었구나'라며 한숨을 쉽니다. 피하지 않고 물어봐 줘서 다행이래요.",
               "소문을 마주 본 두 사람은 적어도 서로를 피하지는 않았다. 하지만 다음 날, 소문은 더 커져 있었다."),
    (19, 1): F("'그때 한 말은 진심이었어'라고 한 번 더 확인시켜 준다.", {"aff": +7, "tru": +6},
               "세라피나가 눈 쌓인 창틀에 '진심'이라고 손가락으로 쓰고는 몰래 지웁니다.",
               "창틀에 썼다 지운 글씨가 마음속에 남았다. 하지만 다음 날, 소문은 더 커져 있었다.",
               trap={"lv": 3, "need": {"tru": 60}, "s": {"aff": -3, "tru": -5},
                     "r": "'진심이었다는 말, 요즘 너무 자주 하는 거 알아?' 소문 때문에 세라피나가 오히려 의심합니다.",
                     "next": "'진심'이라는 말이 가벼워진 것 같아 마음이 무거웠다. 다음 날, 소문은 더 커져 있었다."}),
    (19, 2): F("그날 덮어 준 겉옷을 돌려받으며 '이거 아직 따뜻하네'라고 웃는다.", {"aff": +6, "tru": +4},
               "'...안고 있었던 거 아니거든.' 세라피나가 묻지도 않은 변명을 합니다.",
               "묻지도 않은 변명이 귀여워서 한참 웃었다. 하지만 다음 날, 소문은 더 커져 있었다."),
    # Day 20 → Day 21 (다시 차가워진 눈빛)
    (20, 0): F("목도리를 돌려 달라는 대신, '그거 너한테 더 잘 어울려'라고만 한다.", {"aff": +4, "tru": +4},
               "세라피나가 목도리를 풀려다 멈칫합니다. 차가운 말과 달리 손은 망설이고 있어요.",
               "목도리를 끝내 풀지 않은 게 대답 같았다. 그날 밤, 누군가 그녀의 책상 위에 낡은 쪽지를 올려 두었다."),
    (20, 1): F("'그날 한 말은 내기와 상관없었어'라고 짧고 담담하게 말하고 지나친다.", {"aff": +3, "tru": +6},
               "세라피나가 걸음을 멈추고 당신의 뒷모습을 오래 바라봅니다.",
               "짧은 한마디가 세라피나의 마음속에서 오래 맴돌았다. 그날 밤, 누군가 그녀의 책상 위에 낡은 쪽지를 올려 두었다."),
    (20, 2): F("'어제 공부하자고 한 건, 너랑 더 있고 싶어서였어'라고 뒤늦게 털어놓는다.", {"aff": +5, "tru": +3},
               "'...그걸 이제 말하면 어떡해.' 세라피나의 목소리가 아주 조금 떨립니다.",
               "뒤늦은 진심은 소문보다 늦게 도착했다. 그날 밤, 누군가 그녀의 책상 위에 낡은 쪽지를 올려 두었다."),
    # Day 21 → Day 22 (쪽지)
    (21, 0): F("어제 복도에서 하려던 말이 바로 이거였다고 먼저 말을 꺼낸다.", {"aff": +3, "tru": +8},
               "세라피나가 쪽지를 쥔 손을 내립니다. '...그래서 어제 그렇게 붙잡았던 거야?'",
               "어제의 다급함이 무엇이었는지 세라피나도 조금은 알게 되었다. 다음 날, 눈보라 치는 복도에서 그녀가 기다리고 있다."),
    (21, 1): F("말없이 기다린 이유를 설명한다. '변명보다 네가 직접 보는 게 맞다고 생각했어.'", {"aff": +3, "tru": +7},
               "세라피나가 쪽지를 내려다봅니다. '...그래서 아무 말도 안 했던 거구나.'",
               "기다림이 변명보다 나았는지는 아직 알 수 없었다. 다음 날, 눈보라 치는 복도에서 그녀가 기다리고 있다."),
    (21, 2): F("어제 화낸 걸 먼저 사과하고, 쪽지 이야기를 끝까지 듣겠다고 한다.", {"aff": +4, "tru": +6},
               "세라피나가 놀란 듯 눈을 깜빡입니다. '...사과부터 할 줄은 몰랐어.'",
               "사과부터 한 덕분에 대화는 끊기지 않았다. 다음 날, 눈보라 치는 복도에서 그녀가 기다리고 있다."),
    # Day 22 → Day 23 (진실의 순간)
    (22, 0): F("어제 인정한 것에 더해, 왜 내기를 했는지 그날 밤 일을 처음부터 전부 털어놓는다.",
               {"aff": +12, "tru": +15},
               "세라피나가 끝까지 듣고 나서 울음을 터뜨립니다. '...다 말해 줘서, 고마워.'",
               "모든 걸 털어놓은 밤, 마음은 오히려 가벼웠다. 이튿날, 호숫가에 홀로 앉은 그녀를 발견한다.",
               flag="day23_honest"),
    (22, 1): F("어제 한 거짓말을 바로잡는다. '사실이야. 거짓말해서 미안해.'", {"aff": +5, "tru": +10},
               "세라피나가 차갑게 웃다가 눈물을 흘립니다. '...왜 어제는 그 말을 못 했어?'",
               "거짓말을 바로잡았지만, 한 번 생긴 금은 쉽게 지워지지 않았다. 다음 날, 호숫가에서 그녀를 본다.",
               flag="day23_honest"),
    (22, 2): F("'하루 생각해 보겠다던 대답, 이제 들려줄래?'라고 조심스럽게 묻는다.", {"aff": +3, "tru": +3},
               "'...아직 모르겠어.' 세라피나가 고개를 젓습니다.",
               "대답은 미뤄졌다. 다음 날, 호숫가에서 생각에 잠긴 그녀를 본다.",
               trap={"lv": 2, "s": {"aff": -4, "tru": -4},
                     "r": "'지금 나한테 대답을 재촉하는 거야? 상처받은 건 나야!' 세라피나의 목소리가 높아집니다.",
                     "next": "재촉한 걸 후회하며 잠 못 드는 밤을 보냈다. 다음 날, 그래도 발걸음은 호숫가로 향한다."}),
    # Day 23 → Day 24 (호숫가)
    (23, 0): F("어제 가슴을 콩 친 일을 떠올리며 '아직 아파?' 하고 웃어 보인다.", {"aff": +6, "tru": +5},
               "세라피나가 피식 웃습니다. '...그 정도로 아팠으면 좋겠다.'",
               "웃음이 돌아오자 호숫가의 바람도 덜 차가웠다. 다음 날, 집에서 그녀를 뒤흔드는 편지가 날아든다."),
    (23, 1): F("뺨을 맞고서야 깨달았다며, 이제라도 진실을 말한다.", {"aff": +3, "tru": +8},
               "세라피나가 등을 돌린 채 말합니다. '...너무 늦었어. 그래도, 들었어.'",
               "너무 늦은 진실이었지만, 그래도 전해지기는 했다. 다음 날, 집에서 그녀를 뒤흔드는 편지가 날아든다."),
    (23, 2): F("'떠나겠다는 말, 취소할게. 네가 허락해 준다면'이라고 말한다.", {"aff": +6, "tru": +6},
               "세라피나가 물가에 돌을 던지며 '...누가 떠나래?'라고 중얼거립니다.",
               "'누가 떠나래'라는 말이 그날의 답이었다. 다음 날, 집에서 그녀를 뒤흔드는 편지가 날아든다."),
    # Day 24 → Day 25 (정략결혼 편지)
    (24, 0): F("지난번처럼 아무 말 없이 곁에 앉아 편지를 함께 들여다본다.", {"aff": +7, "tru": +7},
               "세라피나가 편지를 당신 쪽으로 기울입니다. 혼자 읽기엔 너무 무거운 편지였어요.",
               "무거운 편지를 둘이 나눠 들자 조금은 견딜 만해졌다. 다음 날, 대연회장에 정략결혼 소문이 퍼진다."),
    (24, 1): F("편지를 써 줬던 것처럼, 집에 보낼 답장을 같이 써 보자고 한다.", {"aff": +6, "tru": +8, "clue": +1},
               "세라피나가 깃펜을 쥡니다. '...네가 옆에 있으면 쓸 수 있을 것 같아.'",
               "둘이 함께 쓴 답장이 부엉이에 실려 날아갔다. 다음 날, 대연회장에 정략결혼 소문이 퍼진다."),
    (24, 2): F("이번엔 멀리서 지켜보지 않고, 먼저 다가가 '무슨 일이야?'라고 묻는다.", {"aff": +5, "tru": +5},
               "세라피나가 놀란 얼굴로 돌아봅니다. '...이번엔 다가와 주네.'",
               "먼저 다가간 한 걸음이 거리를 조금 좁혔다. 다음 날, 대연회장에 정략결혼 소문이 퍼진다."),
    # Day 25 → Day 26 (대연회장)
    (25, 0): F("약속대로 그녀 곁에 서서 '괜찮아, 내가 있어'라고 작게 속삭인다.", {"aff": +8, "tru": +7},
               "떨리던 세라피나의 손이 당신의 소매를 꼭 붙잡습니다.",
               "소매를 붙잡은 손을 끝까지 놓지 않았다. 다음 날, 그녀가 학교 지하의 오래된 유적으로 당신을 이끈다."),
    (25, 1): F("'도망치자던 말은 잊어. 이번엔 여기서 맞서자'라고 말한다.", {"aff": +6, "tru": +7},
               "세라피나가 놀란 눈으로 당신을 보다가 고개를 똑바로 듭니다.",
               "도망 대신 맞서기로 한 날, 세라피나는 처음으로 고개를 숙이지 않았다. 다음 날, 그녀가 오래된 유적으로 당신을 이끈다."),
    (25, 2): F("가문 뜻을 따르라고 했던 말을 모두 앞에서 취소하고 사과한다.", {"aff": +5, "tru": +6},
               "웅성거림 속에서 세라피나가 입술을 깨물며 당신을 봅니다. '...진짜 바보야.'",
               "모두 앞에서 한 사과는 생각보다 큰 용기였다. 다음 날, 그녀가 학교 지하의 오래된 유적으로 당신을 부른다."),
    # Day 26 → Day 27 (비밀 아지트)
    (26, 0): F("'어제 연회장, 너무 갑작스러웠지?' 하고 그녀의 기분을 먼저 살핀다.", {"aff": +6, "tru": +7},
               "'갑작스러웠지. ...근데 싫진 않았어.' 세라피나가 고개를 돌립니다.",
               "싫지 않았다는 말이 오래 귀에 남았다. 다음 날 아침, 부엉이가 창문을 두드린다."),
    (26, 1): F("그날 걸었던 비밀 산책로 이야기를 하며 '또 가자'고 한다.", {"aff": +7, "tru": +5},
               "세라피나가 '30일 지나도?'라고 묻습니다. 당신은 고개를 끄덕여요.",
               "'30일이 지나도'라는 말이 약속처럼 남았다. 다음 날 아침, 부엉이가 창문을 두드린다."),
    (26, 2): F("어제 더 당당하지 못했던 게 미안하다고 털어놓는다.", {"aff": +5, "tru": +6},
               "세라피나가 '조용히 지켜 준 것도 알아'라며 당신의 손등을 톡 칩니다.",
               "조용한 방식도 누군가를 지킬 수 있다는 걸 알았다. 다음 날 아침, 부엉이가 창문을 두드린다."),
    # Day 27 → Day 28 (편지)
    (27, 0): F("편지 첫 줄을 읽기도 전에, 어제 일을 떠올리며 혼자 웃는다.", {"aff": +5, "tru": +5},
               "창밖의 부엉이가 답장을 재촉하듯 부리로 창을 쪼아요.",
               "부엉이를 기다리게 하면서도 웃음이 멈추질 않았다. 다음 날 밤, 둘은 다시 천문탑에 오른다."),
    (27, 1): F("'마법 같았다'던 어제 말을 그대로 답장 첫 줄에 적는다.", {"aff": +7, "tru": +7},
               "답장을 받은 세라피나가 '똑같은 말을 두 번이나 하냐'면서도 편지를 베개 밑에 넣어 둡니다.",
               "베개 밑의 편지 이야기는 나중에 클라라에게서 들었다. 다음 날 밤, 천문탑에서 그녀가 기다린다."),
    (27, 2): F("남은 시간이 아쉬우니 오늘 하루를 통째로 같이 보내자고 답장한다.", {"aff": +6, "tru": +5},
               "'하루 종일? ...좋아.' 짧은 답장이 금방 돌아옵니다.",
               "하루 종일 함께 보낸 날은 생각보다 빨리 지나갔다. 다음 날 밤, 둘은 천문탑에 오른다."),
    # Day 28 → Day 29 (약속 전날 밤)
    (28, 0): F("어제 아침에 안아 준 것처럼, 오늘 밤도 그녀를 망토 안으로 감싸 준다.", {"aff": +7, "tru": +5},
               "세라피나가 망토 안에서 작게 웃습니다. '...오늘만 두 번째야.'",
               "두 번째 포옹은 첫 번째보다 길었다. 그리고 마침내 30일째 아침이 밝았다."),
    (28, 1): F("답장에 쓴 마음을 직접 소리 내어 다시 말해 준다.", {"aff": +7, "tru": +7},
               "세라피나가 '글로 볼 때보다 더 부끄럽네'라며 얼굴을 가립니다.",
               "글로 쓴 말과 소리 내어 한 말이 같다는 게 중요했다. 그리고 마침내 30일째 아침이 밝았다."),
    (28, 2): F("주머니에서 그 편지를 꺼내며 '하루 종일 들고 다녔어'라고 말한다.", {"aff": +7, "tru": +5},
               "세라피나가 편지를 낚아채려다 실패하고는 웃음을 터뜨립니다.",
               "편지를 사이에 둔 실랑이가 마지막 밤을 가볍게 만들었다. 그리고 마침내 30일째 아침이 밝았다."),
    # Day 29 → Day 30 (마지막 날)
    (29, 0): F("어젯밤 약속대로, 정식으로 사귀자고 또박또박 말한다.", {"aff": +15, "tru": +15},
               "세라피나가 '...약속은 지켰네'라며 숨을 고릅니다. 이제 그녀가 대답할 차례예요—"),
    (29, 1): F("어젯밤 다짐처럼, 앞으로 올 시련을 함께 헤쳐 나가자며 손을 내민다.", {"aff": +12, "tru": +14},
               "세라피나가 내민 손을 내려다봅니다. 그리고 천천히 고개를 들어요—"),
    (29, 2): F("'아쉽다'던 어젯밤 말을 고쳐, '오늘은 끝이 아니라 시작이야'라고 말한다.", {"aff": +13, "tru": +13},
               "세라피나의 눈이 커집니다. 그리고 그녀가 대답합니다—"),
}

# 어제 함정에 걸렸다면 나오는 선택지
APOLOGY = F("어제 일을 먼저 진심으로 사과한다.", {"aff": +3, "tru": +6},
            "세라피나가 잠시 망설이다 '...알았어'라며 사과를 받아 줍니다. 그래도 어색함이 조금 남아 있어요.",
            "사과는 받아 줬지만, 아직 조심스러운 거리가 남아 있었다.")


# ==========================================
# 4-3-1. 관계가 아직 먼 경우의 장면 (서먹한 버전)
#  호감도가 그 날까지 '그 난이도에서 쌓을 수 있는 만큼'의 45%에 못 미치면,
#  둘이 이미 가까운 것처럼 쓰인 장면 대신 아래 서먹한 버전이 나옴.
#  (어려움은 호감도가 천천히 오르므로 기준도 낮음 → 잘 플레이하면 가까운 장면이 나옴)
#  intro: 장면 맨 위 문장 / desc · dialogue: 바뀐 장면 / choices: 바뀐 선택지 (없으면 원래 선택지)
# ==========================================
# 각 난이도에서 '최선을 다했을 때' 그날이 끝난 뒤의 호감도 (시뮬레이션으로 잰 값)
BEST_AFF = {
    "쉬움":   [25, 33, 41, 51, 57, 77, 87, 99, 100, 100, 100, 100, 100, 100, 100,
               100, 100, 100, 100, 95, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    "보통":   [22, 25, 28, 32, 35, 43, 47, 52, 57, 59, 65, 70, 78, 83, 87,
               91, 97, 100, 100, 88, 90, 94, 100, 100, 100, 100, 100, 100, 100, 100],
    "어려움": [21, 23, 25, 26, 28, 34, 36, 37, 39, 40, 43, 45, 51, 54, 57,
               60, 63, 66, 69, 58, 59, 62, 67, 70, 74, 79, 86, 90, 94, 98],
}
CLOSE_RATIO = 0.45


def is_distant(day):
    """오늘 두 사람이 아직 서먹한 사이인지"""
    # 23일차에 끝까지 거짓말했다면, 그 뒤로는 호감도와 상관없이 서먹한 사이
    if day >= 24 and st.session_state.flags.get("day23_defensive"):
        return True
    curve = BEST_AFF.get(st.session_state.difficulty, BEST_AFF["보통"])
    best_prev = 20 if day <= 1 else curve[min(day, 31) - 2]
    need = 20 + CLOSE_RATIO * max(5, best_prev - 20)
    return st.session_state.affection < need


DISTANT = {
    9: {"intro": "저녁 무렵, 안개 낀 호숫가를 걷다가 버드나무 아래 혼자 앉은 세라피나를 발견했다.",
        "desc": "당신을 본 세라피나의 표정이 굳는다. 혼자 있고 싶었던 모양이다.",
        "dialogue": [("세라피나", "...뭐야, 따라온 거야? 혼자 있고 싶으니까 저리 가.", "draco")],
        "choices": [
            F("방해해서 미안하다며 조용히 자리를 피해 준다.", {"aff": +4, "tru": +5},
              "돌아서는 당신의 등 뒤로 '...고마워'라는 작은 목소리가 들린 것 같습니다.",
              "억지로 다가가지 않은 게 오히려 그녀의 마음에 남은 듯했다. 다음 날, 클라라가 휴게실에서 말을 건넨다."),
            F("멀찍이 떨어진 바위에 앉아 말없이 호수만 바라본다.", {"aff": +3, "tru": +4},
              "한참 뒤, 세라피나가 먼저 일어나며 '...감기 걸리기 전에 들어가'라고 툭 던집니다.",
              "같은 호수를 다른 자리에서 바라본 저녁이었다. 다음 날, 클라라가 휴게실에서 말을 건넨다."),
            F("무슨 고민 있냐며 옆에 바짝 붙어 앉는다.", {"aff": +2, "tru": +1},
              "세라피나가 미간을 찌푸리며 한 칸 떨어져 앉습니다. '...너한테 말할 이유 없어.'",
              "그녀의 고민은 끝내 듣지 못했다. 다음 날, 클라라가 휴게실에서 말을 건넨다.",
              trap={"lv": 2, "s": {"aff": -5, "tru": -3, "dist": +3},
                    "r": "'가까이 오지 마.' 세라피나가 벌떡 일어나 가 버립니다. 아직 그럴 사이가 아니었어요.",
                    "next": "괜히 다가갔다가 더 멀어진 기분이었다. 다음 날, 클라라가 휴게실에서 말을 건넨다."}),
        ]},
    12: {"title": "어쩔 수 없는 실습 짝", "intro": "방어 마법 실습 시간, 교수님이 짝을 정해 주었다. 하필 세라피나와 한 조다.",
         "desc": "빈 교실에서 실습을 시작했지만, 세라피나는 당신과 눈도 마주치지 않는다.",
         "dialogue": [("세라피나", "교수님이 정한 거니까 어쩔 수 없이 하는 거야. 착각하지 마.", "draco")],
         "choices": [
             F("말없이 실습에만 집중하며 그녀의 주문을 정확히 받아 낸다.", {"aff": +4, "tru": +6},
               "세라피나가 잠깐 놀란 눈으로 당신을 봅니다. '...생각보다 하네.'",
               "실습이 끝나고 세라피나는 인사도 없이 나갔지만, 표정은 조금 덜 차가웠다. 복도에서는 에단이 당신을 기다리고 있다."),
             F("'우리 꽤 잘 맞는 것 같지 않아?' 하고 먼저 말을 건다.", {"aff": +2, "tru": +1},
               "'전혀.' 세라피나가 단칼에 자르지만, 귀 끝이 살짝 붉어집니다.",
               "'전혀'라는 대답이 묘하게 싫지 않았다. 교실을 나서자 에단이 당신을 불러 세운다.",
               trap={"lv": 2, "s": {"aff": -4, "tru": -2},
                     "r": "'잘 맞긴 뭐가 잘 맞아.' 세라피나가 지팡이를 거두고 실습을 끝내 버립니다.",
                     "next": "실습은 반도 못 하고 끝났다. 교실을 나서자 에단이 당신을 불러 세운다."}),
             F("일부러 실수해서 세라피나에게 한 수 배우는 척한다.", {"aff": +3, "tru": +2},
               "'그것도 못 해?' 투덜대면서도 세라피나가 손목 각도를 고쳐 줍니다.",
               "손목을 고쳐 주던 손끝이 생각보다 조심스러웠다. 교실을 나서자 에단이 당신을 불러 세운다.",
               trap={"lv": 3, "s": {"aff": -3, "tru": -4},
                     "r": "'일부러 틀리는 거 다 보여. 날 놀리는 거야?' 세라피나가 차갑게 돌아섭니다.",
                     "next": "얕은 수는 금방 들통났다. 교실을 나서자 에단이 당신을 불러 세운다."}),
         ]},
    14: {"intro": "저녁 무렵, 눈 덮인 정원을 지나다가 벤치에 혼자 앉은 세라피나를 보았다.",
         "desc": "벤치 한쪽 끝에 앉은 세라피나가 입김을 불며 하늘만 보고 있다. 옆자리는 비어 있지만, 다가가기엔 거리가 느껴진다.",
         "dialogue": [("세라피나", "...왜 서 있어. 앉든지 가든지 해.", "draco")],
         "choices": [
             F("벤치 반대쪽 끝에 조용히 앉는다.", {"aff": +5, "tru": +4},
               "둘 사이에 한 사람 자리만큼의 거리. 그래도 세라피나는 일어나지 않습니다.",
               "말없이 앉아 있던 시간이 생각보다 편했다. 다음 날, 고대 마법 서고에서 그녀와 마주친다."),
             F("따뜻한 코코아를 사 와서 말없이 옆에 놓아 준다.", {"aff": +6, "tru": +3},
               "세라피나가 컵을 한참 보다가 집어 듭니다. '...덜 달게 탔네.'",
               "빈 컵을 돌려주며 그녀가 처음으로 먼저 '잘 자'라고 했다. 다음 날, 고대 마법 서고에서 그녀와 마주친다."),
             F("바로 옆에 앉아 '어깨 빌려줄까?' 하고 농담한다.", {"aff": +2},
               "세라피나가 어이없다는 듯 웃습니다. '꿈도 꾸지 마.'",
               "농담은 농담으로 끝났다. 다음 날, 고대 마법 서고에서 그녀와 마주친다.",
               trap={"lv": 2, "s": {"aff": -6, "tru": -3, "dist": +4},
                     "r": "'미쳤어?' 세라피나가 벌떡 일어나 정원을 빠져나갑니다.",
                     "next": "텅 빈 벤치에 혼자 남았다. 다음 날, 고대 마법 서고에서 그녀와 마주친다."}),
         ]},
    15: {"intro": "고대 마법 서고에 과제 자료를 찾으러 갔다가, 낡은 책을 펼쳐 놓은 세라피나와 마주쳤다.",
         "desc": "세라피나가 황급히 책을 덮는다. 표지에 가문의 문양이 새겨져 있다.",
         "dialogue": [("세라피나", "...봤어? 아무것도 못 본 걸로 해. 이건 남한테 보여 줄 게 아니야.", "draco")],
         "choices": [
             F("못 본 걸로 하겠다고 약속하고 조용히 자리를 비켜 준다.", {"aff": +5, "tru": +8},
               "세라피나가 잠시 당신을 바라보다 고개를 끄덕입니다. '...약속했어.'",
               "지켜진 약속 하나가 그녀의 경계를 조금 낮췄다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
             F("과제 자료만 챙기고 아무 일 없었다는 듯 지나간다.", {"aff": +3, "tru": +4},
               "세라피나가 당신의 뒷모습을 의아한 눈으로 봅니다. 캐묻지 않는 게 의외였나 봐요.",
               "아무것도 묻지 않은 게 오히려 기억에 남은 모양이었다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
             F("무슨 책인지 궁금하다며 한 번만 보여 달라고 조른다.", {"aff": -3, "tru": -4},
               "'남의 집 비밀이 그렇게 궁금해?' 세라피나가 책을 품에 안고 서고를 나갑니다.",
               "괜한 호기심이 벽을 하나 더 쌓았다. 다음 날, 안뜰에 진눈깨비가 쏟아진다."),
         ]},
    17: {"intro": "늦은 밤, 돌아가는 길이 같은 방향이라 세라피나와 몇 걸음 떨어져 걷게 되었다.",
         "desc": "서리 기숙사로 내려가는 계단 앞. 세라피나가 걸음을 멈추고 돌아본다.",
         "dialogue": [("세라피나", "...여기까지 따라올 거야? 너희 기숙사는 반대쪽이잖아.", "draco")],
         "choices": [
             F("'밤길이 어두워서'라고 짧게 말하고 돌아선다.", {"aff": +5, "tru": +4},
               "세라피나가 잠시 멈칫하더니 '...잘 가'라고 작게 말합니다.",
               "처음으로 들은 '잘 가'가 이상하게 오래 남았다. 다음 날, 숲 쪽으로 혼자 가는 그녀를 본다."),
             F("내일 수업 이야기를 꺼내며 대화를 이어 가려 한다.", {"aff": +3, "tru": +2},
               "'...그건 내일 얘기해.' 대답은 짧았지만, 문을 열기 전 한 번 더 돌아봅니다.",
               "그녀가 돌아본 게 착각은 아니었다. 다음 날, 숲 쪽으로 혼자 가는 그녀를 본다."),
             F("'좀 더 같이 걷자'며 손을 내민다.", {"aff": +1},
               "세라피나가 내민 손을 내려다보다 피식 웃습니다. '...무슨 소리야.'",
               "내민 손은 그대로 주머니로 돌아갔다. 다음 날, 숲 쪽으로 혼자 가는 그녀를 본다.",
               trap={"lv": 2, "s": {"aff": -5, "tru": -4, "dist": +4},
                     "r": "'우리가 언제부터 그런 사이였어?' 세라피나가 문을 쾅 닫고 들어갑니다.",
                     "next": "닫힌 문 앞에서 한참을 서 있었다. 다음 날, 숲 쪽으로 혼자 가는 그녀를 본다."}),
         ]},
    18: {"intro": "숲 입구를 지나다가, 무언가를 찾느라 땅만 보며 걷는 세라피나를 보았다.",
         "desc": "가문의 은 브로치를 잃어버린 모양이다. 그 순간, 덤불 속에서 사나운 마법 생물이 튀어나왔다!"},
    19: {"intro": "밤이 되어 별을 보러 천문탑에 올랐더니 세라피나가 먼저 와 있었다.",
         "desc": "난간에 기대 선 세라피나가 당신을 보고도 자리를 피하지 않는다.",
         "dialogue": [("세라피나", "...숲에서 일은 고마웠어. 그 말 하려고 했어. 그게 다야.", "draco")],
         "choices": [
             F("'별 보러 왔어. 같이 봐도 돼?' 하고 조심스럽게 묻는다.", {"aff": +6, "tru": +5},
               "세라피나가 대답 대신 난간 한쪽을 비켜 줍니다.",
               "말없이 별을 본 밤이 지나고, 다음 날부터 학교에 이상한 소문이 돌기 시작한다."),
             F("고맙다는 말을 들은 것만으로 충분하다며 웃고 내려간다.", {"aff": +4, "tru": +5},
               "'...이상한 애.' 세라피나의 목소리에 아주 옅은 웃음기가 섞입니다.",
               "계단을 내려가는 발걸음이 가벼웠다. 그런데 다음 날부터, 학교에 이상한 소문이 돌기 시작한다."),
             F("'별보다 네가 더 예쁘다'고 말한다.", {"aff": +1},
               "세라피나가 어이없다는 듯 당신을 봅니다. '...진심으로 하는 말이야, 그거?'",
               "대답할 틈도 없이 그녀가 먼저 내려갔다. 다음 날부터, 학교에 이상한 소문이 돌기 시작한다.",
               trap={"lv": 2, "s": {"aff": -5, "dist": +4},
                     "r": "'그런 말 아무한테나 하지?' 세라피나가 차갑게 등을 돌립니다.",
                     "next": "가벼운 말 한마디가 그녀를 더 멀어지게 했다. 다음 날부터, 학교에 이상한 소문이 돌기 시작한다."}),
         ]},
    25: {"intro": "복도를 지나다 세라피나가 친구에게 하는 말을 우연히 들었다.",
         "desc": "집에서 그녀를 다른 명문 귀족 집안과 정략결혼시키려 한다는 이야기였다. 세라피나가 당신을 발견하고 굳은 얼굴로 돌아본다.",
         "dialogue": [("세라피나", "...너까지 들었어? 상관하지 마. 네 일 아니잖아.", "draco")],
         "choices": [
             F("'네 일이 내 일은 아니지만, 네 편은 될 수 있어'라고 말한다.", {"aff": +7, "tru": +8},
               "세라피나가 멈춰 섭니다. '...왜 내 편을 들어?' 대답을 기다리는 눈이에요.",
               "'왜 내 편을 들어?'라는 질문이 머릿속을 맴돌았다. 다음 날 대연회장, 정략결혼 소문을 들은 학생들이 그녀를 비웃는다."),
             F("못 들은 척하며 조용히 지나간다.", {"aff": +2, "tru": +3},
               "세라피나가 안도한 듯 숨을 내쉽니다.",
               "모른 척해 준 게 그녀에겐 배려였을지도 모른다. 다음 날 대연회장, 정략결혼 소문을 들은 학생들이 그녀를 비웃는다."),
             F("'정략결혼이면 오히려 편하지 않아?'라고 묻는다.", {"aff": -8, "tru": -4, "dist": +5},
               "세라피나가 당신을 노려봅니다. '네가 뭘 알아.'",
               "그 눈빛이 한동안 잊히지 않았다. 다음 날 대연회장, 정략결혼 소문을 들은 학생들이 그녀를 비웃는다."),
         ]},
    26: {"intro": "전교생이 모인 대연회장. 정략결혼 소문을 들은 서리 기숙사 귀족 학생들이 세라피나를 둘러싸고 비웃고 있다.",
         "desc": "세라피나는 아무렇지 않은 척 고개를 들고 있지만, 포크를 쥔 손이 떨린다. 당신은 자리에서 일어선다.",
         "dialogue": [("세라피나", "(차갑게) ...앉아. 네가 끼어들 일 아니야.", "draco")],
         "choices": [
             F("비웃는 학생들에게 '그만해'라고 단호하게 말한다.", {"aff": +7, "tru": +6},
               "연회장이 조용해집니다. 세라피나가 놀란 눈으로 당신을 봅니다. '...왜 네가 나서?'",
               "소란이 가라앉은 뒤에도 그녀의 '왜'라는 질문이 남았다. 다음 날, 세라피나가 어디에도 보이지 않는다."),
             F("조용히 그녀 옆자리로 가서 앉는다.", {"aff": +5, "tru": +5},
               "세라피나가 당신을 흘끗 보고는 아무 말도 하지 않습니다. 비웃음 소리가 조금씩 잦아들어요.",
               "그날 저녁, 둘은 한마디도 하지 않았지만 끝까지 같은 자리에 앉아 있었다. 다음 날, 세라피나가 어디에도 보이지 않는다."),
             F("모두가 듣는 앞에서 세라피나를 좋아한다고 외친다.", {"aff": +2},
               "연회장이 술렁입니다. 세라피나가 얼굴을 붉히지만 기쁜 얼굴은 아닙니다. '...장난도 정도껏 해.'",
               "연회장의 웅성거림이 밤늦게까지 이어졌다. 다음 날, 세라피나가 어디에도 보이지 않는다.",
               trap={"lv": 2, "s": {"aff": -6, "tru": -5, "dist": +5},
                     "r": "'이 상황에서 그런 말을 하면 내가 더 웃음거리가 되잖아!' 세라피나가 연회장을 뛰쳐나갑니다.",
                     "next": "그녀가 뛰쳐나간 문을 한참 바라보았다. 다음 날, 세라피나가 어디에도 보이지 않는다."}),
         ]},
    # 아래는 장면은 그대로 두고, 아직 가깝지 않을 때 말투만 바꾸는 날 (soft)
    10: {"soft": True,
         "dialogue": [("클라라", "{p}, 요즘 세라피나 쪽을 자꾸 쳐다보더라. 그 애, 가문의 압박 때문에 속앓이가 심하대. "
                       "다가가고 싶으면 솔직하고 다정하게 대하는 게 제일 중요해.", "hermione")]},
    13: {"soft": True,
         "desc": "에단이 복도에서 당신을 불러 세운다. 요즘 세라피나 주변을 맴도는 당신이 영 못마땅한 표정이다."},
    21: {"soft": True,
         "desc": "소문이 점점 커지자, 안 그래도 차갑던 세라피나의 눈빛이 완전히 얼어붙었다. 이제는 당신을 투명 인간 취급한다."},
    23: {"soft": True,
         "dialogue": [("세라피나", "처음부터... 날 내기 상대로 이용한 거였어? 역시 그랬구나. 잠깐이라도 믿어 볼까 했던 내가 바보지!", "draco")]},
    27: {"title": "지하 유적에 숨은 그녀", "intro": "온종일 보이지 않는 세라피나를 찾아 헤매다, 학교 지하의 오래된 유적까지 내려갔다.",
         "desc": "무너진 기둥 사이에 혼자 앉은 세라피나가 놀란 얼굴로 고개를 든다.",
         "dialogue": [("세라피나", "...어떻게 찾아왔어? 여긴 나만 아는 곳인데. 30일도 며칠 안 남았네. 내기 결과는 뻔하지?", "draco")],
         "choices": [
             F("'내기는 이미 졌어. 그래도 네 곁에 있고 싶어'라고 솔직하게 말한다.", {"aff": +8, "tru": +8},
               "세라피나가 한참 말이 없다가 '...이상한 애'라며 고개를 돌립니다. 그래도 나가라고는 하지 않아요.",
               "그녀가 나가라고 하지 않은 것만으로도 충분했다. 다음 날 아침, 짧은 쪽지가 도착한다."),
             F("남은 며칠이라도 친구로 지내자고 한다.", {"aff": +5, "tru": +6},
               "'...친구라.' 세라피나가 그 말을 곱씹듯 중얼거립니다.",
               "'친구'라는 말이 둘 사이에 조용히 놓였다. 다음 날 아침, 짧은 쪽지가 도착한다."),
             F("'아직 모르는 일이지' 하고 장난스럽게 윙크한다.", {"aff": +1},
               "세라피나가 기가 막힌다는 듯 웃습니다. '...정말 끝까지 그러네.'",
               "웃음인지 한숨인지 모를 소리를 남기고 그녀가 먼저 올라갔다. 다음 날 아침, 짧은 쪽지가 도착한다.",
               trap={"lv": 2, "s": {"aff": -5, "tru": -3},
                     "r": "'여전히 그게 게임이구나.' 세라피나가 차갑게 일어나 유적을 떠납니다.",
                     "next": "어두운 유적에 혼자 남았다. 다음 날 아침, 짧은 쪽지가 도착한다."}),
         ]},
    28: {"title": "두 줄짜리 쪽지", "intro": "이른 아침, 부엉이가 짧은 쪽지 한 장을 물어다 주었다.",
         "desc": "세라피나의 글씨다. 단 두 줄뿐이다.",
         "dialogue": [("세라피나", "(쪽지) '30일째 되는 날 밤, 천문탑으로 와. 할 말이 있어. — 세라피나'", "draco")],
         "choices": [
             F("'꼭 갈게'라고 답장을 보낸다.", {"aff": +6, "tru": +6},
               "답장을 받은 세라피나가 쪽지를 접어 책 사이에 끼웁니다.",
               "약속의 날이 하루 앞으로 다가왔다. 다음 날 밤, 천문탑에서 그녀를 마주친다."),
             F("쪽지를 몇 번이고 다시 읽으며 무슨 말일지 고민한다.", {"aff": +3, "tru": +3},
               "하루 종일 그 '할 말'이 무엇인지 머릿속을 떠나지 않습니다.",
               "그 '할 말'을 상상하느라 하루가 다 갔다. 다음 날 밤, 천문탑에서 그녀를 마주친다."),
             F("'할 말 있으면 지금 해'라며 바로 찾아간다.", {"aff": -3, "tru": -2},
               "'...약속한 날에 하겠다고 했잖아.' 세라피나가 불쾌한 듯 돌아섭니다.",
               "성급했다는 걸 깨달았을 땐 이미 늦었다. 다음 날 밤, 천문탑에서 그녀를 마주친다."),
         ]},
    29: {"intro": "30일째를 하루 앞둔 밤, 천문탑에 올랐다.",
         "desc": "먼저 와 있던 세라피나가 당신을 보고도 난간 끝에서 움직이지 않는다.",
         "dialogue": [("세라피나", "...내일이 마지막이야. 솔직히 아직도 네 진심을 모르겠어.", "draco")],
         "choices": [
             F("'내일, 내 진심을 다 말할게'라고 약속한다.", {"aff": +7, "tru": +7},
               "세라피나가 처음으로 당신을 똑바로 봅니다. '...기다릴게.'",
               "'기다릴게'라는 말을 품고 마지막 밤이 저물었다."),
             F("말없이 한 걸음 떨어져 함께 별을 본다.", {"aff": +4, "tru": +5},
               "둘 사이의 거리는 그대로지만, 세라피나가 먼저 자리를 뜨지는 않습니다.",
               "한 걸음의 거리를 둔 채 마지막 밤이 저물었다."),
             F("'내일 대답만 잘 해 주면 돼'라고 가볍게 말한다.", {"aff": -4, "tru": -4},
               "'...결국 끝까지 내기 얘기네.' 세라피나의 목소리가 식습니다.",
               "차가워진 공기 속에서 마지막 밤이 저물었다."),
         ]},
}


def apply_distant(day, story):
    """서먹한 사이라면 그날 장면을 서먹한 버전으로 바꿈"""
    var = DISTANT.get(day)
    if not var or not is_distant(day):
        return story
    story = dict(story)
    name = html.escape(st.session_state.get("player_name", ""))
    if var.get("soft"):                  # 장면은 그대로, 말투만 바꿈
        if "desc" in var:
            story["desc"] = var["desc"]
        if "dialogue" in var:
            story["dialogue"] = [(a, b.replace("{p}", name), c) for a, b, c in var["dialogue"]]
        return story
    story["distant"] = True
    story["intro"] = var["intro"]
    if "title" in var:
        story["title"] = var["title"]
    story["desc"] = var["desc"]
    if "dialogue" in var:
        story["dialogue"] = var["dialogue"]
    if "choices" in var:
        story["fchoices"] = var["choices"]
    return story


def follow_up(day):
    """어제 고른 선택에 따라 오늘 추가로 나오는 선택지 (없으면 None)"""
    last = st.session_state.get("last_choice")
    if not last or last[0] != day - 1:
        return None
    prev_day, prev_idx, trapped = last[0], last[1], last[2]
    distant_prev = len(last) > 3 and last[3]
    if trapped:
        return APOLOGY
    if distant_prev:
        return None          # 어제가 서먹한 버전 장면이었다면 이어지는 선택지 없음
    return FOLLOW.get((prev_day, prev_idx))   # 어제도 '↪' 선택지를 골랐다면 없음


def trap_on(trap):
    """지금 난이도·관계 상태에서 이 함정이 작동하는지"""
    if not trap or DIFFICULTY[st.session_state.difficulty]["trap"] < trap["lv"]:
        return None
    need = trap.get("need")
    if need and st.session_state.affection >= need.get("aff", 0) \
            and st.session_state.trust >= need.get("tru", 0):
        return None      # 관계가 충분히 깊어서 적극적인 행동이 통함
    return trap


def active_trap(day, idx):
    return trap_on(TRAPS.get((day, idx)))


def day_options(day, story):
    """오늘 고를 수 있는 선택지 전부 (기본 3개 + 어제 선택에 따른 '↪' 선택지)"""
    opts = []
    if story.get("fchoices"):            # 서먹한 버전 장면의 선택지
        for idx, ch in enumerate(story["fchoices"]):
            opts.append({"idx": idx, "t": ch["t"], "s": ch["s"], "r": ch["r"], "flag": ch["flag"],
                         "next": ch["next"], "trap": ch["trap"], "follow": False, "variant": True})
    else:
        nexts = NEXT.get(day, ["", "", ""])
        for idx, ch in enumerate(story["choices"]):
            opts.append({"idx": idx, "t": ch[0], "s": ch[1], "r": ch[2],
                         "flag": ch[3] if len(ch) > 3 else None,
                         "next": nexts[idx], "trap": TRAPS.get((day, idx)), "follow": False,
                         "variant": False})
    fu = follow_up(day)
    if fu and (not story.get("distant") or fu is APOLOGY):
        opts.append({"idx": 3, "t": T(fu["t"]), "s": fu["s"], "r": T(fu["r"]), "flag": fu["flag"],
                     "next": fu["next"], "trap": fu["trap"], "follow": True,
                     "variant": bool(story.get("distant"))})
    return opts


# ==========================================
# 4-4. 21일차: 내기 소문이 들통나는 날 → 무엇을 골랐든 호감도가 떨어짐
#  (마음의 상처로는 치지 않아서, 남은 날 동안 노력하면 회복할 수 있음)
# ==========================================
BET_PENALTY = {"쉬움": 5, "보통": 12, "어려움": 18}


def advance_day():
    """다음 날로 넘어가기 (21일차에 들어설 때 내기 들통 이벤트)"""
    st.session_state.day += 1
    if st.session_state.day == 21 and not st.session_state.get("bet_penalty"):
        drop = BET_PENALTY[st.session_state.difficulty]
        before = st.session_state.affection
        update_stats(aff=-drop)
        st.session_state.bet_penalty = before - st.session_state.affection


# ==========================================
# 4-5. 장면별 배경 음악
#  calm 잔잔함 / tense 긴장 / sad 슬픔 / romance 설렘
#  sounds 폴더에 bgm_calm.mp3 같은 파일을 넣으면 그 곡으로 바뀜
# ==========================================
DAY_TRACK = {}
for _d in (1, 2, 3, 5, 6, 10, 12, 16):
    DAY_TRACK[_d] = "calm"
for _d in (7, 13, 18, 21, 22, 25, 26):
    DAY_TRACK[_d] = "tense"
for _d in (4, 9, 11, 23, 24):
    DAY_TRACK[_d] = "sad"
for _d in (8, 14, 15, 17, 19, 20, 27, 28, 29, 30):
    DAY_TRACK[_d] = "romance"


# ==========================================
# 4-6. 선물·데이트 이벤트 (정해진 날이 끝난 뒤 주말에 한 번씩)
#  세라피나의 취향은 이야기 속에 힌트가 있음:
#   온실에서 몰래 꽃을 키움 / 너무 단 건 싫어함 / 오래된 문양·책을 좋아함 /
#   사람 많은 곳·화려한 장신구(가문 생각이 남)는 싫어함 / '서리 아래 피는 붉은 꽃' = 포인센티아
# ==========================================
EVENTS = {
    6: {"title": "주말 선물 고르기", "bg": "bg_01", "place": "주말의 마을 상점가",
        "desc": "첫 주말. 온실을 나와 마을 상점가를 걷다가, 세라피나에게 작은 선물을 하나 사 가기로 했다. 무엇을 고를까?",
        "track": "calm",
        "options": [
            F("작은 화분에 담긴 겨울 마법 꽃 씨앗", {"aff": +10, "tru": +5},
              "세라피나가 화분을 받아 들고 한참 들여다봅니다. '...온실 일, 기억하고 있었구나.' 입꼬리가 숨김없이 올라가요."),
            F("덜 달게 만든 코코아 가루 한 통", {"aff": +6, "tru": +3},
              "'...이건 좀 괜찮네.' 세라피나가 통을 가방에 소중히 넣습니다."),
            F("반짝이는 루비 머리핀", {"aff": -4},
              "'이런 건 집에 산더미야.' 화려한 장신구는 가문을 떠올리게 하는지 세라피나가 시큰둥합니다."),
            F("불꽃 기숙사 응원 목도리", {"aff": -5, "dist": +3},
              "'지금 나한테 이걸 하라고?' 서리 기숙사 애들이 보면 큰일 난다며 세라피나가 질색합니다."),
        ]},
    13: {"title": "주말 데이트 장소 고르기", "bg": "bg_12", "place": "눈 덮인 정원",
         "desc": "에단과 헤어지고 돌아서는데, 세라피나가 '오늘... 시간 있어?'라고 먼저 물어 왔다. 어디로 가자고 할까?",
         "desc_far": "주말 오후다. 용기를 내서 세라피나에게 같이 가자고 말해 볼 생각이다. 그녀가 따라와 줄 만한 곳은 어디일까?",
         "track": "romance",
         "options": [
             F("도서관 봉인 서고에서 같이 오래된 문양 풀기", {"aff": +10, "tru": +6, "clue": +1},
               "촛불 아래 머리를 맞댄 오후. 세라피나가 '너랑 하니까 금방 풀리네'라며 웃습니다."),
             F("사람 없는 한적한 온실", {"aff": +8, "tru": +5},
               "아무도 없는 온실에서 세라피나가 처음으로 꽃 이름을 하나하나 알려 줍니다."),
             F("사람으로 북적이는 마을 사탕 가게", {"aff": -4},
               "인파에 떠밀리던 세라피나가 '사람 많은 데 질색이라고!'라며 먼저 돌아갑니다. 사탕도 너무 달았대요."),
             F("빗자루 경기 불꽃 기숙사 응원석", {"aff": -5, "dist": +3},
               "불꽃 기숙사 응원석 한가운데라니. 세라피나가 후드를 푹 눌러쓴 채 경기 내내 한마디도 하지 않습니다."),
         ]},
    20: {"title": "특별한 선물 고르기", "bg": "bg_10", "place": "고요한 연구실",
         "desc": "소문 때문에 어색해진 주말. 그래도 세라피나에게 마음을 담은 선물을 건네 보기로 했다.",
         "desc_far": "세라피나와의 거리는 아직 먼데, 소문까지 돌고 있다. 작은 선물로라도 마음을 전해 볼까?",
         "track": "romance",
         "options": [
             dict(F("포인센티아 꽃 한 송이", {"aff": +12, "tru": +6},
                    "'서리 아래 피는 붉은 꽃...' 가문 기록의 문양을 기억해 준 걸 알고, 세라피나의 눈가가 붉어집니다."),
                  need="saw_record",
                  alt={"s": {"aff": +6, "tru": +3},
                       "r": "세라피나가 꽃을 받아 들고 잠시 멈칫합니다. '...포인센티아네. 우리 집 문양에 그려진 꽃이야.' 우연이라기엔 묘한 표정이에요."}),
             F("직접 쓴 짧은 편지", {"aff": +8, "tru": +8},
               "세라피나가 편지를 몇 번이고 다시 읽고는 '...글씨 엉망이야'라며 웃습니다."),
             F("유명 상점의 비싼 향수", {"aff": -4},
               "'우리 어머니가 쓰는 향이야.' 세라피나의 표정이 묘하게 굳습니다."),
             F("'내 짝꿍에게'라고 크게 적은 반짝이 카드", {"aff": -3, "dist": +3},
               "세라피나가 카드를 재빨리 주머니에 숨깁니다. '누가 보면 어쩌려고!'"),
         ]},
    27: {"title": "마지막 주말 데이트", "bg": "bg_02", "place": "달빛 아래 성",
         "desc": "약속한 30일이 얼마 남지 않았다. 둘만의 마지막 주말, 어디로 갈까?",
         "desc_far": "약속한 30일이 얼마 남지 않았다. 마지막으로 한 번만 같이 가 달라고 세라피나에게 부탁해 볼까?",
         "track": "romance",
         "options": [
             dict(F("버드나무가 있는 호숫가를 함께 걷기", {"aff": +10, "tru": +8},
                    "버드나무 아래에서 세라피나가 말합니다. '여기서 처음으로 너한테 기댔었지.'"),
                  need="lake_bond",
                  alt={"s": {"aff": +6, "tru": +5},
                       "r": "버드나무 아래를 걷던 세라피나가 말합니다. '여기, 혼자 자주 오던 곳이야. ...누구랑 같이 온 건 처음이네.'"}),
             F("천문탑에서 별 보기", {"aff": +8, "tru": +6},
               "별을 세던 세라피나가 '30일이 지나도 또 오자'며 새끼손가락을 내밉니다."),
             F("전교생이 모이는 겨울 무도회", {"aff": -5},
               "연회장 사건 이후 사람들의 시선이 아직 따갑습니다. 세라피나가 무도회장 입구에서 발길을 돌려요."),
             F("윈터번 저택에 인사하러 가자고 하기", {"aff": -6, "tru": -4},
               "'...지금? 우리 집이 어떤 곳인지 알면서?' 너무 앞서 나간 제안에 세라피나가 당황합니다."),
         ]},
}


# ==========================================
# 4-7. 에필로그 (엔딩 뒤 '몇 년 후' 이야기)
# ==========================================
# 결혼식 그림이 나오는 엔딩의 에필로그 글
WEDDING_EPILOGUE = {
    1: ("5년 후 · 첫눈이 내리던 날",
        "별이 쏟아지는 천문탑 아래에서 두 사람은 결혼식을 올렸습니다. 붉은 포인센티아와 흰 장미 사이로, "
        "하얀 드레스를 입은 세라피나가 당신에게 손을 내밉니다. '앞으로도... 내 곁에 있어, 알겠지?' "
        "장난 같은 내기로 시작된 30일은, 그렇게 평생의 약속이 되었습니다."),
    2: ("3년 후 · 다시 겨울",
        "몇 번이나 엇갈리고, 몇 번이나 다시 손을 잡은 끝에 세라피나는 하얀 드레스를 입고 당신 앞에 섰습니다. "
        "'그때 그 내기, 네가 이긴 걸로 해 줄게. 대신 평생 갚아.' "
        "누구보다 어렵게 시작한 30일이, 둘에게는 가장 소중한 시작이 되었습니다."),
}

EPILOGUE = {
    1: "5년 후, 눈 내리는 애시포드의 졸업생 모임. 세라피나는 가문의 이름 대신 자기 이름으로 연금술 연구소를 열었고, "
       "연구소 창가에는 해마다 포인센티아가 핀다. 사람들이 둘의 첫 만남을 물으면, 세라피나는 언제나 웃으며 말한다. "
       "'처음엔 내기였대. 근데 결국 내가 이겼지.'",
    2: "3년 후 겨울, 세라피나는 여전히 새침하지만 이제는 누구 앞에서도 당신의 손을 놓지 않는다. "
       "가문과의 갈등은 아직 다 풀리지 않았지만, 둘은 함께라면 괜찮다는 걸 알고 있다.",
    3: "졸업 후에도 둘은 매년 첫눈이 오는 날 천문탑 아래에서 만난다. 연인은 아니지만, 서로의 가장 오래된 비밀을 아는 단 한 사람. "
       "어쩌면 언젠가, 그 이름이 바뀔지도 모른다.",
    4: "둘은 함께하지만, 세라피나는 가끔 당신의 편지를 오래 들여다보며 행간을 의심한다. "
       "좋아하는 마음과 믿지 못하는 마음 사이에서, 둘의 겨울은 아직 끝나지 않았다.",
    5: "졸업식 날, 복도에서 세라피나와 스쳐 지나간다. 그녀는 잠깐 걸음을 늦췄지만 돌아보지는 않았다. "
       "그해 겨울의 30일은 그렇게, 눈처럼 조용히 녹아 사라졌다.",
    6: "몇 년 뒤 신문에서 세라피나의 정략결혼 소식을 읽는다. 사진 속 그녀는 완벽하게 웃고 있지만, "
       "당신은 그 미소가 얼마나 차가운지 누구보다 잘 안다.",
}


def choice_order(day, opts):
    """쉬움·보통: 어제 선택에서 이어지는 '↪' 선택지를 맨 위에
    어려움: 판마다·날마다 순서를 섞음 (새로고침해도 같은 순서)"""
    opts = list(opts)
    if DIFFICULTY[st.session_state.difficulty]["shuffle"]:
        random.Random(f"{st.session_state.run_id}-{day}").shuffle(opts)
    else:
        opts.sort(key=lambda o: not o["follow"])
    return opts


# ==========================================
# 4-3. 사운드
#  - 이 폴더(또는 sounds 폴더)에 아래 이름의 파일을 넣으면 그 소리가 나옵니다.
#      bgm_title.mp3   : 이름 입력 화면 배경 음악 (반복 재생)
#      sound_happy.mp3 : 해피 엔딩 축하 소리
#      sound_bad.mp3   : 배드 엔딩 게임 종료 소리
#    (.mp3 / .ogg / .wav / .m4a 모두 가능)
#  - 파일이 없으면 게임이 직접 만든 음악·효과음이 나옵니다.
#  - 브라우저 정책 때문에, 화면을 한 번 클릭하거나 키를 누른 뒤부터 소리가 납니다.
# ==========================================
SOUND_MIME = {"mp3": "audio/mpeg", "ogg": "audio/ogg", "wav": "audio/wav", "m4a": "audio/mp4"}


def find_sound(name):
    for d in SEARCH_DIRS:
        for ext in SOUND_MIME:
            path = os.path.join(d, f"{name}.{ext}")
            if os.path.exists(path):
                return path
    return None


@st.cache_data(show_spinner=False)
def _sound_uri(path, mtime):
    ext = path.rsplit(".", 1)[-1].lower()
    with open(path, "rb") as f:
        return f"data:{SOUND_MIME[ext]};base64," + base64.b64encode(f.read()).decode()


def sound_uri(name):
    path = find_sound(name)
    return _sound_uri(path, os.path.getmtime(path)) if path else None


AUDIO_MANAGER_JS = r"""
window.PoinAudio = (function () {
  var A = {ctx: null, master: null, music: null, sfxOut: null, bus: null, el: null, elBase: 1,
           timer: null, scene: null, token: null, pending: null, muted: false, btn: null,
           musicVol: 0.8, sfxVol: 0.8, sfxToken: null};
  try { A.muted = localStorage.getItem('poin_muted') === '1'; } catch (e) {}

  function ctx() {
    if (!A.ctx) {
      var C = window.AudioContext || window.webkitAudioContext;
      A.ctx = new C();
      A.master = A.ctx.createGain(); A.master.gain.value = A.muted ? 0 : 1;
      A.master.connect(A.ctx.destination);
      A.music = A.ctx.createGain(); A.music.gain.value = A.musicVol; A.music.connect(A.master);
      A.sfxOut = A.ctx.createGain(); A.sfxOut.gain.value = A.sfxVol; A.sfxOut.connect(A.master);
    }
    return A.ctx;
  }
  function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }

  // ================= 악기 =================
  function newBus(vol, echo, out) {
    var c = ctx(), g = c.createGain();
    g.gain.value = vol; g.connect(out || A.music);
    if (echo) {
      var d = c.createDelay(1.0), fb = c.createGain(), wet = c.createGain();
      d.delayTime.value = 0.32; fb.gain.value = 0.3; wet.gain.value = 0.25;
      g.connect(d); d.connect(fb); fb.connect(d); d.connect(wet); wet.connect(out || A.music);
    }
    return g;
  }
  function env(g, t, vol, atk, dur) {
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + atk);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  }
  var V = {
    bell: function (bus, m, t, dur, vol) {          // 오르골 종소리
      var c = ctx(), f = hz(m);
      [[1, 1], [2, 0.28], [3.01, 0.07]].forEach(function (p) {
        var o = c.createOscillator(), g = c.createGain();
        o.type = 'sine'; o.frequency.value = f * p[0];
        env(g, t, vol * p[1], 0.008, dur);
        o.connect(g); g.connect(bus); o.start(t); o.stop(t + dur + 0.05);
      });
    },
    pluck: function (bus, m, t, dur, vol) {         // 하프 같은 뜯는 소리
      var c = ctx(), o = c.createOscillator(), o2 = c.createOscillator(), g = c.createGain();
      o.type = 'triangle'; o.frequency.value = hz(m);
      o2.type = 'sine'; o2.frequency.value = hz(m) * 2;
      var g2 = c.createGain(); g2.gain.value = 0.25;
      env(g, t, vol, 0.005, Math.min(dur, 0.9));
      o.connect(g); o2.connect(g2); g2.connect(g); g.connect(bus);
      o.start(t); o2.start(t); o.stop(t + 1); o2.stop(t + 1);
    },
    dark: function (bus, m, t, dur, vol) {          // 어두운 저음 반복
      var c = ctx(), o = c.createOscillator(), lp = c.createBiquadFilter(), g = c.createGain();
      o.type = 'sawtooth'; o.frequency.value = hz(m);
      lp.type = 'lowpass'; lp.frequency.value = 700;
      env(g, t, vol, 0.01, Math.min(dur, 0.35));
      o.connect(lp); lp.connect(g); g.connect(bus); o.start(t); o.stop(t + 0.4);
    },
    pad: function (bus, m, t, dur, vol) {           // 은은하게 깔리는 화음
      var c = ctx(), lp = c.createBiquadFilter(), g = c.createGain();
      lp.type = 'lowpass'; lp.frequency.value = 1100;
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol, t + Math.min(0.6, dur / 3));
      g.gain.setValueAtTime(vol, t + dur * 0.75);
      g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      [-6, 6].forEach(function (cents) {
        var o = c.createOscillator(); o.type = 'sawtooth';
        o.frequency.value = hz(m); o.detune.value = cents;
        o.connect(lp); o.start(t); o.stop(t + dur + 0.05);
      });
      lp.connect(g); g.connect(bus);
    },
    bass: function (bus, m, t, dur, vol) {
      var c = ctx(), o = c.createOscillator(), g = c.createGain();
      o.type = 'sine'; o.frequency.value = hz(m);
      env(g, t, vol, 0.01, dur);
      o.connect(g); g.connect(bus); o.start(t); o.stop(t + dur + 0.05);
    }
  };
  function brass(bus, m, t, dur, vol, bendTo) {     // 금관 (엔딩용)
    var c = ctx(), o = c.createOscillator(), o2 = c.createOscillator();
    var lp = c.createBiquadFilter(), g = c.createGain(), lfo = c.createOscillator(), lg = c.createGain();
    o.type = 'sawtooth'; o2.type = 'square';
    o.frequency.setValueAtTime(hz(m), t); o2.frequency.setValueAtTime(hz(m) * 1.003, t);
    if (bendTo) {
      o.frequency.exponentialRampToValueAtTime(hz(bendTo), t + dur);
      o2.frequency.exponentialRampToValueAtTime(hz(bendTo), t + dur);
    }
    lfo.frequency.value = 5.5; lg.gain.value = hz(m) * 0.012;
    lfo.connect(lg); lg.connect(o.frequency); lg.connect(o2.frequency);
    lp.type = 'lowpass'; lp.frequency.setValueAtTime(900, t);
    lp.frequency.linearRampToValueAtTime(2600, t + 0.06);
    lp.frequency.linearRampToValueAtTime(1500, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.03);
    g.gain.setValueAtTime(vol, t + Math.max(0.04, dur - 0.12));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur + 0.08);
    o.connect(lp); o2.connect(lp); lp.connect(g); g.connect(bus);
    [o, o2, lfo].forEach(function (x) { x.start(t); x.stop(t + dur + 0.12); });
  }
  function thud(bus, t, vol) {
    var c = ctx(), o = c.createOscillator(), g = c.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(110, t); o.frequency.exponentialRampToValueAtTime(38, t + 0.6);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.7);
    o.connect(g); g.connect(bus); o.start(t); o.stop(t + 0.75);
  }

  // ================= 배경 음악 (모두 이 게임을 위해 새로 지은 곡) =================
  var CH = {
    Dm: [50, 57, 62, 65, 69], Bb: [46, 53, 58, 62, 65], Gm: [43, 50, 55, 58, 62], A: [45, 52, 57, 61, 64],
    F: [41, 48, 53, 57, 60], C: [48, 55, 60, 64, 67], D: [50, 57, 62, 66, 69], Bm: [47, 54, 59, 62, 66],
    G: [43, 50, 55, 59, 62], Am: [45, 52, 57, 60, 64], E: [40, 47, 52, 56, 59], Em: [40, 47, 52, 55, 59]
  };
  var TRACKS = {
    // 이름 입력 화면: 겨울 오르골 왈츠
    title: {beat: 0.62, meter: 3, echo: true, vol: 0.8,
      prog: ['Dm', 'Dm', 'Bb', 'Bb', 'Gm', 'Gm', 'A', 'A', 'Dm', 'F', 'Bb', 'C', 'Gm', 'A', 'Dm', 'Dm'],
      arp: {voice: 'bell', pattern: [0, 1, 2, 3, 4, 3], step: 0.5, tr: 12, vol: 0.07, dur: 1.6},
      melVoice: 'bell', melVol: 0.16,
      mel: [[[81, 2], [77, 1]], [[76, 1], [77, 1], [74, 1]], [[74, 2], [77, 1]], [[77, 1.5], [76, 0.5], [74, 1]],
            [[79, 2], [82, 1]], [[81, 1], [79, 1], [77, 1]], [[76, 2], [73, 1]], [[76, 3]],
            [[81, 2], [86, 1]], [[84, 1], [81, 1], [77, 1]], [[77, 1.5], [79, 0.5], [81, 1]], [[79, 2], [76, 1]],
            [[82, 1], [81, 1], [79, 1]], [[76, 1.5], [77, 0.5], [73, 1]], [[74, 3]], [[0, 2], [69, 1]]]},
    // 평소 학교생활: 잔잔하고 밝은 곡
    calm: {beat: 0.65, meter: 4, echo: true, vol: 1.1,
      prog: ['D', 'A', 'Bm', 'G', 'D', 'A', 'G', 'A'],
      arp: {voice: 'pluck', pattern: [0, 2, 3, 4, 3, 2, 1, 2], step: 0.5, tr: 12, vol: 0.06, dur: 0.8},
      bass: {beats: [0, 2], vol: 0.11, len: 1.8},
      melVoice: 'bell', melVol: 0.12,
      mel: [[[78, 1], [76, 1], [74, 2]], [[73, 1], [74, 1], [76, 2]], [[78, 1.5], [79, 0.5], [78, 1], [76, 1]], [[74, 4]],
            [[74, 1], [76, 1], [78, 1], [81, 1]], [[79, 2], [76, 2]], [[78, 1], [76, 1], [74, 1], [71, 1]], [[73, 2], [0, 2]]]},
    // 다툼·위기: 긴장되는 곡
    tense: {beat: 0.42, meter: 4, echo: false, vol: 0.7,
      prog: ['Dm', 'Dm', 'Bb', 'Bb', 'Gm', 'Gm', 'A', 'A'],
      arp: {voice: 'dark', pattern: [0, 0, 1, 0, 2, 0, 1, 0], step: 0.5, tr: 0, vol: 0.09, dur: 0.3},
      pad: {vol: 0.022, tr: 0},
      bass: {beats: [0, 1, 2, 3], vol: 0.09, len: 0.8},
      melVoice: 'bell', melVol: 0.1,
      mel: [[[0, 4]], [[0, 2], [81, 2]], [[0, 4]], [[0, 2], [82, 2]], [[0, 4]], [[0, 2], [79, 2]], [[0, 4]], [[0, 2], [85, 2]]]},
    // 슬픈 장면: 느리고 쓸쓸한 곡
    sad: {beat: 0.9, meter: 4, echo: true, vol: 0.8,
      prog: ['Am', 'F', 'C', 'E', 'Am', 'Dm', 'E', 'Am'],
      arp: {voice: 'bell', pattern: [0, 2, 3, 4], step: 1, tr: 12, vol: 0.045, dur: 2.2},
      pad: {vol: 0.03, tr: 0},
      melVoice: 'bell', melVol: 0.13,
      mel: [[[76, 2], [72, 2]], [[72, 1], [74, 1], [72, 2]], [[67, 2], [72, 2]], [[71, 3], [0, 1]],
            [[76, 2], [79, 1], [77, 1]], [[77, 2], [74, 2]], [[71, 1], [74, 1], [68, 2]], [[69, 4]]]},
    // 설레는 장면: 따뜻한 곡
    romance: {beat: 0.7, meter: 4, echo: true, vol: 0.8,
      prog: ['F', 'Am', 'Bb', 'C', 'Dm', 'Bb', 'Gm', 'C'],
      arp: {voice: 'pluck', pattern: [0, 2, 3, 4, 3, 2, 3, 4], step: 0.5, tr: 12, vol: 0.05, dur: 0.8},
      pad: {vol: 0.02, tr: 0},
      bass: {beats: [0, 2], vol: 0.1, len: 1.8},
      melVoice: 'bell', melVol: 0.14,
      mel: [[[72, 1.5], [74, 0.5], [76, 2]], [[76, 1], [77, 1], [76, 1], [72, 1]], [[74, 2], [77, 2]], [[76, 3], [0, 1]],
            [[77, 1.5], [79, 0.5], [81, 2]], [[79, 1], [77, 1], [74, 2]], [[74, 1], [76, 1], [77, 1], [79, 1]], [[76, 4]]]}
  };
  // (위에 이어서) 해피 엔딩 에필로그: 종소리가 울리는 밝은 축하 왈츠
  TRACKS.wedding = {beat: 0.48, meter: 3, echo: true, vol: 0.9,
      prog: ['C', 'G', 'Am', 'F', 'C', 'G', 'F', 'G', 'C', 'Em', 'F', 'C', 'Dm', 'G', 'C', 'C'],
      arp: {voice: 'pluck', pattern: [0, 2, 3, 4, 3, 2], step: 0.5, tr: 12, vol: 0.055, dur: 0.8},
      bass: {beats: [0], vol: 0.12, len: 2.6},
      pad: {vol: 0.016, tr: 12},
      melVoice: 'bell', melVol: 0.17,
      mel: [[[76, 2], [79, 1]], [[79, 1], [77, 1], [74, 1]], [[72, 2], [76, 1]], [[77, 3]],
            [[79, 1], [81, 1], [79, 1]], [[77, 1], [76, 1], [74, 1]], [[76, 1], [77, 1], [81, 1]], [[79, 3]],
            [[84, 2], [83, 1]], [[83, 1], [81, 1], [79, 1]], [[81, 2], [77, 1]], [[79, 2], [76, 1]],
            [[77, 1], [76, 1], [74, 1]], [[74, 1], [76, 1], [77, 1]], [[72, 3]], [[0, 2], [67, 1]]]};
  var BUILT = {};
  function build(name) {
    if (BUILT[name]) return BUILT[name];
    var tr = TRACKS[name], ev = [], barLen = tr.meter * tr.beat;
    tr.prog.forEach(function (chord, bar) {
      var t0 = bar * barLen, tones = CH[chord];
      if (tr.arp) {
        var a = tr.arp, n = Math.round(tr.meter / a.step);
        for (var i = 0; i < n; i++) {
          ev.push([t0 + i * a.step * tr.beat, a.voice, tones[a.pattern[i % a.pattern.length]] + (a.tr || 0), a.dur, a.vol]);
        }
      }
      if (tr.pad) [1, 2, 3].forEach(function (k) { ev.push([t0, 'pad', tones[k] + (tr.pad.tr || 0), barLen * 1.02, tr.pad.vol]); });
      if (tr.bass) tr.bass.beats.forEach(function (b) { ev.push([t0 + b * tr.beat, 'bass', tones[0] - 12, tr.beat * tr.bass.len, tr.bass.vol]); });
      if (tr.mel) {
        var tt = t0;
        tr.mel[bar].forEach(function (nn) {
          if (nn[0]) ev.push([tt, tr.melVoice, nn[0], Math.max(1.2, nn[1] * tr.beat * 1.5), tr.melVol]);
          tt += nn[1] * tr.beat;
        });
      }
    });
    ev.sort(function (x, y) { return x[0] - y[0]; });
    BUILT[name] = {ev: ev, loop: tr.prog.length * barLen};
    return BUILT[name];
  }
  function startLoop(name) {
    var c = ctx(), tr = TRACKS[name], song = build(name);
    var bus = newBus(0.0001, tr.echo), start = c.currentTime + 0.1, idx = 0, loop = 0;
    bus.gain.exponentialRampToValueAtTime(tr.vol, start + 1.5);
    A.bus = bus;
    A.timer = setInterval(function () {
      var horizon = c.currentTime + 0.4;
      while (true) {
        var e = song.ev[idx], t = start + loop * song.loop + e[0];
        if (t > horizon) break;
        if (t > c.currentTime - 0.05) V[e[1]](bus, e[2], t, e[3], e[4]);
        idx++;
        if (idx >= song.ev.length) { idx = 0; loop++; }
      }
    }, 100);
  }

  // ================= 엔딩 소리 =================
  function startHappy() {
    var c = ctx(), bus = newBus(0.55, true), t = c.currentTime + 0.05;
    A.bus = bus;
    [[67, 0.13], [72, 0.13], [76, 0.13], [79, 0.13], [84, 0.42]].forEach(function (n) { brass(bus, n[0], t, n[1], 0.18); t += n[1]; });
    t += 0.08;
    [[77, 81, 84], [79, 83, 86]].forEach(function (chord) { chord.forEach(function (m) { brass(bus, m, t, 0.3, 0.11); }); t += 0.34; });
    [72, 76, 79, 84].forEach(function (m) { brass(bus, m, t, 1.9, 0.10); });
    thud(bus, t, 0.5);
    var sp = [84, 86, 88, 91, 93, 96, 98, 100];
    for (var i = 0; i < 26; i++) V.bell(bus, sp[Math.floor(Math.random() * sp.length)], t + 0.05 + i * 0.11 + Math.random() * 0.05, 0.9, 0.07);
  }
  // 노멀 엔딩: 따뜻하지만 조금 아쉬운 오르골 (끝이 열린 화음)
  function startNormal() {
    var c = ctx(), bus = newBus(0.6, true), t = c.currentTime + 0.05;
    A.bus = bus;
    [[72, 0.32], [76, 0.32], [79, 0.32], [84, 0.6], [83, 0.32], [79, 0.32], [81, 0.9]].forEach(function (n) {
      V.bell(bus, n[0], t, 1.8, 0.14); t += n[1];
    });
    [53, 57, 60, 64].forEach(function (m) { V.pad(bus, m, t - 1.2, 3.2, 0.03); });
    V.bell(bus, 77, t, 2.6, 0.12);
  }
  // 씁쓸한 엔딩: 단조 화음 위로 내려가는 종소리, 끝내 풀리지 않음
  function startBitter() {
    var c = ctx(), bus = newBus(0.6, true), t = c.currentTime + 0.05;
    A.bus = bus;
    [45, 52, 57, 60].forEach(function (m) { V.pad(bus, m, t, 4.2, 0.032); });
    [[81, 0.45], [79, 0.45], [76, 0.45], [74, 0.7], [72, 0.45], [71, 1.4]].forEach(function (n) {
      V.bell(bus, n[0], t, 2.0, 0.13); t += n[1];
    });
    V.bass(bus, 41, t - 0.6, 2.6, 0.12);
  }
  // 최악의 엔딩: 게임 종료 소리 + 길게 깔리는 낮은 울림
  function startWorst() {
    startBad();
    var c = ctx(), t = c.currentTime + 1.4;
    [33, 40, 45].forEach(function (m) { V.pad(A.bus, m, t, 4.5, 0.04); });
  }
  function startBad() {
    var c = ctx(), bus = newBus(0.6, false), t = c.currentTime + 0.05;
    A.bus = bus;
    thud(bus, t, 0.7);
    [[55, 0.42], [54, 0.42], [53, 0.42]].forEach(function (n) { brass(bus, n[0], t, n[1] - 0.04, 0.16); t += n[1]; });
    brass(bus, 52, t, 1.6, 0.17, 47);
    thud(bus, t + 1.5, 0.6);
  }

  // ================= 효과음 =================
  function sfx(kind) {
    var c = ctx();
    if (c.state !== 'running') return;
    var t = c.currentTime + 0.01, bus = newBus(1, false, A.sfxOut);
    if (kind === 'click') {
      var o = c.createOscillator(), g = c.createGain();
      o.type = 'sine'; o.frequency.setValueAtTime(1500, t); o.frequency.exponentialRampToValueAtTime(900, t + 0.05);
      env(g, t, 0.12, 0.003, 0.07); o.connect(g); g.connect(bus); o.start(t); o.stop(t + 0.1);
    } else if (kind === 'up') {
      V.bell(bus, 88, t, 0.9, 0.12); V.bell(bus, 95, t + 0.1, 1.1, 0.12); V.bell(bus, 100, t + 0.2, 1.2, 0.08);
    } else if (kind === 'down') {
      V.pluck(bus, 62, t, 0.5, 0.2); V.pluck(bus, 57, t + 0.16, 0.7, 0.2);
    } else if (kind === 'trap') {
      brass(bus, 58, t, 0.5, 0.11, 46); thud(bus, t, 0.55); V.dark(bus, 46, t + 0.05, 0.3, 0.15);
    }
  }

  // ================= 재생 관리 =================
  function stopCurrent() {
    if (A.timer) { clearInterval(A.timer); A.timer = null; }
    if (A.bus && A.ctx) {
      var b = A.bus, now = A.ctx.currentTime;
      try {
        b.gain.cancelScheduledValues(now);
        b.gain.setValueAtTime(Math.max(b.gain.value, 0.0001), now);
        b.gain.exponentialRampToValueAtTime(0.0001, now + 0.8);
      } catch (e) {}
      setTimeout(function () { try { b.disconnect(); } catch (e) {} }, 1000);
      A.bus = null;
    }
    if (A.el) {
      var el = A.el, v = el.volume; A.el = null;
      var fade = setInterval(function () {
        v -= 0.08;
        if (v <= 0) { clearInterval(fade); el.pause(); el.src = ''; } else { el.volume = v; }
      }, 60);
    }
  }
  function startNow(cmd) {
    if (cmd.src) {
      var el = new Audio(cmd.src), once = ['happy', 'bad', 'normal', 'bitter', 'worst'].indexOf(cmd.scene) >= 0;
      el.loop = !once; A.elBase = once ? 0.9 : 0.6;
      el.volume = Math.min(1, A.elBase * A.musicVol); el.muted = A.muted;
      A.el = el;
      el.play().catch(function () { if (A.el === el) { A.el = null; A.pending = cmd; } });
      return;
    }
    if (cmd.scene === 'happy') startHappy();
    else if (cmd.scene === 'bad') startBad();
    else if (cmd.scene === 'normal') startNormal();
    else if (cmd.scene === 'bitter') startBitter();
    else if (cmd.scene === 'worst') startWorst();
    else if (TRACKS[cmd.scene]) startLoop(cmd.scene);
  }
  function tryStart(cmd) {
    if (cmd.src) { startNow(cmd); return; }
    var c = ctx();
    if (c.state === 'running') { startNow(cmd); return; }
    A.pending = cmd;
    c.resume().then(function () {
      if (A.pending === cmd && c.state === 'running') { A.pending = null; startNow(cmd); }
    }).catch(function () {});
  }
  function unlock(ev) {
    var c = ctx();
    if (c.state !== 'running') c.resume();
    if (A.pending && A.pending.scene === A.scene) { var p = A.pending; A.pending = null; startNow(p); }
    if (ev && ev.type === 'pointerdown' && ev.target && ev.target.closest &&
        ev.target.closest('.stButton button, .ep-replay')) sfx('click');
  }
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (e) { document.addEventListener(e, unlock, true); });

  function setVolumes(mv, sv) {
    if (typeof mv === 'number') A.musicVol = mv;
    if (typeof sv === 'number') A.sfxVol = sv;
    if (A.music) A.music.gain.value = A.musicVol;
    if (A.sfxOut) A.sfxOut.gain.value = A.sfxVol;
    if (A.el) A.el.volume = Math.min(1, A.elBase * A.musicVol);
  }
  function setMuted(m) {
    A.muted = m;
    try { localStorage.setItem('poin_muted', m ? '1' : '0'); } catch (e) {}
    if (A.master) A.master.gain.value = m ? 0 : 1;
    if (A.el) A.el.muted = m;
    if (A.btn) A.btn.textContent = m ? '🔇' : '🔊';
  }
  function makeButton() {
    if (document.getElementById('poin-sound-btn')) return;
    var b = document.createElement('button');
    b.id = 'poin-sound-btn'; b.title = '소리 켜기/끄기';
    b.textContent = A.muted ? '🔇' : '🔊';
    b.style.cssText = 'position:fixed;right:18px;bottom:18px;z-index:999999;width:48px;height:48px;' +
      'border-radius:50%;border:1px solid #8b263e;background:rgba(7,13,20,0.85);color:#fff;' +
      'font-size:22px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,0.5);';
    b.addEventListener('click', function () { setMuted(!A.muted); });
    document.body.appendChild(b);
    A.btn = b;
  }
  makeButton();

  return {
    scene: function (cmd) {
      makeButton();
      setVolumes(cmd.musicVol, cmd.sfxVol);
      if (cmd.sfx && cmd.sfxToken && cmd.sfxToken !== A.sfxToken) {
        A.sfxToken = cmd.sfxToken;
        setTimeout(function () { sfx(cmd.sfx); }, 250);
      }
      if (cmd.scene === A.scene && cmd.token === A.token) return;
      stopCurrent();
      A.pending = null;
      A.scene = cmd.scene; A.token = cmd.token; A.lastCmd = cmd;
      if (cmd.scene === 'none') return;
      tryStart(cmd);
    },
    state: function () {
      return {scene: A.scene, token: A.token, pending: !!A.pending, muted: A.muted, musicVol: A.musicVol,
              sfxVol: A.sfxVol, ctx: A.ctx ? A.ctx.state : 'none', playingFile: !!A.el, synth: !!A.bus};
    },
    sfx: sfx,
    restart: function () {          // 에필로그 다시 보기: 노래도 처음부터
      if (!A.lastCmd || A.lastCmd.scene === 'none') return;
      stopCurrent(); A.pending = null; tryStart(A.lastCmd);
    },
    setMuted: setMuted
  };
})();
"""


def page_guard():
    """브라우저 자동 번역 막기.
    Streamlit 화면은 '영어 페이지'로 표시되어 있어서, 크롬·엣지가 한국어 글을
    다시 '한국어로 번역'하며 글을 뭉개고 화면 오류(removeChild)를 일으킵니다.
    페이지를 한국어로 표시하고 번역 금지 표시를 붙여 이를 막습니다."""
    components.html("""<script>
(function () {
  try {
    var d = window.parent.document, h = d.documentElement;
    h.setAttribute('lang', 'ko');
    h.setAttribute('translate', 'no');
    h.classList.add('notranslate');
    if (d.body) { d.body.setAttribute('translate', 'no'); d.body.classList.add('notranslate'); }
    if (!d.querySelector('meta[name="google"]')) {
      var m = d.createElement('meta'); m.name = 'google'; m.content = 'notranslate';
      d.head.appendChild(m);
    }
    // 에필로그 영상 안의 '에필로그 다시 보기' 버튼: 화면을 새로 불러오지 않고
    // 영상(애니메이션)과 노래를 처음부터 다시 재생
    if (!window.parent.__poinReplay) {
      var sc = d.createElement('script');
      sc.textContent = "window.__poinReplay = true;" +
        "document.addEventListener('click', function (e) {" +
        "  var b = e.target && e.target.closest && e.target.closest('.ep-replay'); if (!b) return;" +
        "  document.getAnimations().forEach(function (a) { try { a.cancel(); a.play(); } catch (x) {} });" +
        "  if (window.PoinAudio && window.PoinAudio.restart) window.PoinAudio.restart();" +
        "}, true);" +
        "document.addEventListener('click', function (e) {" +
        "  var g = e.target && e.target.closest && e.target.closest('.ep-goto'); if (!g) return;" +
        "  var btns = document.querySelectorAll('.stButton button');" +
        "  for (var i = 0; i < btns.length; i++) { if (btns[i].textContent.indexOf('에필로그 보기') >= 0) { btns[i].click(); break; } }" +
        "}, true);" +
        "document.addEventListener('click', function (e) {" +
        "  var box = e.target && e.target.closest && e.target.closest('.vn-box'); if (!box) return;" +
        "  var stage = box.closest('.stage');" +
        "  if (stage) stage.getAnimations({subtree: true}).forEach(function (a) { try { a.finish(); } catch (x) {} });" +
        "  document.querySelectorAll('.stButton, .choice-head').forEach(function (el) {" +
        "    el.getAnimations().forEach(function (a) { try { a.finish(); } catch (x) {} }); });" +
        "}, true);";
      d.head.appendChild(sc);
    }
  } catch (e) { console.log('[Poinsettia guard]', e); }
})();
</script>""", height=0)


def play_scene(scene, src=None, token="", sfx=None, sfx_token=None):
    """화면에 맞는 음악(과 효과음)을 틀어 달라고 브라우저에 알림.
    소리 관리자는 Streamlit 화면(부모 페이지)에 한 번만 심어 두어서,
    화면이 다시 그려져도 음악이 끊기거나 처음부터 다시 시작하지 않습니다.
    scene: title / calm / tense / sad / romance / happy / bad / none"""
    cmd = json.dumps({"scene": scene, "src": src, "token": token, "sfx": sfx, "sfxToken": sfx_token,
                      "musicVol": st.session_state.get("music_vol", 70) / 100,
                      "sfxVol": st.session_state.get("sfx_vol", 70) / 100})
    components.html(f"""<script>
(function () {{
  var P = window.parent;
  try {{
    if (!P.PoinAudio) {{
      var s = P.document.createElement('script');
      s.textContent = {json.dumps(AUDIO_MANAGER_JS)};
      P.document.head.appendChild(s);
    }}
    P.PoinAudio.scene({cmd});
  }} catch (e) {{ console.log('[Poinsettia audio]', e); }}
}})();
</script>""", height=0)


def play_track(track, sfx=None, sfx_token=None):
    """배경 음악 트랙 재생. sounds 폴더에 bgm_트랙이름.mp3 가 있으면 그 파일을 씀.
    판 번호가 바뀌면(다시 시작) 음악도 처음부터."""
    play_scene(track, sound_uri(f"bgm_{track}"), f"{track}-{st.session_state.run_id}", sfx, sfx_token)


# ==========================================
# 5. Ending Logic Evaluator (6 Endings)
# ==========================================
def evaluate_ending():
    aff = st.session_state.affection
    tru = st.session_state.trust
    dist = st.session_state.distance
    flags = st.session_state.flags
    clues = st.session_state.clues

    if clues >= 3 and flags.get("day23_honest") and aff >= 85 and tru >= 85:
        return {
            "id": 1,
            "title": "💍 Ending 1: 겨울의 끝에서, 평생의 약속 (True Ending)",
            "bg_color": "#1a3a2a",
            "desc": "눈 내리는 천문탑에서 고백을 들은 세라피나는 한참을 울다가 웃으며 대답했습니다. '30일이나 걸렸잖아, 바보야. ...나도 좋아.' "
                    "그 겨울 이후로도 둘의 이야기는 끝나지 않았습니다. 가문의 반대와 정략결혼의 그림자를 함께 넘어선 끝에, "
                    "세라피나는 별이 쏟아지는 밤 하얀 드레스를 입고 당신에게 손을 내밉니다. "
                    "장난 같은 내기로 시작된 30일은, 이제 평생의 약속이 되었습니다."
        }
    elif aff >= 80 and tru >= 70 and not flags.get("day23_defensive") and st.session_state.get("difficulty") == "어려움":
        return {
            "id": 2,
            "title": "💍 Ending 2: 얼음 공주의 첫 번째 봄 (Happy Ending)",
            "bg_color": "#2d1f3d",
            "desc": "고백을 들은 세라피나는 새빨개진 얼굴로 고개를 돌렸다가, 아주 작게 고개를 끄덕였습니다. '...이번 한 번만 믿어 줄게.' "
                    "가장 어려운 길을 끝까지 걸어온 당신에게, 그녀는 결국 마음을 전부 내주었습니다. "
                    "그리고 몇 년 뒤, 두 사람은 결혼식을 올립니다."
        }
    elif aff >= 80 and tru >= 70 and not flags.get("day23_defensive"):
        return {
            "id": 2,
            "title": "💖 Ending 2: 얼음 공주의 첫 번째 봄 (Happy Ending)",
            "bg_color": "#2d1f3d",
            "desc": "고백을 들은 세라피나는 새빨개진 얼굴로 고개를 돌렸다가, 아주 작게 고개를 끄덕였습니다. '...이번 한 번만 믿어 줄게.' "
                    "도도하던 서리 기숙사의 얼음 공주는 이제 전교생 앞에서도 당신의 손을 놓지 않습니다. "
                    "결혼을 말하기엔 아직 이르지만, 둘은 매년 첫눈이 오는 날 천문탑에서 같은 약속을 합니다. '내년 첫눈도, 같이.'"
        }
    elif flags.get("day23_defensive"):
        # 23일차에 끝까지 거짓말한 경우 → 이후 수치와 관계없이 최악의 엔딩
        return worst_ending()
    elif tru >= 70 and aff >= 50:
        return {
            "id": 3,
            "title": "🌿 Ending 3: 연인보다 깊은 단짝 (Normal Ending)",
            "bg_color": "#1c2d3d",
            "desc": "연인이 되지는 못했지만, 두 사람은 서로의 가장 깊은 비밀까지 나누는 둘도 없는 단짝이 되었습니다. 불꽃과 서리, 두 기숙사의 벽을 넘어선 특별한 우정입니다."
        }
    elif aff >= 70 and tru < 40:
        return {
            "id": 4,
            "title": "💔 Ending 4: 의심 속의 위태로운 사랑 (Bittersweet Ending)",
            "bg_color": "#3d2a1c",
            "desc": "세라피나는 당신을 진심으로 좋아하지만, 내기와 거짓말로 받은 상처 때문에 당신을 온전히 믿지 못합니다. 서로 좋아하면서도 끊임없이 의심하고 불안해하는 아슬아슬한 관계가 이어집니다."
        }
    elif dist >= 50:
        # 관계가 크게 틀어진 경우 → 최악의 엔딩
        return worst_ending()
    else:
        # 그 밖의 애매한 관계 → 스쳐 지나간 인연
        return {
            "id": 5,
            "title": "🧊 Ending 5: 스쳐 지나간 30일 (Bad Ending)",
            "bg_color": "#2b2b2b",
            "desc": "약속한 30일이 모두 지나갔습니다. 세라피나는 다시 차가운 서리 기숙사 귀족의 모습으로 돌아갔고, 복도에서 마주쳐도 무심한 눈빛으로 지나칠 뿐입니다. 두 사람의 인연은 여기서 끝이 납니다."
        }


def worst_ending():
    return {
        "id": 6,
        "title": "❄️ Ending 6: 굳게 닫힌 마음의 문 (Worst Ending)",
        "bg_color": "#3a1a1a",
        "desc": "거짓말과 변명에 깊이 실망한 세라피나는 당신을 완전히 외면했습니다. 그녀에게 당신은 이제 자기 마음을 짓밟은 사람으로만 기억될 것입니다."
    }

# ==========================================
# 6. Main App UI Rendering
# ==========================================

page_guard()   # 브라우저 자동 번역 때문에 글이 뭉개지고 오류가 나는 것을 막음

# Header
st.markdown(T("""
<div class="title-header">
<h1>포인센티아 (Poinsettia)</h1>
<p>애시포드 마법학원 로맨스 노벨 | 주인공 x 세라피나 윈터번</p>
</div>
"""), unsafe_allow_html=True)



# ==========================================
# 7. 선택 처리 · 반응 장면
# ==========================================
def settings_defaults():
    for k, v in (("music_vol", 70), ("sfx_vol", 70), ("text_speed", "보통"), ("hide_stats", False)):
        if k not in st.session_state:
            st.session_state[k] = v


def reaction_face(raw, aff_change, tru_change, trapped, day):
    """선택 결과에 맞는 세라피나 표정 그림 이름 (세라피나가 없는 날은 그날 인물)"""
    if day in DAY_OTHER and mood_for_day(day) is None:
        return DAY_OTHER[day], None
    base = seraphina_level("smile")
    if trapped:
        return "seraphina_30", "경계"
    if raw.get("aff", 0) < 0 or raw.get("tru", 0) < 0:
        lv = 30 if raw.get("dist", 0) > 0 else 20
        return f"seraphina_{lv}", LEVEL_LABEL[lv]
    if aff_change > 0 or tru_change > 0:
        lv = max(base, 60 if raw.get("aff", 0) >= 10 else 50)
        return f"seraphina_{lv}", LEVEL_LABEL[lv]
    return f"seraphina_{base}", LEVEL_LABEL[base]


# ==========================================
# 엔딩 연출 (노멀·씁쓸·배드·최악) 과 엔딩 소리
# ==========================================
ENDING_FX = {
    3: {"bg": "bg_15", "char": "seraphina_80", "fx": "warm", "fall": "snow", "sound": "normal",
        "line": "'친구라도 괜찮아. 너랑은... 오래 가고 싶으니까.'"},
    4: {"bg": "bg_18", "char": "seraphina_40", "fx": "bitter", "fall": "sleet", "sound": "bitter",
        "line": "'좋아해. ...그런데 왜 자꾸 네 말이 거짓말처럼 들릴까.'"},
    5: {"bg": "ending_sad", "char": None, "fx": "grey", "fall": "snow", "sound": "bad",
        "line": "복도에서 스쳐 지나가는 순간, 그녀는 잠깐 걸음을 늦췄지만 돌아보지 않았다."},
    6: {"bg": "bg_04", "char": "seraphina_10", "fx": "dark", "fall": "heavy", "sound": "worst",
        "line": "'다시는... 내 앞에 나타나지 마.'"},
}
ENDING_SOUND = {1: "happy", 2: "happy", 3: "normal", 4: "bitter", 5: "bad", 6: "worst"}

END_STYLE = """<style>
.end-stage{position:relative;width:100%;aspect-ratio:16/9;max-height:80vh;min-height:420px;overflow:hidden;
  border-radius:14px;border:1px solid #8b263e;background:#000;box-shadow:0 8px 25px rgba(0,0,0,.5);margin-bottom:14px}
.end-bg{position:absolute;inset:0;background-size:cover;background-position:center;animation:epZoom 12s ease-out both}
.end-char{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:100%;z-index:1;
  -webkit-mask-image:radial-gradient(ellipse 50% 62% at 50% 48%,#000 62%,transparent 100%);
  mask-image:radial-gradient(ellipse 50% 62% at 50% 48%,#000 62%,transparent 100%);animation:charIn 1.4s ease .3s both}
.end-fx{position:absolute;inset:0;z-index:2;pointer-events:none}
.fx-warm{background:radial-gradient(ellipse at 50% 30%,rgba(255,206,140,.32),transparent 65%);animation:epPulse 3s ease-in-out infinite alternate}
.fx-bitter{background:linear-gradient(180deg,rgba(40,60,110,.35),rgba(10,15,30,.55));animation:epStay 3s ease both}
.fx-dark{background:radial-gradient(ellipse at 50% 45%,transparent 25%,rgba(0,0,0,.92) 80%);animation:endDark 6s ease 1s both}
.grey .end-bg{animation:epZoom 12s ease-out both, endGrey 7s ease 1.5s both}
.dark .end-char{animation:charIn 1.2s ease .3s both, endVanish 4s ease 3.5s forwards}
.end-sleet{position:absolute;top:-10%;width:1.5px;height:38px;background:linear-gradient(transparent,rgba(200,220,255,.75));
  z-index:3;opacity:0;animation-name:endSleet;animation-timing-function:linear;animation-iteration-count:infinite;animation-fill-mode:backwards}
.end-line{position:absolute;left:5%;right:5%;bottom:8%;text-align:center;color:#fff;z-index:4;font-size:clamp(16px,2.4vh,24px);
  line-height:1.6;text-shadow:0 2px 10px #000,0 0 4px #000;animation:epStay 1.6s ease 2s both;opacity:0}
@keyframes endGrey{from{filter:grayscale(0) brightness(1)}to{filter:grayscale(1) brightness(.72)}}
@keyframes endDark{from{opacity:0}to{opacity:1}}
@keyframes endVanish{from{opacity:1}to{opacity:.12}}
@keyframes endSleet{0%{top:-10%;opacity:0;transform:translateX(0)}10%{opacity:.8}100%{top:110%;opacity:.8;transform:translateX(-80px)}}
</style>"""


def ending_stage(ending_id):
    """노멀·씁쓸·배드·최악 엔딩 화면 연출"""
    fx = ENDING_FX.get(ending_id)
    if not fx:
        return ""
    bg = image_uri(fx["bg"], 1672)
    char = image_uri(fx["char"], 1086) if fx["char"] else None
    rnd = random.Random(ending_id)
    fall = ""
    if fx["fall"] == "sleet":
        fall = "".join(f'<span class="end-sleet" style="left:{rnd.uniform(0, 110):.1f}%;'
                       f'animation-duration:{rnd.uniform(.7, 1.3):.2f}s;animation-delay:{rnd.uniform(0, 3):.2f}s;"></span>'
                       for _ in range(45))
    elif fx["fall"] in ("snow", "heavy"):
        fall = _falling(rnd, 0.5, 0, 22 if fx["fall"] == "snow" else 55, 6)
    line = T(fx["line"]).replace("{p}", html.escape(st.session_state.player_name))
    return (EP_STYLE + END_STYLE +
            f'<div class="end-stage {fx["fx"]}" style="animation:stageFade 1.4s ease-out both;">'
            f'<div class="end-bg" style="background-image:url(\'{bg}\');"></div>'
            + (f'<img class="end-char" src="{char}">' if char else "")
            + f'<div class="end-fx fx-{fx["fx"]}"></div>' + fall
            + f'<div class="end-line">{line}</div></div>')


REVIEW_TIPS = {
    "trap": "💡 함정은 '적극적이지만 때와 방법이 틀린' 선택이에요. 세라피나가 방금 한 말과 지금 두 사람의 거리를 먼저 생각해 보세요.",
    "clue": "💡 단서는 세라피나 가문의 비밀에 관심을 보이는 선택에서 얻어요. (5·8·10·15일, 13일 주말 데이트 등)",
    "honest": "💡 23일 '진실의 순간'에는 끝까지 솔직하게 고백해야 트루 엔딩으로 갈 수 있어요.",
    "lie": "💡 23일에 거짓말로 버티면 그 뒤로는 무엇을 해도 최악의 엔딩으로 이어져요.",
    "slow": "💡 실수가 없어도 호감도가 부족했다면, 대사에 담긴 세라피나의 마음(외로움, 가문의 압박, 비밀)을 챙기는 선택을 골라 보세요.",
}


def review_html(ending_id):
    """엔딩 화면의 '이번 판 돌아보기': 결정적 순간 + 트루 엔딩까지 부족했던 것 + 힌트"""
    ss = st.session_state
    hide = ss.get("hide_stats")
    moments = ss.get("moments", [])
    worst = sorted(moments, key=lambda m: (m["aff"] + m["tru"], m["day"]))[:5]
    worst.sort(key=lambda m: m["day"])

    need = []
    if ending_id != 1:
        if ss.affection < 85:
            need.append(f"호감도 {ss.affection} / 85")
        if ss.trust < 85:
            need.append(f"신뢰도 {ss.trust} / 85")
        if ss.clues < 3:
            need.append(f"단서 {ss.clues}개 / 3개")
        if not ss.flags.get("day23_honest"):
            need.append("23일 솔직한 고백")

    parts = ['<div class="review"><h3>🔍 이번 판 돌아보기</h3>']
    if ending_id == 1 and not moments:
        parts.append("<p class='rv-good'>✨ 함정도 실수도 없이 30일을 보냈어요. 완벽한 플레이예요!</p>")
    elif ending_id == 1:
        parts.append(f"<p class='rv-good'>✨ 트루 엔딩 달성! 실수 {len(moments)}번을 딛고 끝까지 해냈어요.</p>")
    if need:
        parts.append("<div class='rv-need'><b>트루 엔딩까지 부족했던 것</b><ul>"
                     + "".join(f"<li>{T(n)}</li>" for n in need) + "</ul></div>")
    if worst:
        parts.append("<b>결정적 순간</b><ol class='rv-list'>")
        for m in worst:
            tag = "🪤 함정" if m["trap"] else "💔 실수"
            when = f"{m['day']}일 주말" if m["event"] else f"{m['day']}일"
            nums = "" if hide else f" <span class='rv-num'>(호감도 {m['aff']:+d} · 신뢰도 {m['tru']:+d})</span>"
            parts.append(f"<li><span class='rv-tag'>{tag}</span> <b>{when}</b> ▶ {html.escape(T(m['choice']))}"
                         f"<div class='rv-why'>{m['why']}{nums}</div></li>")
        parts.append("</ol>")
        if len(moments) > len(worst):
            parts.append(f"<p class='rv-more'>그 밖의 실수 {len(moments) - len(worst)}번은 영향이 작아서 생략했어요.</p>")
    elif ending_id != 1:
        parts.append("<p>함정이나 큰 실수는 없었어요.</p>")

    tips = []
    if any(m["trap"] for m in moments):
        tips.append("trap")
    if ss.flags.get("day23_defensive"):
        tips.append("lie")
    elif ending_id != 1 and not ss.flags.get("day23_honest"):
        tips.append("honest")
    if ending_id != 1 and ss.clues < 3:
        tips.append("clue")
    if ending_id != 1 and not moments and ss.affection < 85:
        tips.append("slow")
    if tips:
        parts.append("<div class='rv-tips'>" + "".join(f"<p>{T(REVIEW_TIPS[t])}</p>" for t in tips) + "</div>")
    parts.append("</div>")
    style = ("<style>.review{background:rgba(13,27,20,.88);border:1px solid #1f3d2b;border-radius:12px;padding:18px 22px;"
             "margin:14px 0;color:#e2e8f0;line-height:1.7}.review h3{margin:0 0 10px 0;color:#fda4af}"
             ".rv-list{padding-left:1.3em}.rv-list li{margin-bottom:10px}.rv-why{color:#cbd5e1;font-size:.95rem}"
             ".rv-tag{font-size:.82rem;background:rgba(248,113,113,.18);color:#fca5a5;padding:1px 8px;border-radius:10px}"
             ".rv-num{color:#fda4af;font-size:.88rem}.rv-need{background:rgba(127,29,29,.25);border-radius:10px;"
             "padding:8px 14px;margin-bottom:12px}.rv-need ul{margin:4px 0 0 0}.rv-tips{border-top:1px dashed #3f5a4a;"
             "margin-top:10px;padding-top:8px;color:#fde68a}.rv-tips p{margin:4px 0}.rv-good{color:#6ee7b7;font-weight:bold}"
             ".rv-more{color:#94a3b8;font-size:.88rem}</style>")
    return style + "".join(parts)


# 다른 인물이 나오는 날이지만, 결과가 세라피나의 반응인 선택지
SERAPHINA_REACTS = {(13, 1)}


def resolve_choice(day, opt, kind="day"):
    """선택지를 골랐을 때 수치·플래그를 반영하고, 반응 장면에 보여 줄 내용을 돌려줌"""
    trap = trap_on(opt.get("trap"))
    stats, result, flag, bridge = opt["s"], opt["r"], opt.get("flag"), opt.get("next", "")
    if trap:
        stats, result, flag = trap["s"], T(trap["r"]), None
        bridge = trap.get("next", bridge)
        st.session_state.traps_hit += 1
    aff_change, tru_change, mistake = apply_choice(stats)
    st.session_state.last_mistake = mistake
    if flag:
        st.session_state.flags[flag] = True
    if kind == "day" and not trap and not opt.get("variant") and not opt.get("follow"):
        if day == 15:                                   # 가문 기록을 직접 봄
            st.session_state.flags["saw_record"] = True
        if day == 9 and opt["idx"] in (0, 1):           # 호숫가에서 마음을 털어놓음
            st.session_state.flags["lake_bond"] = True
    if kind == "day":
        st.session_state.last_bridge = bridge
        st.session_state.last_choice = (day, opt["idx"], bool(trap), bool(opt.get("variant")))
    log_history(day, ("🎁 " if kind == "event" else "") + ("🪤 " if trap else "") + opt["t"])
    if trap or mistake:
        st.session_state.setdefault("moments", []).append(
            {"day": day, "event": kind == "event", "trap": bool(trap), "choice": opt["t"],
             "why": result, "aff": aff_change, "tru": tru_change})
    face, face_label = reaction_face(stats, aff_change, tru_change, bool(trap), day)
    if kind == "day" and (day, opt["idx"]) in SERAPHINA_REACTS and not opt.get("follow"):
        face, face_label = "seraphina_30", "경계"     # 결과가 세라피나 이야기라면 세라피나 얼굴로
    sfx = "trap" if trap else ("up" if aff_change > 0 or (aff_change == 0 and tru_change > 0)
                               else ("down" if aff_change < 0 or tru_change < 0 else None))
    return {"day": day, "kind": kind, "choice": opt["t"], "result": result, "trap": bool(trap),
            "distant": bool(opt.get("variant")) or (kind == "day" and day in DISTANT and is_distant(day)),
            "aff": aff_change, "tru": tru_change, "mistake": mistake, "face": face,
            "face_label": face_label, "sfx": sfx}


def track_for(day, distant):
    """그날 배경 음악 (서먹한 버전 장면이면 설레는 곡 대신 잔잔한 곡)"""
    track = DAY_TRACK.get(day, "calm")
    return "calm" if distant and track == "romance" else track


def event_option(o, i):
    """선물·데이트 선택지: 그 반응에 필요한 일을 실제로 겪었는지에 따라 결과가 달라짐"""
    o = dict(o, idx=i)
    if o.get("need") and not st.session_state.flags.get(o["need"]):
        o["s"], o["r"] = o["alt"]["s"], T(o["alt"]["r"])
    return o


def finish_reaction():
    """반응 장면에서 '다음'을 눌렀을 때: 주말 이벤트가 있으면 이벤트로, 아니면 다음 날로"""
    r = st.session_state.reaction
    if r["kind"] == "day" and r["day"] in EVENTS and r["day"] not in st.session_state.events_done:
        st.session_state.phase = "event"
    else:
        advance_day()
        st.session_state.phase = "day"
    st.session_state.reaction = None


def stat_popup(r):
    """선택 직후 장면 위에 크게 뜨는 수치 변화 (예: 💚 호감도 +10  💙 신뢰도 +10)"""
    def badge(icon, name, v, delay):
        kind = "up" if v > 0 else ("down" if v < 0 else "zero")
        return (f'<div class="stat-badge {kind}" style="animation-delay:{delay:.2f}s;">'
                f'{icon} {name} <b>{v:+d}</b></div>')
    return ('<div class="stat-pop">' + badge("💚", "호감도", r["aff"], 0.9)
            + badge("💙", "신뢰도", r["tru"], 1.15) + '</div>')


def stat_text(r):
    if st.session_state.get("hide_stats"):
        return ""
    return f"호감도 {r['aff']:+d} · 신뢰도 {r['tru']:+d}"


# ==========================================
# 8. 화면
# ==========================================
settings_defaults()
for _k, _v in (("phase", "day"), ("reaction", None), ("events_done", [])):
    if _k not in st.session_state:
        st.session_state[_k] = _v

with st.sidebar:
    with st.expander("⚙️ 설정", expanded=False):
        st.slider("🎵 음악 크기", 0, 100, key="music_vol")
        st.slider("🔔 효과음 크기", 0, 100, key="sfx_vol")
        st.select_slider("💬 대사 나오는 속도", options=list(TEXT_SPEED.keys()), key="text_speed")
        st.checkbox("🙈 호감도·신뢰도 숫자 숨기기", key="hide_stats",
                    help="숫자 대신 세라피나의 표정과 관계 상태만 보고 마음을 짐작해요.")

# ------------------------------------------
# 시작 화면
# ------------------------------------------
if not st.session_state.game_started:
    # 판 번호(run_id)가 바뀌면 = 다시 시작하면, 음악도 처음부터 다시 나옴
    play_track("title")
    st.markdown(backdrop_css("bg_02"), unsafe_allow_html=True)
    st.markdown(stage_html("bg_02", "seraphina_50", "", T("📍 눈 내리는 애시포드의 밤")),
                unsafe_allow_html=True)
    st.markdown(T("""
<div class="story-card" style="text-align: center;">
<h3>🪄 애시포드 입학을 환영합니다!</h3>
<p>당신은 불꽃 기숙사 학생입니다.<br>어젯밤 친구들과 장난삼아 "30일 안에 서리 기숙사의 얼음 공주, <b>세라피나 윈터번</b>의 마음을 얻겠다"는 내기를 하고 말았습니다.<br>눈 내리는 겨울, 30일 동안 그녀의 마음을 사로잡아 보세요.</p>
</div>
"""), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        input_name = st.text_input("주인공(당신)의 이름을 입력하세요:", value="", placeholder="예: 레오")
        levels = list(DIFFICULTY.keys())
        chosen = st.radio("난이도", levels, index=levels.index(st.session_state.difficulty), horizontal=True)
        st.caption(DIFFICULTY[chosen]["desc"])
        st.radio("등장인물·학교 이름", NAME_MODES, index=None, horizontal=True, key="name_mode_pick")
        st.caption("원작: 해리 포터 세계관 이름 그대로 · 오리지널: 애시포드 마법학원 이름 "
                   "(고르지 않으면 원작 이름으로 시작해요)")
        st.caption("🎵 음악이 안 들리면 화면을 아무 데나 한 번 클릭해 주세요. 음량은 왼쪽 ⚙️ 설정에서 바꿀 수 있어요.")
        st.caption(f"🏷️ 게임 버전: {GAME_VERSION}")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 게임 시작하기"):
            if input_name.strip() != "":
                st.session_state.player_name = input_name.strip()
                st.session_state.difficulty = chosen
                st.session_state.name_mode = st.session_state.get("name_mode_pick") or "원작"
                st.session_state.game_started = True
                st.session_state.phase = "day"
                st.session_state.reaction = None
                st.session_state.events_done = []
                st.rerun()
            else:
                st.warning("이름을 입력해 주세요.")

else:
    hide = st.session_state.get("hide_stats")
    # 왼쪽 상태창
    with st.sidebar:
        st.markdown(f"👤 플레이어: **{st.session_state.player_name}**")
        st.markdown("### 📊 캐릭터 상태창")
        shown_day = min(st.session_state.day, 30)
        st.markdown(f"현재 날짜: Day {shown_day} / 30")
        st.progress(shown_day / 30.0)

        st.markdown("---")
        st.markdown(f"관계 상태: {get_relationship_status()}")
        if hide:
            st.caption("🙈 숫자를 숨겼어요. 세라피나의 표정으로 마음을 짐작해 보세요.")
        else:
            st.markdown(T(f"💚 세라피나 호감도: {st.session_state.affection} / 100"))
            st.progress(st.session_state.affection / 100.0)
            st.caption("호감도가 오를수록 표정이 밝아져요: 차가움 → 무심 → 옅은 미소 → 수줍음 → 편안함 → 애정 → 행복")
            st.markdown(T(f"💙 세라피나 신뢰도: {st.session_state.trust} / 100"))
            st.progress(st.session_state.trust / 100.0)
            st.markdown(f"❄️ 거리감/서먹함: {st.session_state.distance} / 100")
            st.progress(st.session_state.distance / 100.0)

        st.markdown(f"🔍 수집한 단서 수: {st.session_state.clues}개")
        st.markdown(f"🎚️ 난이도: {st.session_state.difficulty}")
        if DIFFICULTY[st.session_state.difficulty]["trap"]:
            st.markdown(f"🪤 빠진 함정: {st.session_state.traps_hit}개")
        if st.session_state.scars:
            st.markdown(f"💔 마음의 상처: {st.session_state.scars}개")
            if not hide:
                cap_aff, cap_tru = stat_caps()
                st.caption(f"상처 때문에 호감도는 최대 {cap_aff}, 신뢰도는 최대 {cap_tru}까지만 오를 수 있어요.")

        st.markdown("---")
        st.markdown("### 📜 주요 선택 기록")
        if st.session_state.history:
            for item in st.session_state.history[-5:]:
                st.caption(T(item))
        else:
            st.caption("아직 기록된 선택이 없습니다.")

        st.markdown("---")
        st.caption(f"🏷️ 게임 버전: {GAME_VERSION}")
        if st.button("🔄 처음으로 돌아가기 (이름 변경)"):
            init_game()
            st.session_state.phase = "day"
            st.session_state.reaction = None
            st.session_state.events_done = []
            st.rerun()

    phase = st.session_state.phase
    ended = st.session_state.day > 30 or st.session_state.game_over

    # ------------------------------------------
    # 에필로그 + 스태프 롤
    # ------------------------------------------
    if ended and phase == "epilogue":
        ending = localize(evaluate_ending())
        happy = ending["id"] in (1, 2)
        play_track("wedding" if happy else ("romance" if ending["id"] == 3 else "sad"))
        cg, bg_code, lv = ENDING_ART.get(ending["id"], (None, "bg_15", 50))
        st.markdown(backdrop_css(cg or bg_code), unsafe_allow_html=True)
        name = html.escape(st.session_state.player_name)
        credits_body = T(f"""<h3>포인센티아 (Poinsettia)</h3>
<p>{ending['title']}</p>
<h4>등장인물</h4>
<p>주인공 · {name}</p><p>세라피나 윈터번</p><p>클라라</p><p>에단</p>
<h4>무대</h4><p>눈 내리는 애시포드 마법학원</p>
<h4>그림</h4><p>포인센티아 일러스트</p>
<h4>음악 · 효과음</h4><p>게임에서 직접 만든 오르골 · 왈츠</p>
<h4>그리고</h4><p>30일 동안 함께해 준 당신</p>""")
        wed_html = wedding_frame(T(f"<small>{WEDDING_EPILOGUE[ending['id']][0]}</small>"
                                   f"💍 {name} ♥ 세라피나, 결혼을 축하합니다")) if wedding_ending(ending["id"]) else ""
        if wed_html:
            # 결혼 엔딩: 에필로그를 누르자마자 결혼식 그림 + 문구 + 제작진 자막
            st.markdown(wed_html, unsafe_allow_html=True)
            st.markdown(f'<div class="story-card"><p style="font-size:1.12rem;line-height:1.9;color:#f0f0f0">'
                        f'{T(WEDDING_EPILOGUE[ending["id"]][1])}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="credits-wrap"><div class="credits">{credits_body}<br><p>— 끝 —</p></div></div>',
                        unsafe_allow_html=True)
        elif happy:
            # 해피 엔딩(쉬움·보통): 둘의 '몇 년 후'를 보여 주는 에필로그 영상 + 자막
            st.markdown(epilogue_movie(ending["id"], st.session_state.player_name, credits_body),
                        unsafe_allow_html=True)
            st.markdown(f'<div class="story-card"><p style="font-size:1.05rem;line-height:1.8;color:#f0f0f0">'
                        f'{T(EPILOGUE[ending["id"]])}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(vn_stage(bg_code, "🌙 에필로그 · 몇 년 후", "",
                                 [{"kind": "narr", "text": T(EPILOGUE[ending["id"]])}],
                                 first_char=f"seraphina_{lv}", fallback_mood="smile"), unsafe_allow_html=True)
            st.markdown(f'<div class="credits-wrap"><div class="credits">{credits_body}<br><p>— 끝 —</p></div></div>',
                        unsafe_allow_html=True)
        # '에필로그 다시 보기'는 영상 안의 버튼으로 (누르면 영상과 노래가 처음부터)
        if st.button("🎮 다시 도전하기"):
            init_game()
            st.rerun()

    # ------------------------------------------
    # 엔딩
    # ------------------------------------------
    elif ended:
        ending = localize(evaluate_ending())
        # 엔딩 소리: 해피·트루 → 축하 / 노멀 → 따뜻한 오르골 / 씁쓸 → 단조 / 배드 → 게임 종료 / 최악 → 더 무거운 종료
        snd = ENDING_SOUND.get(ending["id"], "bad")
        play_scene(snd, sound_uri(f"sound_{snd}"), st.session_state.run_id)
        cg, bg_code, lv = ENDING_ART.get(ending["id"], (None, "bg_15", 50))
        st.markdown(backdrop_css(cg or bg_code), unsafe_allow_html=True)
        cg_uri = image_uri(cg, 1672) if cg else None
        if ending["id"] in ENDING_FX:
            st.markdown(ending_stage(ending["id"]), unsafe_allow_html=True)
        elif cg_uri:
            st.markdown(f'<img class="ending-cg" src="{cg_uri}" style="animation:stageFade 1.2s ease-out both;">',
                        unsafe_allow_html=True)
        else:
            st.markdown(stage_html(bg_code, f"seraphina_{lv}", "", "🎬 ENDING",
                                   fallback_mood="smile"), unsafe_allow_html=True)

        st.markdown(f"""
<div style="background-color: {ending['bg_color']}; padding: 30px; border-radius: 12px; border: 2px solid #8b263e; text-align: center;">
<h2 style="color: #ff6b81; font-family: 'Cinzel', serif;">{ending['title']}</h2>
<hr style="border-color: #8b263e;">
<p style="font-size: 1.1rem; line-height: 1.8; color: #f0f0f0;">{ending['desc']}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown(review_html(ending["id"]), unsafe_allow_html=True)
        st.markdown("### 📋 최종 플레이 결과 리포트")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("최종 호감도", f"{st.session_state.affection}점")
        col2.metric("최종 신뢰도", f"{st.session_state.trust}점")
        col3.metric("획득한 단서", f"{st.session_state.clues}개")
        col4.metric("빠진 함정", f"{st.session_state.traps_hit}개")

        st.markdown("---")
        c1, c2 = st.columns(2)
        if wedding_ending(ending["id"]):
            st.markdown('<div class="choice-head" style="color:#fda4af;font-size:1.05rem;margin:4px 0 10px 0">'
                        '💍 에필로그에서 두 사람의 결혼식이 기다리고 있어요.</div>', unsafe_allow_html=True)
        if c1.button("📜 에필로그 보기"):
            st.session_state.phase = "epilogue"
            st.rerun()
        if c2.button("🎮 다시 도전하기"):
            init_game()
            st.session_state.phase = "day"
            st.session_state.reaction = None
            st.session_state.events_done = []
            st.rerun()

    # ------------------------------------------
    # 반응 장면 (선택 직후 세라피나의 반응)
    # ------------------------------------------
    elif phase == "react" and st.session_state.reaction:
        r = st.session_state.reaction
        day = r["day"]
        if r["kind"] == "event":
            ev = EVENTS[day]
            bg_code, track, place = ev["bg"], ev["track"], T(ev["place"])
        else:
            story = localize(get_story_data(day))
            bg_code = story["bg"].split()[0]
            track = track_for(day, r.get("distant"))
            place = story["bg"][len(bg_code):].strip(" ()")
        play_track(track, r["sfx"], f"{st.session_state.run_id}-{day}-{r['kind']}")
        st.markdown(backdrop_css(bg_code), unsafe_allow_html=True)
        lines = [{"kind": "narr", "text": "▶ " + html.escape(T(r["choice"]))}]
        if r["trap"]:
            lines.append({"kind": "trap", "text": "🪤 함정이었어요!"})
        lines.append({"kind": "narr", "text": r["result"]})
        if r["mistake"] and DIFFICULTY[st.session_state.difficulty]["scar_trust"]:
            lines.append({"kind": "trap", "text": T("💔 세라피나의 마음에 상처가 남았습니다.")})
        # 수치 변화: 설정에서 숫자를 숨겼으면 아예 안 보여 주고, 아니면 장면 위에 크게 띄움
        overlay = "" if st.session_state.get("hide_stats") else stat_popup(r)
        label = T(f"세라피나 · {r['face_label']}") if r["face_label"] else ""
        st.markdown(vn_stage(bg_code, f"📍 {place} · DAY {day}", label, lines, first_char=r["face"],
                             fallback_mood="smile", overlay=overlay), unsafe_allow_html=True)
        st.markdown(choices_after_text(), unsafe_allow_html=True)
        if st.button("다음 ▶", key=f"next_{day}_{r['kind']}"):
            finish_reaction()
            st.rerun()

    # ------------------------------------------
    # 주말 선물·데이트 이벤트
    # ------------------------------------------
    elif phase == "event":
        day = st.session_state.day
        ev = localize(EVENTS[day])
        if ev.get("desc_far") and is_distant(day + 1):
            ev["desc"] = ev["desc_far"]
        play_track(ev["track"])
        st.markdown(backdrop_css(ev["bg"]), unsafe_allow_html=True)
        lv = seraphina_level("shy")
        st.markdown(vn_stage(ev["bg"], f"🎁 {ev['place']} · 주말", T(f"세라피나 · {LEVEL_LABEL[lv]}"),
                             [{"kind": "narr", "text": f'<span class="event-tag">🎁 {ev["title"]}</span>'},
                              {"kind": "narr", "text": ev["desc"]}],
                             first_char=f"seraphina_{lv}", fallback_mood="shy"), unsafe_allow_html=True)
        st.markdown(choices_after_text(), unsafe_allow_html=True)
        st.markdown(T('<div class="choice-head"><h4>🎁 무엇을 고를까요? '
                      '<small>(세라피나의 취향은 지금까지의 이야기 속에 힌트가 있어요)</small></h4></div>'),
                    unsafe_allow_html=True)
        opts = [event_option(o, i) for i, o in enumerate(ev["options"])]
        opts = choice_order(f"event{day}", [dict(o, follow=False) for o in opts])
        for pos, opt in enumerate(opts):
            if st.button(f"{pos+1}. {opt['t']}", key=f"ev_{day}_{opt['idx']}"):
                st.session_state.events_done = st.session_state.events_done + [day]
                st.session_state.reaction = resolve_choice(day, opt, kind="event")
                st.session_state.phase = "react"
                st.rerun()

    # ------------------------------------------
    # 하루 장면
    # ------------------------------------------
    else:
        current_day = st.session_state.day
        story = localize(get_story_data(current_day))
        play_track(track_for(current_day, story.get("distant")))

        bg_code = story["bg"].split()[0]
        st.markdown(backdrop_css(bg_code), unsafe_allow_html=True)
        if current_day == 21 and st.session_state.get("bet_penalty"):
            how_much = "크게" if hide else f"{st.session_state.bet_penalty}"
            st.markdown(T(f'<div class="bet-alert">💔 내기 소문이 학교 전체에 퍼졌습니다. '
                          f'세라피나의 호감도가 {how_much} 떨어졌어요.</div>'), unsafe_allow_html=True)
        place = story["bg"][len(bg_code):].strip(" ()")
        loc_text = f"📍 {place} · DAY {current_day} · {story['title']}"
        mood = mood_for_day(current_day)
        sera = f"seraphina_{seraphina_level(mood)}" if mood else None
        label = T(f"세라피나 · {LEVEL_LABEL[seraphina_level(mood)]}") if mood else ""

        lines = []
        # 서먹한 버전 장면은 그 장면에 맞는 첫 문장으로 시작 (어제 이어지는 문장 대신)
        bridge = story.get("intro") or st.session_state.get("last_bridge") or ""
        if bridge:
            lines.append({"kind": "bridge", "text": T(bridge)})
        lines.append({"kind": "narr", "text": story["desc"]})
        for speaker, text, style_class in story["dialogue"]:
            char = sera if style_class == "draco" else SPEAKER_IMG.get(style_class)
            lines.append({"kind": "say", "speaker": speaker, "text": text, "cls": style_class, "char": char})
        first = sera or DAY_OTHER.get(current_day)
        st.markdown(vn_stage(bg_code, loc_text, label, lines, first_char=first, fallback_mood=mood),
                    unsafe_allow_html=True)

        st.markdown(choices_after_text(), unsafe_allow_html=True)
        st.markdown(f'<div class="choice-head"><h4>💬 {html.escape(st.session_state.player_name)}(플레이어)의 선택:</h4></div>',
                    unsafe_allow_html=True)
        if st.session_state.get("last_choice"):
            st.markdown('<div class="choice-head" style="color:#94a3b8;font-size:.88rem;margin:-6px 0 8px 0">'
                        '↪ 표시가 붙은 선택지는 어제 고른 선택 때문에 새로 생긴 선택지예요.</div>',
                        unsafe_allow_html=True)

        options = choice_order(current_day, day_options(current_day, story))
        for pos, opt in enumerate(options):
            label_btn = f"{pos+1}. " + ("↪ " if opt["follow"] else "") + opt["t"]
            if st.button(label_btn, key=f"btn_day_{current_day}_{opt['idx']}"):
                # 함정인지는 '누르는 순간'의 관계 상태로 판단
                st.session_state.reaction = resolve_choice(current_day, opt, kind="day")
                st.session_state.phase = "react"
                st.rerun()
