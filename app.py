import streamlit as st
import random
import os
from PIL import Image, ImageDraw, ImageFont

# 💡 ページ設定はスクリプトの「一番最初」に実行する必要があります（Streamlitのルール）
st.set_page_config(page_title="タイ文字画像化マスター Pro", page_icon="🇹🇭", layout="centered")

# --- データの定義（子音の厳選14文字。動いたら母音なども追加可能です！） ---
THAI_CONSONANTS = {
    "ก": ["ko kai (鶏)", "kho khai (卵)", "kho khuat (瓶)", "ngo ngu (蛇)"],
    "ข": ["kho khai (卵)", "ko kai (鶏)", "kho khuat (瓶)", "cho chan (皿)"],
    "ค": ["kho khwai (水牛)", "kho khon (人)", "kho rakhang (鐘)", "ngo ngu (蛇)"],
    "ง": ["ngo ngu (蛇)", "no nu (ネズミ)", "mo ma (馬)", "lo ling (猿)"],
    "จ": ["cho chan (皿)", "cho ching (シンバル)", "cho chang (象)", "so so (鎖)"],
    "ด": ["do dek (子供)", "to tao (亀)", "do chada (冠)", "bo baimai (葉)"],
    "ต": ["to tao (亀)", "do dek (子供)", "to patak (突き棒)", "tho thung (袋)"],
    "น": ["no nu (ネズミ)", "mo ma (馬)", "no nen (小僧)", "lo ling (猿)"],
    "บ": ["bo baimai (葉)", "po pla (魚)", "pho phan (トレイ)", "fo fan (歯)"],
    "ป": ["po pla (魚)", "bo baimai (葉)", "pho phan (トレイ)", "fo fa (蓋)"],
    "ม": ["mo ma (馬)", "no nu (ネズミ)", "lo ling (猿)", "yo yak (夜叉)"],
    "ร": ["ro rua (船)", "lo ling (猿)", "wo waen (指輪)", "mo ma (馬)"],
    "ล": ["lo ling (猿)", "ro rua (船)", "so sua (虎)", "lo chula (凧)"],
    "ว": ["wo waen (指輪)", "ro rua (船)", "lo ling (猿)", "o ang (洗面器)"]
}

# --- 🔤 文字を画像化する魔法の関数（両フォントファイル読み込み版） ---
def create_letter_image(text, use_modern=False):
    # 200x200マスの白い画像を作る
    img = Image.new("RGB", (200, 200), "#F0F2F6")
    draw = ImageDraw.Draw(img)
    
    # 状況に応じて読み込むフォントファイルを切り替える
    if use_modern:
        font_path = "Kanit-Regular.ttf"
    else:
        font_path = "Sarabun-Regular.ttf" # 👈 アップロードした標準フォントを指定

    # フォントの読み込み
    if os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, 120)
        except Exception:
            font = ImageFont.load_default()
    else:
        # 万が一ファイルが見つからない場合のセーフティネット
        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except Exception:
            font = ImageFont.load_default()

    # 文字を中央寄りに描画
    draw.text((40, 20), text, fill="#0F172A" if not use_modern else "#DC2626", font=font)
    return img

# --- セッション状態の初期化 ---
if "quiz_font" not in st.session_state:
    st.session_state.quiz_font = "標準 (教科書体)"
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.choices = []
    st.session_state.answered = False
    st.session_state.feedback = ""

def next_question():
    st.session_state.current_char = random.choice(list(THAI_CONSONANTS.keys()))
    st.session_state.answered = False
    st.session_state.feedback = ""
    
    options = THAI_CONSONANTS[st.session_state.current_char].copy()
    correct = options[0]
    random.shuffle(options)
    st.session_state.choices = options
    st.session_state.correct_answer = correct

if "current_char" not in st.session_state or not st.session_state.choices:
    next_question()

# --- UIレイアウト ---
st.title("🇹🇭 タイ文字画像化マスター")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ アプリ設定")
    st.session_state.quiz_font = st.radio(
        "出題時の見た目：", 
        ["標準 (教科書体)", "丸なしモダン (Kanit)"]
    )
    if st.button("スコアをリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        next_question()
        st.rerun()

st.write(f"成績: **{st.session_state.score} / {st.session_state.total}** 問正解")
st.markdown("---")

# 出題画像の生成と表示
is_modern = (st.session_state.quiz_font == "丸なしモダン (Kanit)")
quiz_img = create_letter_image(st.session_state.current_char, use_modern=is_modern)

col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    st.image(quiz_img, use_container_width=True)

st.markdown("---")

# 4択ボタン
for choice in st.session_state.choices:
    if st.button(choice, use_container_width=True, disabled=st.session_state.answered):
        st.session_state.answered = True
        st.session_state.total += 1
        if choice == st.session_state.correct_answer:
            st.session_state.score += 1
            st.session_state.feedback = "⭕ 正解です！"
        else:
            st.session_state.feedback = f"❌ 残念！正解は 「{st.session_state.correct_answer}」 です。"
        st.rerun()

# 答え合わせと2フォント比較
if st.session_state.answered:
    if "⭕" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
    
    st.write("🔍 **画像で見るフォントの形の違い：**")
    img_standard = create_letter_image(st.session_state.current_char, use_modern=False)
    img_modern = create_letter_image(st.session_state.current_char, use_modern=True)
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        st.caption("標準（教科書体）")
        st.image(img_standard, use_container_width=True)
    with comp_col2:
        st.caption("丸なしモダン（看板）")
        st.image(img_modern, use_container_width=True)
        
    if st.button("次の問題へ進む ➡️", use_container_width=True):
        next_question()
        st.rerun()