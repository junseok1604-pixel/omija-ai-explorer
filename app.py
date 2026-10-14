# -*- coding: utf-8 -*-
"""오미자 AI 탐험대 5.0 — QR 접속용 Streamlit 모바일 웹 앱.
실제 생성형 AI 없이 사전 작성된 캐릭터 반응을 사용하는 성향 체험입니다.
"""
import json
from pathlib import Path
import streamlit as st

BASE = Path(__file__).resolve().parent
MENU_DATA = json.loads((BASE / "menus.json").read_text(encoding="utf-8"))["menus"]
QUESTIONS = [
    ("E", "I", "행사장에 도착했어! 가장 먼저 하고 싶은 건?", "새 친구에게 인사하며 함께 돌아보기!", "일단 둘러보고 마음에 드는 것부터 보기!"),
    ("S", "N", "비밀 재료 상자를 받았어. 어떻게 열어볼까?", "적힌 설명과 단서를 자세히 확인해!", "상상력을 발휘해 새로운 방법을 떠올려!"),
    ("T", "F", "친구들이 음료 이름을 두고 의견이 달라졌어!", "각 이름의 장점을 비교해 정해보자!", "친구들이 모두 기분 좋을 이름을 찾자!"),
    ("J", "P", "오늘 체험 부스를 즐기는 내 방식은?", "체험 순서를 미리 정하고 알차게!", "끌리는 부스부터 즉흥적으로!"),
    ("E", "I", "모험 중 재미있는 아이디어가 떠올랐어!", "친구에게 바로 말하며 더 발전시키기!", "머릿속으로 충분히 정리한 뒤 말하기!"),
    ("S", "N", "새로운 오미자 음료를 만든다면?", "정확한 양을 재서 맛부터 확인할래!", "상상 속 조합을 떠올려 도전할래!"),
    ("T", "F", "친구가 음료를 너무 시게 만들었대!", "왜 그런지 살펴보고 해결 방법을 찾자!", "속상할 친구를 위로하고 함께 다시 만들자!"),
    ("J", "P", "마지막 미션! 레시피를 받았다면?", "순서를 따라 하나씩 완성할래!", "기본은 참고하고 나만의 변화를 줄래!"),
]
COMMENTS = [
    ("새 친구와 함께하는 모험이 신나겠어!", "찬찬히 관찰하는 탐험가구나!"),
    ("단서를 꼼꼼하게 살펴보는구나!", "상상력이 반짝반짝 빛나!"),
    ("장단점을 비교하는 게 멋져!", "친구를 생각하는 마음이 따뜻해!"),
    ("미리 계획하면 든든하지!", "즉흥적인 모험도 즐겁지!"),
    ("아이디어를 함께 키워 가는구나!", "생각할 시간을 소중히 여기는구나!"),
    ("정확하게 확인하는 과학자 스타일!", "새로운 조합을 꿈꾸는 발명가 스타일!"),
    ("해결 방법을 찾는 데 집중하는구나!", "친구 마음부터 살피는구나!"),
    ("순서대로 완성하는 재미가 있지!", "나만의 방식으로 도전해 보는구나!"),
]

st.set_page_config(page_title="오미자 AI 탐험대", page_icon="🍒", layout="centered")
st.markdown("""<style>
.stApp {background: linear-gradient(180deg,#fff4f7 0%,#fffaf6 48%,#ffffff 100%);}
.block-container {max-width:760px;padding-top:1.35rem;padding-bottom:3rem;}
h1,h2,h3 {color:#59243a!important;}
div.stButton>button {min-height:3.35rem;white-space:normal;border-radius:17px;font-weight:750;font-size:1.07rem;}
div.stButton>button[kind="primary"] {background:#ed4774;border-color:#ed4774;color:white;}
div[data-testid="stAlert"] {border-radius:16px;}
.omi-bubble {background:white;border:2px solid #ffd0dc;border-radius:20px;padding:16px 18px;color:#49263b;font-size:1.08rem;line-height:1.7;}
.subcopy {font-size:.95rem;color:#765568;}
</style>""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "intro"
    st.session_state.answers = []
    st.session_state.selected_menu = None
    st.session_state.comment = ""

def photo(file_name, caption=None):
    path = BASE / "images" / file_name
    if path.is_file():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.info(f"📷 사진 준비 중! images/{file_name} 파일을 추가해 주세요.")

def mascot_says(message):
    left, right = st.columns([1, 3], vertical_alignment="center")
    with left:
        animation_for_page = {
            "intro": "omi_wave.gif",
            "quiz": "omi_think.gif",
            "result": "omi_celebrate.gif",
            "recipe": "omi_cook.gif",
            "all_menus": "omi_wave.gif",
        }
        animation = BASE / "images" / animation_for_page.get(st.session_state.page, "omi_wave.gif")
        fallback = BASE / "images" / "omi.png"
        if animation.is_file():
            st.image(animation.read_bytes(), use_container_width=True)
        elif fallback.is_file():
            st.image(str(fallback), use_container_width=True)
        else:
            st.markdown("# 🍒")
    with right:
        st.markdown(f'<div class="omi-bubble"><b>🍒 오미</b><br>{message}</div>', unsafe_allow_html=True)

def restart():
    st.session_state.page = "intro"
    st.session_state.answers = []
    st.session_state.selected_menu = None
    st.session_state.comment = ""

def mbti_type(answers):
    chars = []
    # 축마다 2문항, 동점이면 첫 문항 응답으로 결정하는 체험용 규칙
    for first in (0, 1, 2, 3):
        chosen = [answers[first], answers[first+4]]
        axis_a, axis_b = QUESTIONS[first][:2]
        chars.append(axis_a if chosen.count(0) >= chosen.count(1) else axis_b)
    return "".join(chars)

def find_menu(mbti):
    for idx, menu in enumerate(MENU_DATA):
        if mbti in menu.get("mbti", []):
            return idx
    return 0

def safe_alt_menu(idx):
    st.session_state.selected_menu = idx
    st.session_state.page = "recipe"

st.caption("🍒 교육지원청 체험 부스 · 나만의 오미자 찾기")

if st.session_state.page == "intro":
    st.title("🍒 오미자 AI 탐험대")
    st.subheader("나의 성향으로 찾아보는 특별한 오미자 메뉴!")
    mascot_says("안녕! 나는 오미야. 재미있는 상황 질문 8개에 답하면 너에게 어울리는 오미자 메뉴를 찾아줄게! 준비됐니?")
    st.info("약 2~3분 · 이름이나 연락처 입력 없음 · MBTI는 정식 검사 결과가 아닌 재미있는 체험용 추정이에요.")
    if st.button("🚀 탐험 시작하기", type="primary", use_container_width=True):
        st.session_state.page = "quiz"
        st.rerun()
    st.markdown('<p class="subcopy">※ 오미는 미리 작성한 대사로 반응하는 캐릭터입니다. 실제 생성형 AI 대화 기능은 사용하지 않습니다.</p>', unsafe_allow_html=True)

elif st.session_state.page == "quiz":
    num = len(st.session_state.answers)
    if num == len(QUESTIONS):
        st.session_state.page = "result"
        st.rerun()
    a, b, question, choice_a, choice_b = QUESTIONS[num]
    st.progress(num / len(QUESTIONS), text=f"미션 {num+1} / {len(QUESTIONS)}")
    st.title("오미와 성향 탐험")
    if st.session_state.comment:
        st.success("🍒 " + st.session_state.comment)
    mascot_says(question)
    st.write("**어느 쪽이 너와 더 가까워?**")
    for selection, label in enumerate((choice_a, choice_b)):
        if st.button(("🅰️  " if selection == 0 else "🅱️  ") + label, key=f"choice-{num}-{selection}", use_container_width=True, type="primary" if selection == 0 else "secondary"):
            st.session_state.answers.append(selection)
            st.session_state.comment = COMMENTS[num][selection]
            st.rerun()
    if num > 0 and st.button("← 이전 질문", use_container_width=True):
        st.session_state.answers.pop()
        st.session_state.comment = ""
        st.rerun()

elif st.session_state.page == "result":
    mbti = mbti_type(st.session_state.answers)
    selected = find_menu(mbti)
    st.title("✨ 탐험 완료!")
    mascot_says(f"너의 답변으로 살펴본 오늘의 성향은 <b>{mbti}</b>야! 재미있는 탐험 결과니까 정답처럼 생각하지 않아도 돼.")
    st.metric("오늘의 MBTI 탐험 결과", mbti)
    st.success(f"🍹 오미가 추천하는 메뉴: **{MENU_DATA[selected]['name']}**")
    photo(MENU_DATA[selected]["image"])
    st.write(MENU_DATA[selected]["description"])
    st.caption("메뉴 추천은 MBTI 선택에 따라 재미로 연결한 것이며, 성격·건강·취향을 과학적으로 판별한 결과가 아닙니다.")
    if st.button("📖 추천 메뉴 레시피 보기", type="primary", use_container_width=True):
        safe_alt_menu(selected)
        st.rerun()
    if st.button("🍹 다른 메뉴 선택하기 (알레르기·기호 고려)", use_container_width=True):
        st.session_state.page = "all_menus"
        st.rerun()

elif st.session_state.page == "all_menus":
    st.title("🍹 오미자 메뉴 5종")
    mascot_says("다른 메뉴도 살펴보자! 마음에 드는 오미자를 골라 봐!")
    st.info("추천과 관계없이 좋아하는 메뉴로 바꿀 수 있어요. 알레르기와 카페인 여부를 먼저 확인하세요.")
    for idx, menu in enumerate(MENU_DATA):
        with st.container(border=True):
            st.subheader(f"{idx+1}. {menu['name']}")
            photo(menu["image"])
            st.write(menu["description"])
            if st.button("이 메뉴의 레시피 보기", key=f"menu-{idx}", use_container_width=True):
                safe_alt_menu(idx)
                st.rerun()
    if st.button("처음부터 다시", use_container_width=True):
        restart(); st.rerun()

elif st.session_state.page == "recipe":
    idx = st.session_state.selected_menu
    if idx is None:
        st.session_state.page = "intro"; st.rerun()
    menu = MENU_DATA[idx]
    st.title("🧋 " + menu["name"])
    mascot_says("이제 직접 만들어볼 시간이야! 레시피를 보면서 천천히 만들어 보자. 필요한 경우 운영 선생님의 도움을 받아!")
    photo(menu["image"], caption=menu["name"])
    st.subheader("🥄 준비 재료 (1인분)")
    for line in menu["ingredients"]:
        st.write("• " + line)
    st.subheader("👩‍🍳 만드는 순서")
    for no, step in enumerate(menu["steps"], 1):
        st.write(f"**{no}.** {step}")
    st.warning("⚠️ " + menu.get("allergens", "재료의 알레르기 정보를 확인하세요."))
    st.caption("식품을 제조하기 전 손 씻기, 위생 도구 사용, 안전한 음료 온도 등을 확인하세요.")
    if st.button("다른 메뉴 보기", use_container_width=True):
        st.session_state.page = "all_menus"; st.rerun()
    if st.button("🔄 다음 참가자 / 처음부터", type="primary", use_container_width=True):
        restart(); st.rerun()
